"""
Tests for FPS Predictor Module.
"""

import pytest

import sys
sys.path.insert(0, 'src')

from gpu_gaming_advisor.fps_predictor import (
    FPSPredictor,
    FPSPrediction,
    GPU_PERFORMANCE_INDEX,
    RESOLUTION_MULTIPLIERS,
    QUALITY_MULTIPLIERS,
    GAME_BASE_FPS,
)
from gpu_gaming_advisor.gpu_detector import GPUInfo


class TestFPSPrediction:
    """Tests for FPSPrediction dataclass."""
    
    def test_prediction_creation(self):
        """Test creating an FPSPrediction instance."""
        pred = FPSPrediction(
            game_name="Cyberpunk 2077",
            gpu_name="RTX 3070",
            resolution="1920x1080",
            quality_preset="high",
            fps_min=50,
            fps_max=70,
            fps_average=60,
            fps_1_percent_low=45,
            confidence="high",
            notes=["DLSS recommended"],
        )
        
        assert pred.fps_average == 60
        assert pred.confidence == "high"
    
    def test_prediction_to_dict(self):
        """Test converting prediction to dictionary."""
        pred = FPSPrediction(
            game_name="Fortnite",
            gpu_name="RTX 4060",
            resolution="1920x1080",
            quality_preset="ultra",
            fps_min=80,
            fps_max=120,
            fps_average=100,
            fps_1_percent_low=70,
            confidence="high",
            notes=[],
        )
        
        data = pred.to_dict()
        
        assert isinstance(data, dict)
        assert data["fps_average"] == 100
        assert data["game_name"] == "Fortnite"


class TestPerformanceIndices:
    """Tests for performance index data."""
    
    def test_gpu_performance_index_not_empty(self):
        """Test that GPU performance index has entries."""
        assert len(GPU_PERFORMANCE_INDEX) > 0
    
    def test_rtx_3060_is_baseline(self):
        """Test that RTX 3060 is the baseline (1.0)."""
        assert GPU_PERFORMANCE_INDEX["RTX 3060"] == 1.0
    
    def test_higher_gpus_have_higher_index(self):
        """Test that higher-end GPUs have higher indices."""
        assert GPU_PERFORMANCE_INDEX["RTX 4090"] > GPU_PERFORMANCE_INDEX["RTX 4080"]
        assert GPU_PERFORMANCE_INDEX["RTX 4080"] > GPU_PERFORMANCE_INDEX["RTX 4070"]
        assert GPU_PERFORMANCE_INDEX["RTX 3080"] > GPU_PERFORMANCE_INDEX["RTX 3070"]
    
    def test_resolution_multipliers(self):
        """Test resolution multipliers make sense."""
        assert RESOLUTION_MULTIPLIERS["1280x720"] > RESOLUTION_MULTIPLIERS["1920x1080"]
        assert RESOLUTION_MULTIPLIERS["1920x1080"] > RESOLUTION_MULTIPLIERS["2560x1440"]
        assert RESOLUTION_MULTIPLIERS["2560x1440"] > RESOLUTION_MULTIPLIERS["3840x2160"]
    
    def test_quality_multipliers(self):
        """Test quality multipliers make sense."""
        assert QUALITY_MULTIPLIERS["low"] > QUALITY_MULTIPLIERS["medium"]
        assert QUALITY_MULTIPLIERS["medium"] > QUALITY_MULTIPLIERS["high"]
        assert QUALITY_MULTIPLIERS["high"] > QUALITY_MULTIPLIERS["ultra"]


class TestFPSPredictor:
    """Tests for FPSPredictor class."""
    
    @pytest.fixture
    def predictor(self):
        """Create an FPSPredictor instance."""
        return FPSPredictor()
    
    @pytest.fixture
    def rtx_3070(self):
        """Create an RTX 3070 GPU for testing."""
        return GPUInfo(
            name="NVIDIA GeForce RTX 3070",
            vram_total=8192,
            architecture="Ampere",
            tier="High-End",
        )
    
    @pytest.fixture
    def rtx_4090(self):
        """Create an RTX 4090 GPU for testing."""
        return GPUInfo(
            name="NVIDIA GeForce RTX 4090",
            vram_total=24576,
            architecture="Ada Lovelace",
            tier="Enthusiast",
        )
    
    @pytest.fixture
    def gtx_1060(self):
        """Create a GTX 1060 GPU for testing."""
        return GPUInfo(
            name="NVIDIA GeForce GTX 1060",
            vram_total=6144,
            architecture="Pascal",
            tier="Entry",
        )
    
    def test_get_gpu_performance_index_exact(self, predictor):
        """Test getting performance index for known GPU."""
        index = predictor._get_gpu_performance_index("NVIDIA GeForce RTX 3070")
        assert index == 1.20
    
    def test_get_gpu_performance_index_unknown(self, predictor):
        """Test getting performance index for unknown GPU."""
        index = predictor._get_gpu_performance_index("Unknown GPU XYZ")
        assert index == 0.50  # Conservative fallback
    
    def test_predict_basic(self, predictor, rtx_3070):
        """Test basic FPS prediction."""
        prediction = predictor.predict(
            rtx_3070,
            "Cyberpunk 2077",
            "1920x1080",
            "high",
        )
        
        assert isinstance(prediction, FPSPrediction)
        assert prediction.fps_average > 0
        assert prediction.fps_min <= prediction.fps_average <= prediction.fps_max
    
    def test_predict_higher_gpu_higher_fps(self, predictor, rtx_3070, rtx_4090):
        """Test that higher-end GPUs predict higher FPS."""
        pred_3070 = predictor.predict(rtx_3070, "Cyberpunk 2077", "1920x1080", "high")
        pred_4090 = predictor.predict(rtx_4090, "Cyberpunk 2077", "1920x1080", "high")
        
        assert pred_4090.fps_average > pred_3070.fps_average
    
    def test_predict_lower_resolution_higher_fps(self, predictor, rtx_3070):
        """Test that lower resolution predicts higher FPS."""
        pred_1080p = predictor.predict(rtx_3070, "Cyberpunk 2077", "1920x1080", "high")
        pred_1440p = predictor.predict(rtx_3070, "Cyberpunk 2077", "2560x1440", "high")
        pred_4k = predictor.predict(rtx_3070, "Cyberpunk 2077", "3840x2160", "high")
        
        assert pred_1080p.fps_average > pred_1440p.fps_average > pred_4k.fps_average
    
    def test_predict_lower_quality_higher_fps(self, predictor, rtx_3070):
        """Test that lower quality predicts higher FPS."""
        pred_low = predictor.predict(rtx_3070, "Cyberpunk 2077", "1920x1080", "low")
        pred_medium = predictor.predict(rtx_3070, "Cyberpunk 2077", "1920x1080", "medium")
        pred_high = predictor.predict(rtx_3070, "Cyberpunk 2077", "1920x1080", "high")
        pred_ultra = predictor.predict(rtx_3070, "Cyberpunk 2077", "1920x1080", "ultra")
        
        assert pred_low.fps_average > pred_medium.fps_average
        assert pred_medium.fps_average > pred_high.fps_average
        assert pred_high.fps_average > pred_ultra.fps_average
    
    def test_predict_confidence_levels(self, predictor, rtx_3070):
        """Test confidence levels for known vs unknown games."""
        # Known game and GPU should have high confidence
        pred_known = predictor.predict(rtx_3070, "Cyberpunk 2077", "1920x1080", "high")
        assert pred_known.confidence == "high"
        
        # Unknown game should have lower confidence
        pred_unknown = predictor.predict(rtx_3070, "Unknown Game 2099", "1920x1080", "high")
        assert pred_unknown.confidence in ["medium", "low"]
    
    def test_predict_all_presets(self, predictor, rtx_3070):
        """Test predicting for all quality presets."""
        predictions = predictor.predict_all_presets(rtx_3070, "Fortnite", "1920x1080")
        
        assert "low" in predictions
        assert "medium" in predictions
        assert "high" in predictions
        assert "ultra" in predictions
        
        assert predictions["low"].fps_average > predictions["ultra"].fps_average
    
    def test_predict_all_resolutions(self, predictor, rtx_3070):
        """Test predicting for all resolutions."""
        predictions = predictor.predict_all_resolutions(rtx_3070, "Fortnite", "high")
        
        assert "1920x1080" in predictions
        assert "2560x1440" in predictions
        assert "3840x2160" in predictions
        
        assert predictions["1920x1080"].fps_average > predictions["3840x2160"].fps_average
    
    def test_find_optimal_settings_quality_priority(self, predictor, rtx_3070):
        """Test finding optimal settings with quality priority."""
        result = predictor.find_optimal_settings(
            rtx_3070,
            "Fortnite",
            target_fps=60,
            prefer_quality=True,
        )
        
        assert "resolution" in result
        assert "quality_preset" in result
        assert "prediction" in result
        assert result["prediction"].fps_average >= 60
    
    def test_find_optimal_settings_performance_priority(self, predictor, rtx_3070):
        """Test finding optimal settings with performance priority."""
        result = predictor.find_optimal_settings(
            rtx_3070,
            "Fortnite",
            target_fps=60,
            prefer_quality=False,
        )
        
        assert "resolution" in result
        assert result["prediction"].fps_average >= 60
    
    def test_find_optimal_settings_impossible_target(self, predictor, gtx_1060):
        """Test finding optimal settings with impossible target."""
        # Try to get 240 FPS in demanding game with low-end GPU
        result = predictor.find_optimal_settings(
            gtx_1060,
            "Cyberpunk 2077",
            target_fps=240,
            prefer_quality=True,
        )
        
        # Should return lowest settings with warning
        assert result["resolution"] == "1280x720"
        assert result["quality_preset"] == "low"
        assert "warning" in result
    
    def test_compare_gpus(self, predictor, rtx_3070):
        """Test comparing GPUs."""
        comparison = predictor.compare_gpus(
            rtx_3070,
            "RTX 4070",
            "Cyberpunk 2077",
            "1920x1080",
            "high",
        )
        
        assert "gpu1_name" in comparison
        assert "gpu2_name" in comparison
        assert "fps_difference" in comparison
        assert "percentage_difference" in comparison
        assert "faster_gpu" in comparison
    
    def test_compare_gpus_4090_faster(self, predictor, rtx_3070):
        """Test that RTX 4090 is predicted faster than RTX 3070."""
        comparison = predictor.compare_gpus(
            rtx_3070,
            "RTX 4090",
            "Cyberpunk 2077",
        )
        
        assert comparison["faster_gpu"] == "RTX 4090"
        assert comparison["percentage_difference"] > 0
    
    def test_vram_warning_in_notes(self, predictor):
        """Test that VRAM warnings appear in notes."""
        low_vram_gpu = GPUInfo(
            name="GTX 1650",
            vram_total=4096,  # 4GB
        )
        
        # Alan Wake 2 recommends 16GB
        prediction = predictor.predict(
            low_vram_gpu,
            "Alan Wake 2",
            "1920x1080",
            "high",
        )
        
        # Should have a VRAM warning note
        vram_warning = any("VRAM" in note for note in prediction.notes)
        assert vram_warning or prediction.confidence == "low"
