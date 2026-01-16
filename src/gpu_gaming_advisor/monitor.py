"""
GPU Monitoring Module.

This module provides real-time GPU monitoring functionality
with a beautiful terminal dashboard.
"""

import time
import threading
from typing import Optional, Callable, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text

from .gpu_detector import GPUDetector, GPUInfo


@dataclass
class GPUMetrics:
    """Data class for GPU metrics at a point in time."""
    
    timestamp: datetime
    temperature: float
    gpu_usage: float
    memory_usage: float
    memory_used: int
    memory_total: int
    power_draw: float
    power_limit: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "temperature_c": self.temperature,
            "gpu_usage_percent": self.gpu_usage,
            "memory_usage_percent": self.memory_usage,
            "memory_used_mb": self.memory_used,
            "memory_total_mb": self.memory_total,
            "power_draw_w": self.power_draw,
            "power_limit_w": self.power_limit,
        }


@dataclass
class MonitoringSession:
    """Data class for a monitoring session."""
    
    start_time: datetime
    end_time: Optional[datetime] = None
    gpu_name: str = ""
    metrics_history: List[GPUMetrics] = field(default_factory=list)
    
    @property
    def duration_seconds(self) -> float:
        """Get session duration in seconds."""
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
    
    @property
    def avg_temperature(self) -> float:
        """Get average temperature."""
        if not self.metrics_history:
            return 0.0
        return sum(m.temperature for m in self.metrics_history) / len(self.metrics_history)
    
    @property
    def max_temperature(self) -> float:
        """Get maximum temperature."""
        if not self.metrics_history:
            return 0.0
        return max(m.temperature for m in self.metrics_history)
    
    @property
    def avg_gpu_usage(self) -> float:
        """Get average GPU usage."""
        if not self.metrics_history:
            return 0.0
        return sum(m.gpu_usage for m in self.metrics_history) / len(self.metrics_history)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary."""
        return {
            "gpu_name": self.gpu_name,
            "duration_seconds": self.duration_seconds,
            "samples": len(self.metrics_history),
            "avg_temperature": round(self.avg_temperature, 1),
            "max_temperature": self.max_temperature,
            "avg_gpu_usage": round(self.avg_gpu_usage, 1),
        }


class GPUMonitor:
    """
    Real-time GPU monitoring with terminal dashboard.
    
    This class provides functionality to monitor GPU metrics
    in real-time with a beautiful Rich-based interface.
    """
    
    def __init__(self, refresh_rate: float = 1.0):
        """
        Initialize the GPU Monitor.
        
        Args:
            refresh_rate: Refresh rate in seconds.
        """
        self.refresh_rate = refresh_rate
        self.detector = GPUDetector()
        self.console = Console()
        self._monitoring = False
        self._current_session: Optional[MonitoringSession] = None
        self._callbacks: List[Callable[[GPUInfo], None]] = []
    
    def _get_temp_color(self, temp: float) -> str:
        """Get color based on temperature."""
        if temp < 50:
            return "green"
        elif temp < 70:
            return "yellow"
        elif temp < 85:
            return "orange1"
        else:
            return "red"
    
    def _get_usage_color(self, usage: float) -> str:
        """Get color based on usage percentage."""
        if usage < 50:
            return "green"
        elif usage < 80:
            return "yellow"
        else:
            return "red"
    
    def _create_dashboard(self, gpu_info: GPUInfo) -> Panel:
        """Create the monitoring dashboard."""
        # Main layout
        layout = Layout()
        
        # GPU Info section
        info_text = Text()
        info_text.append(f"🖥️  {gpu_info.name}\n", style="bold cyan")
        info_text.append(f"   Architecture: {gpu_info.architecture}\n", style="dim")
        info_text.append(f"   Driver: {gpu_info.driver_version}\n", style="dim")
        info_text.append(f"   VRAM: {gpu_info.vram_total / 1024:.0f} GB\n", style="dim")
        
        # Create metrics table
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Metric", style="bold")
        table.add_column("Value", justify="right")
        table.add_column("Bar", width=30)
        
        # Temperature
        temp_color = self._get_temp_color(gpu_info.temperature)
        temp_bar = self._create_bar(gpu_info.temperature, 100, temp_color)
        table.add_row(
            "🌡️  Temperature",
            f"[{temp_color}]{gpu_info.temperature:.0f}°C[/]",
            temp_bar
        )
        
        # GPU Usage
        gpu_color = self._get_usage_color(gpu_info.gpu_usage)
        gpu_bar = self._create_bar(gpu_info.gpu_usage, 100, gpu_color)
        table.add_row(
            "⚡ GPU Usage",
            f"[{gpu_color}]{gpu_info.gpu_usage:.0f}%[/]",
            gpu_bar
        )
        
        # Memory Usage
        mem_percent = (gpu_info.vram_used / gpu_info.vram_total * 100) if gpu_info.vram_total > 0 else 0
        mem_color = self._get_usage_color(mem_percent)
        mem_bar = self._create_bar(mem_percent, 100, mem_color)
        table.add_row(
            "💾 VRAM Used",
            f"[{mem_color}]{gpu_info.vram_used / 1024:.1f} / {gpu_info.vram_total / 1024:.0f} GB[/]",
            mem_bar
        )
        
        # Power Draw
        if gpu_info.power_limit > 0:
            power_percent = (gpu_info.power_draw / gpu_info.power_limit * 100)
            power_color = self._get_usage_color(power_percent)
            power_bar = self._create_bar(power_percent, 100, power_color)
            table.add_row(
                "🔌 Power Draw",
                f"[{power_color}]{gpu_info.power_draw:.0f}W / {gpu_info.power_limit:.0f}W[/]",
                power_bar
            )
        
        # Session info if monitoring
        session_text = ""
        if self._current_session:
            duration = self._current_session.duration_seconds
            samples = len(self._current_session.metrics_history)
            session_text = f"\n\n📊 Session: {duration:.0f}s | {samples} samples | Avg Temp: {self._current_session.avg_temperature:.1f}°C"
        
        # Combine all elements
        content = Text()
        content.append_text(info_text)
        content.append("\n")
        
        panel_content = f"{info_text}\n{table}{session_text}"
        
        return Panel(
            table,
            title="[bold blue]GPU Gaming Advisor - Real-time Monitor[/]",
            subtitle=f"[dim]{gpu_info.name} | Press Ctrl+C to stop[/]",
            border_style="blue",
        )
    
    def _create_bar(self, value: float, max_value: float, color: str) -> Text:
        """Create a progress bar."""
        width = 20
        filled = int((value / max_value) * width) if max_value > 0 else 0
        bar = "█" * filled + "░" * (width - filled)
        return Text(bar, style=color)
    
    def start_monitoring(
        self,
        duration: Optional[float] = None,
        callback: Optional[Callable[[GPUInfo], None]] = None
    ):
        """
        Start real-time GPU monitoring with dashboard.
        
        Args:
            duration: Optional duration in seconds. None for indefinite.
            callback: Optional callback function called with each update.
        """
        if not self.detector.initialize():
            self.console.print("[red]Failed to initialize GPU detector[/]")
            return
        
        self._monitoring = True
        self._current_session = MonitoringSession(
            start_time=datetime.now(),
            gpu_name=""
        )
        
        if callback:
            self._callbacks.append(callback)
        
        start_time = time.time()
        
        try:
            with Live(console=self.console, refresh_per_second=1/self.refresh_rate) as live:
                while self._monitoring:
                    # Check duration
                    if duration and (time.time() - start_time) >= duration:
                        break
                    
                    # Get GPU info
                    gpu_info = self.detector.get_primary_gpu()
                    
                    if gpu_info:
                        # Update session
                        self._current_session.gpu_name = gpu_info.name
                        
                        # Record metrics
                        metrics = GPUMetrics(
                            timestamp=datetime.now(),
                            temperature=gpu_info.temperature,
                            gpu_usage=gpu_info.gpu_usage,
                            memory_usage=gpu_info.memory_usage,
                            memory_used=gpu_info.vram_used,
                            memory_total=gpu_info.vram_total,
                            power_draw=gpu_info.power_draw,
                            power_limit=gpu_info.power_limit,
                        )
                        self._current_session.metrics_history.append(metrics)
                        
                        # Update dashboard
                        dashboard = self._create_dashboard(gpu_info)
                        live.update(dashboard)
                        
                        # Call callbacks
                        for cb in self._callbacks:
                            cb(gpu_info)
                    
                    time.sleep(self.refresh_rate)
                    
        except KeyboardInterrupt:
            pass
        finally:
            self._monitoring = False
            self._current_session.end_time = datetime.now()
            self.detector.shutdown()
            
            # Print session summary
            if self._current_session.metrics_history:
                self._print_session_summary()
    
    def _print_session_summary(self):
        """Print session summary after monitoring ends."""
        if not self._current_session:
            return
        
        summary = self._current_session.get_summary()
        
        self.console.print("\n")
        self.console.print(Panel(
            f"""[bold]Monitoring Session Summary[/]
            
GPU: {summary['gpu_name']}
Duration: {summary['duration_seconds']:.1f} seconds
Samples: {summary['samples']}

Average Temperature: {summary['avg_temperature']}°C
Maximum Temperature: {summary['max_temperature']}°C
Average GPU Usage: {summary['avg_gpu_usage']}%""",
            title="📊 Session Complete",
            border_style="green"
        ))
    
    def stop_monitoring(self):
        """Stop the monitoring loop."""
        self._monitoring = False
    
    def get_current_metrics(self) -> Optional[GPUInfo]:
        """
        Get current GPU metrics (single snapshot).
        
        Returns:
            GPUInfo with current metrics.
        """
        if not self.detector.initialize():
            return None
        
        gpu_info = self.detector.get_primary_gpu()
        self.detector.shutdown()
        return gpu_info
    
    def get_session_data(self) -> Optional[MonitoringSession]:
        """Get the current or last monitoring session."""
        return self._current_session
    
    def export_session(self, filepath: str):
        """
        Export session data to JSON.
        
        Args:
            filepath: Path to save the JSON file.
        """
        if not self._current_session:
            self.console.print("[yellow]No session data to export[/]")
            return
        
        import json
        
        data = {
            "summary": self._current_session.get_summary(),
            "metrics": [m.to_dict() for m in self._current_session.metrics_history]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.console.print(f"[green]Session exported to {filepath}[/]")


def quick_monitor(duration: float = 10.0, refresh_rate: float = 1.0):
    """
    Quick monitoring function for simple use cases.
    
    Args:
        duration: Duration to monitor in seconds.
        refresh_rate: Refresh rate in seconds.
    """
    monitor = GPUMonitor(refresh_rate=refresh_rate)
    monitor.start_monitoring(duration=duration)


if __name__ == "__main__":
    # Test the monitor
    quick_monitor(duration=30.0)
