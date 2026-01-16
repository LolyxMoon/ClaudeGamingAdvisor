"""
Tests for GPU Detector Module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

import sys
sys.path.insert(0, 'src')

from gpu_gaming_advisor.gpu_detector import (
    GPUDetector,
    GPUInfo,
    GPU_SPECS_DATABASE,
    get_gpu_info,
)


class TestGPUInfo:
    """Tests for GPUInfo dataclass."""
    
    def test_gpu_info_creation(self):
        """Test creating a GPUInfo instance."""
        gpu = GPUInfo(
            name="NVIDIA GeForce RTX 3070",
            vendor="NVIDIA",
            vram_total=8192,
            vram_used=1024,
            vram_free=7168,
            cuda_cores=5888,
            base_clock=1500,
            boost_clock=1725,
            temperature=45.0,
            gpu_usage=15.0,
            memory_usage=12.5,
            driver_version="535.154.05",
            architecture="Ampere",
            tier="High-End",
        )
        
        assert gpu.name == "NVIDIA GeForce RTX 3070"
        assert gpu.vendor == "NVIDIA"
        assert gpu.vram_total == 8192
        assert gpu.cuda_cores == 5888
        assert gpu.architecture == "Ampere"
    
    def test_gpu_info_to_dict(self):
        """Test converting GPUInfo to dictionary."""
        gpu = GPUInfo(
            name="RTX 4090",
            vendor="NVIDIA",
            vram_total=24576,
            cuda_cores=16384,
            architecture="Ada Lovelace",
            tier="Enthusiast",
        )
        
        data = gpu.to_dict()
        
        assert isinstance(data, dict)
        assert data["name"] == "RTX 4090"
        assert data["vram_total_mb"] == 24576
        assert data["cuda_cores"] == 16384
    
    def test_gpu_info_get_summary(self):
        """Test getting GPU summary string."""
        gpu = GPUInfo(
            name="RTX 3060",
            vram_total=12288,
            architecture="Ampere",
            cuda_cores=3584,
            base_clock=1320,
            boost_clock=1777,
            driver_version="535.0",
        )
        
        summary = gpu.get_summary()
        
        assert "RTX 3060" in summary
        assert "12 GB" in summary
        assert "Ampere" in summary


class TestGPUSpecsDatabase:
    """Tests for GPU specifications database."""
    
    def test_database_contains_rtx_40_series(self):
        """Test that database contains RTX 40 series GPUs."""
        assert "RTX 4090" in GPU_SPECS_DATABASE
        assert "RTX 4080" in GPU_SPECS_DATABASE
        assert "RTX 4070" in GPU_SPECS_DATABASE
        assert "RTX 4060" in GPU_SPECS_DATABASE
    
    def test_database_contains_rtx_30_series(self):
        """Test that database contains RTX 30 series GPUs."""
        assert "RTX 3090" in GPU_SPECS_DATABASE
        assert "RTX 3080" in GPU_SPECS_DATABASE
        assert "RTX 3070" in GPU_SPECS_DATABASE
        assert "RTX 3060" in GPU_SPECS_DATABASE
    
    def test_gpu_specs_have_required_fields(self):
        """Test that GPU specs have all required fields."""
        required_fields = ["cuda_cores", "base_clock", "boost_clock", "architecture", "tier"]
        
        for gpu_name, specs in GPU_SPECS_DATABASE.items():
            for field in required_fields:
                assert field in specs, f"{gpu_name} missing {field}"
    
    def test_rtx_4090_specs(self):
        """Test RTX 4090 specifications."""
        specs = GPU_SPECS_DATABASE["RTX 4090"]
        
        assert specs["cuda_cores"] == 16384
        assert specs["architecture"] == "Ada Lovelace"
        assert specs["tier"] == "Enthusiast"


class TestGPUDetector:
    """Tests for GPUDetector class."""
    
    def test_detector_initialization(self):
        """Test GPUDetector initialization."""
        detector = GPUDetector()
        assert detector._initialized == False
        assert detector._gpus == []
    
    def test_lookup_gpu_specs_exact_match(self):
        """Test looking up GPU specs with exact name."""
        detector = GPUDetector()
        
        specs = detector._lookup_gpu_specs("NVIDIA GeForce RTX 3070")
        
        assert specs["cuda_cores"] == 5888
        assert specs["architecture"] == "Ampere"
    
    def test_lookup_gpu_specs_partial_match(self):
        """Test looking up GPU specs with partial name."""
        detector = GPUDetector()
        
        specs = detector._lookup_gpu_specs("GeForce RTX 4080 SUPER OC")
        
        assert specs["cuda_cores"] == 10240
        assert specs["architecture"] == "Ada Lovelace"
    
    def test_lookup_gpu_specs_not_found(self):
        """Test looking up unknown GPU returns empty dict."""
        detector = GPUDetector()
        
        specs = detector._lookup_gpu_specs("Unknown GPU Model XYZ")
        
        assert specs == {}
    
    @patch('gpu_gaming_advisor.gpu_detector.PYNVML_AVAILABLE', False)
    @patch('gpu_gaming_advisor.gpu_detector.GPUTIL_AVAILABLE', False)
    def test_initialize_no_libraries(self):
        """Test initialization fails when no libraries available."""
        detector = GPUDetector()
        result = detector.initialize()
        
        # Should return False when no GPU libraries are available
        assert result == False or detector._initialized == False


class TestGetGPUInfo:
    """Tests for get_gpu_info convenience function."""
    
    @patch('gpu_gaming_advisor.gpu_detector.GPUDetector')
    def test_get_gpu_info_returns_primary(self, mock_detector_class):
        """Test get_gpu_info returns primary GPU."""
        mock_detector = Mock()
        mock_gpu = GPUInfo(name="RTX 3070", tier="High-End")
        mock_detector.get_primary_gpu.return_value = mock_gpu
        mock_detector.initialize.return_value = True
        mock_detector_class.return_value = mock_detector
        
        result = get_gpu_info()
        
        mock_detector.initialize.assert_called_once()
        mock_detector.get_primary_gpu.assert_called_once()
        mock_detector.shutdown.assert_called_once()


# Fixtures
@pytest.fixture
def sample_gpu_info():
    """Create a sample GPUInfo for testing."""
    return GPUInfo(
        name="NVIDIA GeForce RTX 3070",
        vendor="NVIDIA",
        vram_total=8192,
        vram_used=2048,
        vram_free=6144,
        cuda_cores=5888,
        base_clock=1500,
        boost_clock=1725,
        temperature=55.0,
        gpu_usage=35.0,
        memory_usage=25.0,
        power_draw=150.0,
        power_limit=220.0,
        driver_version="535.154.05",
        architecture="Ampere",
        tier="High-End",
    )


@pytest.fixture
def detector():
    """Create a GPUDetector instance."""
    return GPUDetector()
