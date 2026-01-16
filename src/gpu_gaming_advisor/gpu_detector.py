"""
GPU Detection and Information Module.

This module provides functionality to detect NVIDIA GPUs and retrieve
detailed information about their specifications and current status.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import platform
import subprocess

try:
    import pynvml
    PYNVML_AVAILABLE = True
except ImportError:
    PYNVML_AVAILABLE = False

try:
    import GPUtil
    GPUTIL_AVAILABLE = True
except ImportError:
    GPUTIL_AVAILABLE = False


@dataclass
class GPUInfo:
    """Data class containing GPU information."""
    
    name: str
    vendor: str = "Unknown"
    vram_total: int = 0  # MB
    vram_used: int = 0  # MB
    vram_free: int = 0  # MB
    cuda_cores: int = 0
    base_clock: int = 0  # MHz
    boost_clock: int = 0  # MHz
    temperature: float = 0.0  # Celsius
    gpu_usage: float = 0.0  # Percentage
    memory_usage: float = 0.0  # Percentage
    power_draw: float = 0.0  # Watts
    power_limit: float = 0.0  # Watts
    driver_version: str = "Unknown"
    architecture: str = "Unknown"
    pcie_gen: int = 0
    pcie_width: int = 0
    
    # Performance tier classification
    tier: str = "Unknown"
    
    # Additional metadata
    uuid: str = ""
    index: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert GPU info to dictionary."""
        return {
            "name": self.name,
            "vendor": self.vendor,
            "vram_total_mb": self.vram_total,
            "vram_used_mb": self.vram_used,
            "vram_free_mb": self.vram_free,
            "cuda_cores": self.cuda_cores,
            "base_clock_mhz": self.base_clock,
            "boost_clock_mhz": self.boost_clock,
            "temperature_c": self.temperature,
            "gpu_usage_percent": self.gpu_usage,
            "memory_usage_percent": self.memory_usage,
            "power_draw_w": self.power_draw,
            "power_limit_w": self.power_limit,
            "driver_version": self.driver_version,
            "architecture": self.architecture,
            "tier": self.tier,
        }
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the GPU."""
        return (
            f"{self.name}\n"
            f"├── VRAM: {self.vram_total / 1024:.0f} GB\n"
            f"├── Architecture: {self.architecture}\n"
            f"├── CUDA Cores: {self.cuda_cores:,}\n"
            f"├── Base/Boost Clock: {self.base_clock}/{self.boost_clock} MHz\n"
            f"└── Driver: {self.driver_version}"
        )


# GPU specifications database for common NVIDIA cards
GPU_SPECS_DATABASE: Dict[str, Dict[str, Any]] = {
    # RTX 40 Series
    "RTX 4090": {"cuda_cores": 16384, "base_clock": 2235, "boost_clock": 2520, "architecture": "Ada Lovelace", "tier": "Enthusiast"},
    "RTX 4080 SUPER": {"cuda_cores": 10240, "base_clock": 2290, "boost_clock": 2550, "architecture": "Ada Lovelace", "tier": "Enthusiast"},
    "RTX 4080": {"cuda_cores": 9728, "base_clock": 2205, "boost_clock": 2505, "architecture": "Ada Lovelace", "tier": "Enthusiast"},
    "RTX 4070 TI SUPER": {"cuda_cores": 8448, "base_clock": 2340, "boost_clock": 2610, "architecture": "Ada Lovelace", "tier": "High-End"},
    "RTX 4070 TI": {"cuda_cores": 7680, "base_clock": 2310, "boost_clock": 2610, "architecture": "Ada Lovelace", "tier": "High-End"},
    "RTX 4070 SUPER": {"cuda_cores": 7168, "base_clock": 1980, "boost_clock": 2475, "architecture": "Ada Lovelace", "tier": "High-End"},
    "RTX 4070": {"cuda_cores": 5888, "base_clock": 1920, "boost_clock": 2475, "architecture": "Ada Lovelace", "tier": "High-End"},
    "RTX 4060 TI": {"cuda_cores": 4352, "base_clock": 2310, "boost_clock": 2535, "architecture": "Ada Lovelace", "tier": "Mid-Range"},
    "RTX 4060": {"cuda_cores": 3072, "base_clock": 1830, "boost_clock": 2460, "architecture": "Ada Lovelace", "tier": "Mid-Range"},
    
    # RTX 30 Series
    "RTX 3090 TI": {"cuda_cores": 10752, "base_clock": 1560, "boost_clock": 1860, "architecture": "Ampere", "tier": "Enthusiast"},
    "RTX 3090": {"cuda_cores": 10496, "base_clock": 1395, "boost_clock": 1695, "architecture": "Ampere", "tier": "Enthusiast"},
    "RTX 3080 TI": {"cuda_cores": 10240, "base_clock": 1365, "boost_clock": 1665, "architecture": "Ampere", "tier": "Enthusiast"},
    "RTX 3080": {"cuda_cores": 8704, "base_clock": 1440, "boost_clock": 1710, "architecture": "Ampere", "tier": "High-End"},
    "RTX 3070 TI": {"cuda_cores": 6144, "base_clock": 1575, "boost_clock": 1770, "architecture": "Ampere", "tier": "High-End"},
    "RTX 3070": {"cuda_cores": 5888, "base_clock": 1500, "boost_clock": 1725, "architecture": "Ampere", "tier": "High-End"},
    "RTX 3060 TI": {"cuda_cores": 4864, "base_clock": 1410, "boost_clock": 1670, "architecture": "Ampere", "tier": "Mid-Range"},
    "RTX 3060": {"cuda_cores": 3584, "base_clock": 1320, "boost_clock": 1777, "architecture": "Ampere", "tier": "Mid-Range"},
    "RTX 3050": {"cuda_cores": 2560, "base_clock": 1552, "boost_clock": 1777, "architecture": "Ampere", "tier": "Entry"},
    
    # RTX 20 Series
    "RTX 2080 TI": {"cuda_cores": 4352, "base_clock": 1350, "boost_clock": 1545, "architecture": "Turing", "tier": "High-End"},
    "RTX 2080 SUPER": {"cuda_cores": 3072, "base_clock": 1650, "boost_clock": 1815, "architecture": "Turing", "tier": "High-End"},
    "RTX 2080": {"cuda_cores": 2944, "base_clock": 1515, "boost_clock": 1710, "architecture": "Turing", "tier": "High-End"},
    "RTX 2070 SUPER": {"cuda_cores": 2560, "base_clock": 1605, "boost_clock": 1770, "architecture": "Turing", "tier": "Mid-Range"},
    "RTX 2070": {"cuda_cores": 2304, "base_clock": 1410, "boost_clock": 1620, "architecture": "Turing", "tier": "Mid-Range"},
    "RTX 2060 SUPER": {"cuda_cores": 2176, "base_clock": 1470, "boost_clock": 1650, "architecture": "Turing", "tier": "Mid-Range"},
    "RTX 2060": {"cuda_cores": 1920, "base_clock": 1365, "boost_clock": 1680, "architecture": "Turing", "tier": "Entry"},
    
    # GTX 16 Series
    "GTX 1660 TI": {"cuda_cores": 1536, "base_clock": 1500, "boost_clock": 1770, "architecture": "Turing", "tier": "Entry"},
    "GTX 1660 SUPER": {"cuda_cores": 1408, "base_clock": 1530, "boost_clock": 1785, "architecture": "Turing", "tier": "Entry"},
    "GTX 1660": {"cuda_cores": 1408, "base_clock": 1530, "boost_clock": 1785, "architecture": "Turing", "tier": "Entry"},
    "GTX 1650 SUPER": {"cuda_cores": 1280, "base_clock": 1530, "boost_clock": 1725, "architecture": "Turing", "tier": "Entry"},
    "GTX 1650": {"cuda_cores": 896, "base_clock": 1485, "boost_clock": 1665, "architecture": "Turing", "tier": "Entry"},
    
    # GTX 10 Series
    "GTX 1080 TI": {"cuda_cores": 3584, "base_clock": 1480, "boost_clock": 1582, "architecture": "Pascal", "tier": "High-End"},
    "GTX 1080": {"cuda_cores": 2560, "base_clock": 1607, "boost_clock": 1733, "architecture": "Pascal", "tier": "Mid-Range"},
    "GTX 1070 TI": {"cuda_cores": 2432, "base_clock": 1607, "boost_clock": 1683, "architecture": "Pascal", "tier": "Mid-Range"},
    "GTX 1070": {"cuda_cores": 1920, "base_clock": 1506, "boost_clock": 1683, "architecture": "Pascal", "tier": "Mid-Range"},
    "GTX 1060": {"cuda_cores": 1280, "base_clock": 1506, "boost_clock": 1708, "architecture": "Pascal", "tier": "Entry"},
    "GTX 1050 TI": {"cuda_cores": 768, "base_clock": 1290, "boost_clock": 1392, "architecture": "Pascal", "tier": "Entry"},
    "GTX 1050": {"cuda_cores": 640, "base_clock": 1354, "boost_clock": 1455, "architecture": "Pascal", "tier": "Entry"},
}


class GPUDetector:
    """Detects and retrieves information about installed GPUs."""
    
    def __init__(self):
        """Initialize the GPU detector."""
        self._initialized = False
        self._gpus: List[GPUInfo] = []
        
    def initialize(self) -> bool:
        """
        Initialize the GPU detection system.
        
        Returns:
            bool: True if initialization was successful.
        """
        if PYNVML_AVAILABLE:
            try:
                pynvml.nvmlInit()
                self._initialized = True
                return True
            except pynvml.NVMLError as e:
                print(f"Failed to initialize NVML: {e}")
                return False
        elif GPUTIL_AVAILABLE:
            self._initialized = True
            return True
        else:
            print("No GPU detection library available. Install pynvml or GPUtil.")
            return False
    
    def shutdown(self):
        """Clean up resources."""
        if PYNVML_AVAILABLE and self._initialized:
            try:
                pynvml.nvmlShutdown()
            except pynvml.NVMLError:
                pass
        self._initialized = False
    
    def detect_gpus(self) -> List[GPUInfo]:
        """
        Detect all available GPUs.
        
        Returns:
            List[GPUInfo]: List of detected GPU information.
        """
        if not self._initialized:
            self.initialize()
        
        self._gpus = []
        
        if PYNVML_AVAILABLE:
            self._detect_with_pynvml()
        elif GPUTIL_AVAILABLE:
            self._detect_with_gputil()
        else:
            # Fallback to basic detection
            self._detect_fallback()
        
        return self._gpus
    
    def _detect_with_pynvml(self):
        """Detect GPUs using pynvml."""
        try:
            device_count = pynvml.nvmlDeviceGetCount()
            driver_version = pynvml.nvmlSystemGetDriverVersion()
            
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                if isinstance(name, bytes):
                    name = name.decode('utf-8')
                
                # Get memory info
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                
                # Get utilization
                try:
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    gpu_usage = util.gpu
                    memory_usage = util.memory
                except pynvml.NVMLError:
                    gpu_usage = 0.0
                    memory_usage = 0.0
                
                # Get temperature
                try:
                    temperature = pynvml.nvmlDeviceGetTemperature(
                        handle, pynvml.NVML_TEMPERATURE_GPU
                    )
                except pynvml.NVMLError:
                    temperature = 0.0
                
                # Get power info
                try:
                    power_draw = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
                    power_limit = pynvml.nvmlDeviceGetPowerManagementLimit(handle) / 1000.0
                except pynvml.NVMLError:
                    power_draw = 0.0
                    power_limit = 0.0
                
                # Get UUID
                try:
                    uuid = pynvml.nvmlDeviceGetUUID(handle)
                    if isinstance(uuid, bytes):
                        uuid = uuid.decode('utf-8')
                except pynvml.NVMLError:
                    uuid = ""
                
                # Look up additional specs from database
                specs = self._lookup_gpu_specs(name)
                
                gpu_info = GPUInfo(
                    name=name,
                    vendor="NVIDIA",
                    vram_total=mem_info.total // (1024 * 1024),
                    vram_used=mem_info.used // (1024 * 1024),
                    vram_free=mem_info.free // (1024 * 1024),
                    cuda_cores=specs.get("cuda_cores", 0),
                    base_clock=specs.get("base_clock", 0),
                    boost_clock=specs.get("boost_clock", 0),
                    temperature=temperature,
                    gpu_usage=gpu_usage,
                    memory_usage=memory_usage,
                    power_draw=power_draw,
                    power_limit=power_limit,
                    driver_version=driver_version,
                    architecture=specs.get("architecture", "Unknown"),
                    tier=specs.get("tier", "Unknown"),
                    uuid=uuid,
                    index=i,
                )
                
                self._gpus.append(gpu_info)
                
        except pynvml.NVMLError as e:
            print(f"Error detecting GPUs with pynvml: {e}")
    
    def _detect_with_gputil(self):
        """Detect GPUs using GPUtil."""
        try:
            gpus = GPUtil.getGPUs()
            
            for i, gpu in enumerate(gpus):
                specs = self._lookup_gpu_specs(gpu.name)
                
                gpu_info = GPUInfo(
                    name=gpu.name,
                    vendor="NVIDIA",
                    vram_total=int(gpu.memoryTotal),
                    vram_used=int(gpu.memoryUsed),
                    vram_free=int(gpu.memoryFree),
                    cuda_cores=specs.get("cuda_cores", 0),
                    base_clock=specs.get("base_clock", 0),
                    boost_clock=specs.get("boost_clock", 0),
                    temperature=gpu.temperature,
                    gpu_usage=gpu.load * 100,
                    memory_usage=(gpu.memoryUsed / gpu.memoryTotal) * 100,
                    driver_version=gpu.driver,
                    architecture=specs.get("architecture", "Unknown"),
                    tier=specs.get("tier", "Unknown"),
                    uuid=gpu.uuid,
                    index=i,
                )
                
                self._gpus.append(gpu_info)
                
        except Exception as e:
            print(f"Error detecting GPUs with GPUtil: {e}")
    
    def _detect_fallback(self):
        """Fallback GPU detection using system commands."""
        system = platform.system()
        
        if system == "Linux":
            try:
                result = subprocess.run(
                    ["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
                     "--format=csv,noheader,nounits"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    for i, line in enumerate(result.stdout.strip().split('\n')):
                        parts = line.split(', ')
                        if len(parts) >= 3:
                            name = parts[0].strip()
                            specs = self._lookup_gpu_specs(name)
                            
                            gpu_info = GPUInfo(
                                name=name,
                                vendor="NVIDIA",
                                vram_total=int(float(parts[1])),
                                driver_version=parts[2].strip(),
                                cuda_cores=specs.get("cuda_cores", 0),
                                base_clock=specs.get("base_clock", 0),
                                boost_clock=specs.get("boost_clock", 0),
                                architecture=specs.get("architecture", "Unknown"),
                                tier=specs.get("tier", "Unknown"),
                                index=i,
                            )
                            self._gpus.append(gpu_info)
            except FileNotFoundError:
                pass
    
    def _lookup_gpu_specs(self, gpu_name: str) -> Dict[str, Any]:
        """
        Look up GPU specifications from the database.
        
        Args:
            gpu_name: Full GPU name string.
            
        Returns:
            Dictionary with GPU specifications.
        """
        # Normalize the name for matching
        gpu_name_upper = gpu_name.upper()
        
        for model_name, specs in GPU_SPECS_DATABASE.items():
            if model_name.upper() in gpu_name_upper:
                return specs
        
        return {}
    
    def get_primary_gpu(self) -> Optional[GPUInfo]:
        """
        Get the primary (first) GPU.
        
        Returns:
            GPUInfo for the primary GPU, or None if no GPU detected.
        """
        if not self._gpus:
            self.detect_gpus()
        
        return self._gpus[0] if self._gpus else None
    
    def refresh_gpu_status(self, gpu_index: int = 0) -> Optional[GPUInfo]:
        """
        Refresh the status of a specific GPU.
        
        Args:
            gpu_index: Index of the GPU to refresh.
            
        Returns:
            Updated GPUInfo or None.
        """
        self.detect_gpus()
        
        if gpu_index < len(self._gpus):
            return self._gpus[gpu_index]
        return None


def get_gpu_info() -> Optional[GPUInfo]:
    """
    Convenience function to get primary GPU info.
    
    Returns:
        GPUInfo for the primary GPU, or None if no GPU detected.
    """
    detector = GPUDetector()
    detector.initialize()
    gpu = detector.get_primary_gpu()
    detector.shutdown()
    return gpu


if __name__ == "__main__":
    # Test the detector
    detector = GPUDetector()
    if detector.initialize():
        gpus = detector.detect_gpus()
        for gpu in gpus:
            print(gpu.get_summary())
            print()
        detector.shutdown()
    else:
        print("Failed to initialize GPU detector")
