"""
Command Line Interface Module.

🤖 This entire CLI was built by Claude AI by Anthropic!

This module provides the CLI for GPU Gaming Advisor using Typer.
Every command, every option, every help text - all written by Claude.
"""

import os
import sys
from typing import Optional
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich import print as rprint

from . import __version__, BANNER
from .gpu_detector import GPUDetector, GPUInfo
from .game_analyzer import GameAnalyzer
from .claude_advisor import ClaudeAdvisor
from .fps_predictor import FPSPredictor
from .monitor import GPUMonitor
from .utils import load_config, export_profile

# Create Typer app
app = typer.Typer(
    name="gpu-gaming-advisor",
    help="🎮 AI-powered GPU gaming optimization tool\n\n🤖 100% Built with Claude AI by Anthropic",
    add_completion=False,
)

console = Console()


def get_gpu_info() -> Optional[GPUInfo]:
    """Get GPU information."""
    detector = GPUDetector()
    if detector.initialize():
        gpu = detector.get_primary_gpu()
        detector.shutdown()
        return gpu
    return None


def print_header():
    """Print application header with Claude branding."""
    console.print(Panel(
        "[bold blue]🎮 GPU Gaming Advisor[/]\n"
        "[dim]AI-powered gaming optimization[/]\n\n"
        "[bold magenta]🤖 Built entirely with Claude AI by Anthropic[/]",
        border_style="blue",
        subtitle="[dim]anthropic.com/claude[/]"
    ))


@app.command()
def analyze():
    """Analyze your GPU and display detailed specifications."""
    print_header()
    
    with console.status("[bold green]Detecting GPU...[/]"):
        gpu = get_gpu_info()
    
    if not gpu:
        console.print("[red]❌ No GPU detected. Make sure you have NVIDIA drivers installed.[/]")
        raise typer.Exit(1)
    
    # Create info table
    table = Table(title=f"🖥️ {gpu.name}", show_header=True, header_style="bold cyan")
    table.add_column("Property", style="bold")
    table.add_column("Value", justify="right")
    
    table.add_row("Vendor", gpu.vendor)
    table.add_row("Architecture", gpu.architecture)
    table.add_row("Performance Tier", gpu.tier)
    table.add_row("VRAM", f"{gpu.vram_total / 1024:.0f} GB")
    table.add_row("CUDA Cores", f"{gpu.cuda_cores:,}")
    table.add_row("Base Clock", f"{gpu.base_clock} MHz")
    table.add_row("Boost Clock", f"{gpu.boost_clock} MHz")
    table.add_row("Driver Version", gpu.driver_version)
    
    console.print(table)
    
    # Current status
    console.print("\n[bold]Current Status:[/]")
    status_table = Table(show_header=False, box=None)
    status_table.add_column("Metric")
    status_table.add_column("Value", justify="right")
    
    temp_color = "green" if gpu.temperature < 70 else "yellow" if gpu.temperature < 85 else "red"
    status_table.add_row("Temperature", f"[{temp_color}]{gpu.temperature}°C[/]")
    status_table.add_row("GPU Usage", f"{gpu.gpu_usage}%")
    status_table.add_row("VRAM Used", f"{gpu.vram_used / 1024:.1f} / {gpu.vram_total / 1024:.0f} GB")
    
    if gpu.power_draw > 0:
        status_table.add_row("Power Draw", f"{gpu.power_draw:.0f}W / {gpu.power_limit:.0f}W")
    
    console.print(status_table)


@app.command()
def optimize(
    game: str = typer.Argument(..., help="Name of the game to optimize"),
    resolution: str = typer.Option("1920x1080", "--resolution", "-r", help="Target resolution"),
    target_fps: int = typer.Option(60, "--fps", "-f", help="Target framerate"),
    priority: str = typer.Option("balanced", "--priority", "-p", help="Priority: quality, balanced, or performance"),
):
    """Get AI-powered optimization recommendations for a specific game."""
    print_header()
    
    # Check API key
    config = load_config()
    api_key = config.get("anthropic", {}).get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        console.print("[red]❌ ANTHROPIC_API_KEY not set. Please set it in your environment or config file.[/]")
        raise typer.Exit(1)
    
    # Get GPU info
    with console.status("[bold green]Detecting GPU...[/]"):
        gpu = get_gpu_info()
    
    if not gpu:
        console.print("[red]❌ No GPU detected.[/]")
        raise typer.Exit(1)
    
    console.print(f"[green]✓[/] Detected: [bold]{gpu.name}[/]")
    
    # Check if game exists in database
    analyzer = GameAnalyzer()
    game_req = analyzer.get_game_requirements(game)
    
    if game_req:
        console.print(f"[green]✓[/] Game found: [bold]{game_req.name}[/]")
        game = game_req.name  # Use canonical name
    else:
        suggestions = analyzer.search_games(game)
        if suggestions:
            console.print(f"[yellow]⚠[/] Game '{game}' not in database. Similar games: {', '.join(suggestions[:3])}")
        else:
            console.print(f"[yellow]⚠[/] Game '{game}' not in database. Using AI estimation.")
    
    # Get recommendations from Claude
    with console.status(f"[bold green]Getting AI recommendations for {game}...[/]"):
        try:
            advisor = ClaudeAdvisor(api_key=api_key)
            recommendation = advisor.get_optimization_recommendation(
                gpu_info=gpu,
                game_name=game,
                resolution=resolution,
                target_fps=target_fps,
                priority=priority
            )
        except Exception as e:
            console.print(f"[red]❌ Error getting recommendations: {e}[/]")
            raise typer.Exit(1)
    
    # Display recommendations
    console.print(f"\n[bold]🎮 Optimized Settings for {game}[/]")
    console.print(f"Resolution: {resolution} | Target FPS: {target_fps} | Priority: {priority}\n")
    
    settings_table = Table(title="Recommended Settings", show_header=True)
    settings_table.add_column("Setting", style="bold")
    settings_table.add_column("Value", justify="right")
    
    for setting, value in recommendation.settings.items():
        settings_table.add_row(setting, str(value))
    
    console.print(settings_table)
    
    # FPS prediction
    fps_min, fps_max = recommendation.expected_fps_range
    fps_avg = (fps_min + fps_max) // 2
    
    console.print(f"\n[bold]📊 Expected Performance:[/]")
    console.print(f"   FPS Range: [green]{fps_min}[/] - [green]{fps_max}[/] (avg: ~{fps_avg})")
    console.print(f"   Confidence: {recommendation.confidence}")
    
    # Tips
    if recommendation.tips:
        console.print(f"\n[bold]💡 Tips:[/]")
        for tip in recommendation.tips:
            console.print(f"   • {tip}")
    
    # Offer to export
    if Confirm.ask("\n[dim]Save these settings to a profile?[/]", default=False):
        profile_name = Prompt.ask("Profile name", default=f"{game}_{resolution}")
        path = export_profile(profile_name, gpu.name, game, recommendation.settings)
        console.print(f"[green]✓ Profile saved to {path}[/]")


@app.command()
def predict(
    game: str = typer.Argument(..., help="Name of the game"),
    resolution: str = typer.Option("1920x1080", "--resolution", "-r", help="Target resolution"),
    quality: str = typer.Option("high", "--quality", "-q", help="Quality preset: low, medium, high, ultra"),
):
    """Predict FPS for a game at different settings."""
    print_header()
    
    gpu = get_gpu_info()
    if not gpu:
        console.print("[red]❌ No GPU detected.[/]")
        raise typer.Exit(1)
    
    console.print(f"[green]✓[/] GPU: [bold]{gpu.name}[/]\n")
    
    predictor = FPSPredictor()
    
    # Predict for specified settings
    prediction = predictor.predict(gpu, game, resolution, quality)
    
    console.print(f"[bold]📊 FPS Prediction for {game}[/]")
    console.print(f"Resolution: {resolution} | Quality: {quality.title()}\n")
    
    # Create results table
    table = Table(show_header=True)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")
    
    table.add_row("Average FPS", f"[green]{prediction.fps_average}[/]")
    table.add_row("FPS Range", f"{prediction.fps_min} - {prediction.fps_max}")
    table.add_row("1% Low", f"[yellow]{prediction.fps_1_percent_low}[/]")
    table.add_row("Confidence", prediction.confidence)
    
    console.print(table)
    
    if prediction.notes:
        console.print("\n[bold]📝 Notes:[/]")
        for note in prediction.notes:
            console.print(f"   • {note}")
    
    # Show all presets
    if Confirm.ask("\n[dim]Show predictions for all quality presets?[/]", default=False):
        all_predictions = predictor.predict_all_presets(gpu, game, resolution)
        
        preset_table = Table(title=f"All Quality Presets at {resolution}")
        preset_table.add_column("Preset", style="bold")
        preset_table.add_column("Avg FPS", justify="right")
        preset_table.add_column("Range", justify="right")
        preset_table.add_column("1% Low", justify="right")
        
        for preset, pred in all_predictions.items():
            fps_color = "green" if pred.fps_average >= 60 else "yellow" if pred.fps_average >= 30 else "red"
            preset_table.add_row(
                preset.title(),
                f"[{fps_color}]{pred.fps_average}[/]",
                f"{pred.fps_min}-{pred.fps_max}",
                str(pred.fps_1_percent_low)
            )
        
        console.print(preset_table)


@app.command()
def compare(
    other_gpu: str = typer.Argument(..., help="GPU to compare against (e.g., 'RTX 4070')"),
    game: str = typer.Option(None, "--game", "-g", help="Specific game for comparison"),
):
    """Compare your GPU with another model."""
    print_header()
    
    gpu = get_gpu_info()
    if not gpu:
        console.print("[red]❌ No GPU detected.[/]")
        raise typer.Exit(1)
    
    console.print(f"[green]✓[/] Your GPU: [bold]{gpu.name}[/]")
    console.print(f"[green]✓[/] Comparing to: [bold]{other_gpu}[/]\n")
    
    predictor = FPSPredictor()
    
    if game:
        # Compare for specific game
        comparison = predictor.compare_gpus(gpu, other_gpu, game)
        
        console.print(f"[bold]📊 Comparison for {game}[/]\n")
        
        table = Table(show_header=True)
        table.add_column("GPU", style="bold")
        table.add_column("Est. FPS", justify="right")
        
        table.add_row(comparison["gpu1_name"], f"[cyan]{comparison['gpu1_fps']}[/]")
        table.add_row(comparison["gpu2_name"], f"[cyan]{comparison['gpu2_fps']}[/]")
        
        console.print(table)
        
        diff = comparison["percentage_difference"]
        if diff > 0:
            console.print(f"\n[yellow]{other_gpu}[/] is approximately [green]{diff}%[/] faster")
        elif diff < 0:
            console.print(f"\n[yellow]{gpu.name}[/] is approximately [green]{abs(diff)}%[/] faster")
        else:
            console.print("\n[yellow]Both GPUs have similar performance[/]")
    else:
        # General comparison across multiple games
        games = ["Cyberpunk 2077", "Fortnite", "Counter-Strike 2", "Elden Ring"]
        
        table = Table(title=f"Performance Comparison: {gpu.name} vs {other_gpu}")
        table.add_column("Game", style="bold")
        table.add_column(gpu.name, justify="right")
        table.add_column(other_gpu, justify="right")
        table.add_column("Difference", justify="right")
        
        for game_name in games:
            comparison = predictor.compare_gpus(gpu, other_gpu, game_name)
            diff = comparison["percentage_difference"]
            diff_str = f"[green]+{diff}%[/]" if diff > 0 else f"[red]{diff}%[/]"
            
            table.add_row(
                game_name,
                str(comparison["gpu1_fps"]),
                str(comparison["gpu2_fps"]),
                diff_str
            )
        
        console.print(table)
        console.print("\n[dim]Note: Positive difference means the compared GPU is faster[/]")


@app.command()
def monitor(
    duration: int = typer.Option(None, "--duration", "-d", help="Duration in seconds (default: indefinite)"),
    refresh: float = typer.Option(1.0, "--refresh", "-r", help="Refresh rate in seconds"),
):
    """Monitor GPU performance in real-time."""
    print_header()
    
    gpu_monitor = GPUMonitor(refresh_rate=refresh)
    
    console.print("[bold green]Starting GPU monitor...[/]")
    console.print("[dim]Press Ctrl+C to stop[/]\n")
    
    gpu_monitor.start_monitoring(duration=float(duration) if duration else None)


@app.command("list-games")
def list_games(
    search: str = typer.Option(None, "--search", "-s", help="Search for games"),
    feature: str = typer.Option(None, "--feature", "-f", help="Filter by feature: raytracing, dlss, fsr"),
):
    """List all supported games in the database."""
    print_header()
    
    analyzer = GameAnalyzer()
    
    if feature:
        games = analyzer.get_games_by_feature(feature)
        title = f"Games with {feature.upper()} support"
    elif search:
        games = analyzer.search_games(search)
        title = f"Games matching '{search}'"
    else:
        games = analyzer.list_games()
        title = "Supported Games"
    
    if not games:
        console.print(f"[yellow]No games found[/]")
        return
    
    table = Table(title=title)
    table.add_column("#", style="dim")
    table.add_column("Game", style="bold")
    table.add_column("Engine")
    table.add_column("RT", justify="center")
    table.add_column("DLSS", justify="center")
    table.add_column("FSR", justify="center")
    
    for i, game_name in enumerate(games, 1):
        req = analyzer.get_game_requirements(game_name)
        if req:
            table.add_row(
                str(i),
                game_name,
                req.engine,
                "✓" if req.supports_raytracing else "✗",
                "✓" if req.supports_dlss else "✗",
                "✓" if req.supports_fsr else "✗",
            )
    
    console.print(table)
    console.print(f"\n[dim]Total: {len(games)} games[/]")


@app.command()
def interactive():
    """Start an interactive chat session with Claude about gaming optimization."""
    print_header()
    
    # Check API key
    config = load_config()
    api_key = config.get("anthropic", {}).get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        console.print("[red]❌ ANTHROPIC_API_KEY not set.[/]")
        raise typer.Exit(1)
    
    # Get GPU info
    gpu = get_gpu_info()
    if not gpu:
        console.print("[red]❌ No GPU detected.[/]")
        raise typer.Exit(1)
    
    console.print(f"[green]✓[/] GPU: [bold]{gpu.name}[/]")
    console.print("[dim]Type 'quit' or 'exit' to end the conversation[/]\n")
    
    advisor = ClaudeAdvisor(api_key=api_key)
    conversation_history = []
    
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/]")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("[dim]Goodbye! Happy gaming! 🎮[/]")
                break
            
            if not user_input.strip():
                continue
            
            with console.status("[bold green]Thinking...[/]"):
                response = advisor.chat(gpu, user_input, conversation_history)
            
            # Update history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": response})
            
            console.print(f"\n[bold green]Claude:[/] {response}\n")
            
        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye! Happy gaming! 🎮[/]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")


@app.command()
def export(
    output: str = typer.Option("profile.json", "--output", "-o", help="Output file path"),
    game: str = typer.Option(None, "--game", "-g", help="Game name for the profile"),
):
    """Export your GPU profile and settings."""
    print_header()
    
    gpu = get_gpu_info()
    if not gpu:
        console.print("[red]❌ No GPU detected.[/]")
        raise typer.Exit(1)
    
    import json
    from datetime import datetime
    
    profile = {
        "exported_at": datetime.now().isoformat(),
        "gpu": gpu.to_dict(),
    }
    
    if game:
        analyzer = GameAnalyzer()
        compatibility = analyzer.check_compatibility(gpu, game)
        profile["game_compatibility"] = compatibility
    
    with open(output, 'w') as f:
        json.dump(profile, f, indent=2)
    
    console.print(f"[green]✓ Profile exported to {output}[/]")


@app.command()
def version():
    """Show version information."""
    console.print(Panel(
        f"[bold blue]GPU Gaming Advisor[/] v{__version__}\n\n"
        "[bold magenta]🤖 100% Built with Claude AI[/]\n"
        "[dim]by Anthropic[/]\n\n"
        "This entire application - every line of code,\n"
        "every feature, every piece of documentation -\n"
        "was created by Claude, Anthropic's AI assistant.\n\n"
        "[cyan]Learn more:[/]\n"
        "• Claude AI: [link=https://anthropic.com/claude]anthropic.com/claude[/link]\n"
        "• API Console: [link=https://console.anthropic.com]console.anthropic.com[/link]",
        title="🎮 About",
        border_style="blue"
    ))


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
