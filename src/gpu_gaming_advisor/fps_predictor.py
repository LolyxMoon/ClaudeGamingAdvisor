"""
FPS Prediction Module.

This module provides FPS prediction functionality based on
GPU specifications and game requirements.
"""

from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

from .gpu_detector import GPUInfo, GPU_SPECS_DATABASE
from .game_analyzer import GameAnalyzer


# Performance multipliers for different GPU tiers
# Base is normalized to RTX 3060 = 1.0
GPU_PERFORMANCE_INDEX: Dict[str, float] = {
    # RTX 40 Series
    "RTX 4090": 2.80,
    "RTX 4080 SUPER": 2.30,
    "RTX 4080": 2.15,
    "RTX 4070 TI SUPER": 1.95,
    "RTX 4070 TI": 1.80,
    "RTX 4070 SUPER": 1.65,
    "RTX 4070": 1.45,
    "RTX 4060 TI": 1.25,
    "RTX 4060": 1.10,
    
    # RTX 30 Series
    "RTX 3090 TI": 1.85,
    "RTX 3090": 1.75,
    "RTX 3080 TI": 1.70,
    "RTX 3080": 1.55,
    "RTX 3070 TI": 1.30,
    "RTX 3070": 1.20,
    "RTX 3060 TI": 1.10,
    "RTX 3060": 1.00,  # Baseline
    "RTX 3050": 0.70,
    
    # RTX 20 Series
    "RTX 2080 TI": 1.20,
    "RTX 2080 SUPER": 1.05,
    "RTX 2080": 0.95,
    "RTX 2070 SUPER": 0.90,
    "RTX 2070": 0.82,
    "RTX 2060 SUPER": 0.78,
    "RTX 2060": 0.70,
    
    # GTX 16 Series
    "GTX 1660 TI": 0.58,
    "GTX 1660 SUPER": 0.55,
    "GTX 1660": 0.50,
    "GTX 1650 SUPER": 0.45,
    "GTX 1650": 0.35,
    
    # GTX 10 Series
    "GTX 1080 TI": 0.85,
    "GTX 1080": 0.68,
    "GTX 1070 TI": 0.62,
    "GTX 1070": 0.55,
    "GTX 1060": 0.42,
    "GTX 1050 TI": 0.28,
    "GTX 1050": 0.22,
}

# Resolution multipliers (relative to 1080p)
RESOLUTION_MULTIPLIERS: Dict[str, float] = {
    "1280x720": 1.80,    # 720p
    "1600x900": 1.40,    # 900p
    "1920x1080": 1.00,   # 1080p (baseline)
    "2560x1080": 0.85,   # Ultrawide 1080p
    "2560x1440": 0.65,   # 1440p
    "3440x1440": 0.55,   # Ultrawide 1440p
    "3840x2160": 0.35,   # 4K
    "5120x2160": 0.28,   # Ultrawide 4K
}

# Quality preset multipliers
QUALITY_MULTIPLIERS: Dict[str, float] = {
    "low": 2.00,
    "medium": 1.40,
    "high": 1.00,
    "ultra": 0.70,
    "extreme": 0.50,
}

# Game-specific base FPS at 1080p High settings on RTX 3060
# These are reference values for the prediction model
GAME_BASE_FPS: Dict[str, int] = {
    "Cyberpunk 2077": 55,
    "Elden Ring": 58,
    "Red Dead Redemption 2": 52,
    "Hogwarts Legacy": 50,
    "God of War Ragnarok": 65,
    "Baldur's Gate 3": 60,
    "Starfield": 45,
    "Alan Wake 2": 40,
    "Call of Duty: Warzone": 95,
    "Fortnite": 120,
    "Counter-Strike 2": 180,
    "Valorant": 250,
    "The Witcher 3: Wild Hunt": 80,
    "GTA V": 100,
    "Minecraft": 150,
}


@dataclass
class FPSPrediction:
    """Data class for FPS predictions."""
    
    game_name: str
    gpu_name: str
    resolution: str
    quality_preset: str
    fps_min: int
    fps_max: int
    fps_average: int
    fps_1_percent_low: int
    confidence: str  # "high", "medium", "low"
    notes: list
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "game_name": self.game_name,
            "gpu_name": self.gpu_name,
            "resolution": self.resolution,
            "quality_preset": self.quality_preset,
            "fps_min": self.fps_min,
            "fps_max": self.fps_max,
            "fps_average": self.fps_average,
            "fps_1_percent_low": self.fps_1_percent_low,
            "confidence": self.confidence,
            "notes": self.notes,
        }


class FPSPredictor:
    """
    Predicts FPS performance based on GPU and game parameters.
    
    This class uses a combination of reference data and performance
    indices to estimate FPS for different configurations.
    """
    
    def __init__(self):
        """Initialize the FPS Predictor."""
        self.game_analyzer = GameAnalyzer()
    
    def _get_gpu_performance_index(self, gpu_name: str) -> float:
        """
        Get the performance index for a GPU.
        
        Args:
            gpu_name: GPU name string.
            
        Returns:
            Performance index (1.0 = RTX 3060 baseline).
        """
        gpu_name_upper = gpu_name.upper()
        
        for model_name, index in GPU_PERFORMANCE_INDEX.items():
            if model_name.upper() in gpu_name_upper:
                return index
        
        # Estimate based on VRAM if GPU not in database
        # This is a rough fallback
        return 0.50  # Conservative estimate
    
    def _get_resolution_multiplier(self, resolution: str) -> float:
        """Get the resolution multiplier."""
        return RESOLUTION_MULTIPLIERS.get(resolution, 1.0)
    
    def _get_quality_multiplier(self, quality: str) -> float:
        """Get the quality preset multiplier."""
        return QUALITY_MULTIPLIERS.get(quality.lower(), 1.0)
    
    def _get_game_base_fps(self, game_name: str) -> int:
        """Get the base FPS for a game."""
        # Try exact match
        if game_name in GAME_BASE_FPS:
            return GAME_BASE_FPS[game_name]
        
        # Try partial match
        for name, fps in GAME_BASE_FPS.items():
            if game_name.lower() in name.lower() or name.lower() in game_name.lower():
                return fps
        
        # Default for unknown games
        return 60
    
    def predict(
        self,
        gpu_info: GPUInfo,
        game_name: str,
        resolution: str = "1920x1080",
        quality_preset: str = "high"
    ) -> FPSPrediction:
        """
        Predict FPS for a specific configuration.
        
        Args:
            gpu_info: GPU information.
            game_name: Name of the game.
            resolution: Target resolution.
            quality_preset: Quality preset (low, medium, high, ultra, extreme).
            
        Returns:
            FPSPrediction with estimated performance.
        """
        # Get multipliers
        gpu_index = self._get_gpu_performance_index(gpu_info.name)
        res_multiplier = self._get_resolution_multiplier(resolution)
        quality_multiplier = self._get_quality_multiplier(quality_preset)
        base_fps = self._get_game_base_fps(game_name)
        
        # Calculate predicted FPS
        predicted_fps = base_fps * gpu_index * res_multiplier * quality_multiplier
        
        # Calculate FPS range (±15% for variance)
        fps_average = int(predicted_fps)
        fps_min = int(predicted_fps * 0.75)
        fps_max = int(predicted_fps * 1.15)
        fps_1_percent_low = int(predicted_fps * 0.60)
        
        # Determine confidence level
        gpu_in_db = any(
            model.upper() in gpu_info.name.upper()
            for model in GPU_PERFORMANCE_INDEX.keys()
        )
        game_in_db = game_name in GAME_BASE_FPS or any(
            game_name.lower() in name.lower()
            for name in GAME_BASE_FPS.keys()
        )
        
        if gpu_in_db and game_in_db:
            confidence = "high"
        elif gpu_in_db or game_in_db:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Generate notes
        notes = []
        
        # Check VRAM limitations
        game_req = self.game_analyzer.get_game_requirements(game_name)
        if game_req:
            if gpu_info.vram_total < game_req.recommended_vram:
                notes.append(
                    f"VRAM ({gpu_info.vram_total}MB) is below recommended "
                    f"({game_req.recommended_vram}MB). May experience stuttering."
                )
            
            if game_req.supports_dlss and "RTX" in gpu_info.name.upper():
                notes.append("DLSS available - can boost FPS by 30-60%")
            elif game_req.supports_fsr:
                notes.append("FSR available - can boost FPS by 20-40%")
        
        # Resolution-specific notes
        if resolution in ["3840x2160", "5120x2160"]:
            notes.append("4K gaming is very demanding. Consider DLSS/FSR for better performance.")
        
        # Quality-specific notes
        if quality_preset.lower() == "ultra" and fps_average < 60:
            notes.append("Consider reducing to High for smoother gameplay.")
        
        return FPSPrediction(
            game_name=game_name,
            gpu_name=gpu_info.name,
            resolution=resolution,
            quality_preset=quality_preset,
            fps_min=fps_min,
            fps_max=fps_max,
            fps_average=fps_average,
            fps_1_percent_low=fps_1_percent_low,
            confidence=confidence,
            notes=notes,
        )
    
    def predict_all_presets(
        self,
        gpu_info: GPUInfo,
        game_name: str,
        resolution: str = "1920x1080"
    ) -> Dict[str, FPSPrediction]:
        """
        Predict FPS for all quality presets.
        
        Args:
            gpu_info: GPU information.
            game_name: Name of the game.
            resolution: Target resolution.
            
        Returns:
            Dictionary mapping preset names to predictions.
        """
        presets = ["low", "medium", "high", "ultra"]
        return {
            preset: self.predict(gpu_info, game_name, resolution, preset)
            for preset in presets
        }
    
    def predict_all_resolutions(
        self,
        gpu_info: GPUInfo,
        game_name: str,
        quality_preset: str = "high"
    ) -> Dict[str, FPSPrediction]:
        """
        Predict FPS for all common resolutions.
        
        Args:
            gpu_info: GPU information.
            game_name: Name of the game.
            quality_preset: Quality preset.
            
        Returns:
            Dictionary mapping resolution to predictions.
        """
        resolutions = ["1920x1080", "2560x1440", "3840x2160"]
        return {
            res: self.predict(gpu_info, game_name, res, quality_preset)
            for res in resolutions
        }
    
    def find_optimal_settings(
        self,
        gpu_info: GPUInfo,
        game_name: str,
        target_fps: int = 60,
        prefer_quality: bool = True
    ) -> Dict[str, Any]:
        """
        Find optimal settings to achieve target FPS.
        
        Args:
            gpu_info: GPU information.
            game_name: Name of the game.
            target_fps: Target framerate.
            prefer_quality: If True, prefer higher quality at target FPS.
            
        Returns:
            Recommended settings configuration.
        """
        resolutions = ["3840x2160", "2560x1440", "1920x1080", "1280x720"]
        presets = ["ultra", "high", "medium", "low"]
        
        best_config = None
        
        # If preferring quality, start from highest settings
        if prefer_quality:
            for res in resolutions:
                for preset in presets:
                    prediction = self.predict(gpu_info, game_name, res, preset)
                    if prediction.fps_average >= target_fps:
                        if best_config is None:
                            best_config = {
                                "resolution": res,
                                "quality_preset": preset,
                                "prediction": prediction,
                            }
                        break
                if best_config:
                    break
        else:
            # Prefer performance - find settings that exceed target by most
            for res in reversed(resolutions):
                for preset in reversed(presets):
                    prediction = self.predict(gpu_info, game_name, res, preset)
                    if prediction.fps_average >= target_fps:
                        best_config = {
                            "resolution": res,
                            "quality_preset": preset,
                            "prediction": prediction,
                        }
        
        if best_config is None:
            # Can't reach target - return lowest settings
            prediction = self.predict(gpu_info, game_name, "1280x720", "low")
            best_config = {
                "resolution": "1280x720",
                "quality_preset": "low",
                "prediction": prediction,
                "warning": f"Cannot achieve {target_fps} FPS even at lowest settings"
            }
        
        return best_config
    
    def compare_gpus(
        self,
        gpu1_info: GPUInfo,
        gpu2_name: str,
        game_name: str,
        resolution: str = "1920x1080",
        quality_preset: str = "high"
    ) -> Dict[str, Any]:
        """
        Compare FPS predictions between two GPUs.
        
        Args:
            gpu1_info: First GPU (user's GPU) information.
            gpu2_name: Name of second GPU to compare.
            game_name: Name of the game.
            resolution: Target resolution.
            quality_preset: Quality preset.
            
        Returns:
            Comparison results.
        """
        pred1 = self.predict(gpu1_info, game_name, resolution, quality_preset)
        
        # Create a mock GPUInfo for GPU2
        gpu2_index = self._get_gpu_performance_index(gpu2_name)
        
        # Calculate GPU2 prediction manually
        base_fps = self._get_game_base_fps(game_name)
        res_multiplier = self._get_resolution_multiplier(resolution)
        quality_multiplier = self._get_quality_multiplier(quality_preset)
        gpu2_fps = int(base_fps * gpu2_index * res_multiplier * quality_multiplier)
        
        difference = gpu2_fps - pred1.fps_average
        percentage = (difference / pred1.fps_average * 100) if pred1.fps_average > 0 else 0
        
        return {
            "gpu1_name": gpu1_info.name,
            "gpu1_fps": pred1.fps_average,
            "gpu2_name": gpu2_name,
            "gpu2_fps": gpu2_fps,
            "fps_difference": difference,
            "percentage_difference": round(percentage, 1),
            "faster_gpu": gpu2_name if difference > 0 else gpu1_info.name,
            "game": game_name,
            "resolution": resolution,
            "quality": quality_preset,
        }
