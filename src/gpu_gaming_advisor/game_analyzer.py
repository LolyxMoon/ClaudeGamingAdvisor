"""
Game Analyzer Module.

This module provides game analysis functionality including
requirements checking and compatibility assessment.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .gpu_detector import GPUInfo


@dataclass
class GameRequirements:
    """Data class for game requirements."""
    
    name: str
    minimum_vram: int  # MB
    recommended_vram: int  # MB
    minimum_gpu: str
    recommended_gpu: str
    supports_raytracing: bool
    supports_dlss: bool
    supports_fsr: bool
    release_year: int
    engine: str
    optimization_level: str  # "excellent", "good", "average", "poor"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "minimum_vram_mb": self.minimum_vram,
            "recommended_vram_mb": self.recommended_vram,
            "minimum_gpu": self.minimum_gpu,
            "recommended_gpu": self.recommended_gpu,
            "supports_raytracing": self.supports_raytracing,
            "supports_dlss": self.supports_dlss,
            "supports_fsr": self.supports_fsr,
            "release_year": self.release_year,
            "engine": self.engine,
            "optimization_level": self.optimization_level,
        }


# Built-in games database
GAMES_DATABASE: Dict[str, Dict[str, Any]] = {
    "Cyberpunk 2077": {
        "minimum_vram": 3072,
        "recommended_vram": 8192,
        "minimum_gpu": "GTX 970",
        "recommended_gpu": "RTX 2060",
        "supports_raytracing": True,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2020,
        "engine": "REDengine 4",
        "optimization_level": "good",
        "settings": [
            "Quality Preset", "Ray Tracing", "DLSS", "FSR", "Crowd Density",
            "Shadow Quality", "Reflection Quality", "Ambient Occlusion",
            "Screen Space Reflections", "Volumetric Fog", "Cascaded Shadows"
        ]
    },
    "Elden Ring": {
        "minimum_vram": 3072,
        "recommended_vram": 8192,
        "minimum_gpu": "GTX 1060",
        "recommended_gpu": "RTX 3060",
        "supports_raytracing": True,
        "supports_dlss": False,
        "supports_fsr": False,
        "release_year": 2022,
        "engine": "FromSoftware Engine",
        "optimization_level": "average",
        "settings": [
            "Quality Preset", "Texture Quality", "Antialiasing Quality",
            "SSAO", "Depth of Field", "Motion Blur", "Shadow Quality",
            "Lighting Quality", "Effects Quality", "Volumetric Quality",
            "Reflection Quality", "Water Surface Quality", "Shader Quality",
            "Global Illumination Quality", "Grass Quality"
        ]
    },
    "Red Dead Redemption 2": {
        "minimum_vram": 2048,
        "recommended_vram": 8192,
        "minimum_gpu": "GTX 770",
        "recommended_gpu": "RTX 2070",
        "supports_raytracing": False,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2019,
        "engine": "RAGE",
        "optimization_level": "good",
        "settings": [
            "Quality Preset", "Texture Quality", "Anisotropic Filtering",
            "Lighting Quality", "Global Illumination Quality", "Shadow Quality",
            "Far Shadow Quality", "Screen Space Ambient Occlusion",
            "Reflection Quality", "Mirror Quality", "Water Quality",
            "Volumetrics Quality", "Particle Quality", "Tessellation Quality",
            "TAA", "FXAA", "MSAA"
        ]
    },
    "Hogwarts Legacy": {
        "minimum_vram": 4096,
        "recommended_vram": 8192,
        "minimum_gpu": "GTX 960",
        "recommended_gpu": "RTX 3070",
        "supports_raytracing": True,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2023,
        "engine": "Unreal Engine 4",
        "optimization_level": "average",
        "settings": [
            "Quality Preset", "Ray Tracing Reflections", "Ray Tracing Shadows",
            "Ray Tracing Ambient Occlusion", "DLSS", "FSR", "Effects Quality",
            "Material Quality", "Fog Quality", "Sky Quality", "Foliage Quality",
            "Post Process Quality", "Shadow Quality", "Texture Quality",
            "View Distance Quality", "Population Quality"
        ]
    },
    "God of War Ragnarok": {
        "minimum_vram": 4096,
        "recommended_vram": 8192,
        "minimum_gpu": "GTX 1070",
        "recommended_gpu": "RTX 3070",
        "supports_raytracing": False,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2024,
        "engine": "Santa Monica Studio Engine",
        "optimization_level": "excellent",
        "settings": [
            "Graphics Preset", "Texture Quality", "Model Quality",
            "Anisotropic Filter", "Shadows", "Reflections", "Atmospherics",
            "Ambient Occlusion", "DLSS", "FSR"
        ]
    },
    "Baldur's Gate 3": {
        "minimum_vram": 4096,
        "recommended_vram": 8192,
        "minimum_gpu": "GTX 970",
        "recommended_gpu": "RTX 3060",
        "supports_raytracing": False,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2023,
        "engine": "Divinity Engine 4.0",
        "optimization_level": "good",
        "settings": [
            "Overall Preset", "Model Quality", "Detail Distance",
            "Instance Distance", "Texture Quality", "Texture Filtering",
            "Animation LOD Distance", "Slow HDD Mode", "Shadow Quality",
            "Cloud Quality", "Fog Quality", "God Rays", "Bloom", "Depth of Field",
            "DLSS", "FSR", "Antialiasing"
        ]
    },
    "Starfield": {
        "minimum_vram": 6144,
        "recommended_vram": 8192,
        "minimum_gpu": "GTX 1070 Ti",
        "recommended_gpu": "RTX 2080",
        "supports_raytracing": False,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2023,
        "engine": "Creation Engine 2",
        "optimization_level": "poor",
        "settings": [
            "Render Resolution Scale", "Shadow Quality", "Indirect Lighting",
            "Reflections", "Particle Quality", "Volumetric Lighting",
            "Crowd Density", "Motion Blur", "GTAO", "Grass Quality",
            "Contact Shadows", "VSync", "Upscaling", "Film Grain",
            "Enable VRS"
        ]
    },
    "Alan Wake 2": {
        "minimum_vram": 6144,
        "recommended_vram": 16384,
        "minimum_gpu": "RTX 2060",
        "recommended_gpu": "RTX 4070",
        "supports_raytracing": True,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2023,
        "engine": "Northlight Engine",
        "optimization_level": "average",
        "settings": [
            "Quality Preset", "Texture Resolution", "Shadow Resolution",
            "Global Reflections", "Volumetric Lighting", "Fog Quality",
            "Global Illumination", "Post Process", "Ray Traced Reflections",
            "DLSS", "FSR", "XeSS"
        ]
    },
    "Call of Duty: Warzone": {
        "minimum_vram": 4096,
        "recommended_vram": 8192,
        "minimum_gpu": "GTX 970",
        "recommended_gpu": "RTX 3060",
        "supports_raytracing": True,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2020,
        "engine": "IW Engine",
        "optimization_level": "good",
        "settings": [
            "Render Resolution", "Dynamic Resolution", "Upscaling",
            "VRAM Scale Target", "Texture Resolution", "Texture Filter",
            "Nearby LOD", "Distant LOD", "Clutter Draw Distance",
            "Particle Quality", "Bullet Impacts", "Shader Quality",
            "Tessellation", "On-Demand Texture Streaming", "Shadow Quality",
            "Screen Space Shadows", "Ambient Occlusion", "Screen Space Reflections",
            "Static Reflection Quality", "Weather Grid Volumes", "Water Quality"
        ]
    },
    "Fortnite": {
        "minimum_vram": 2048,
        "recommended_vram": 4096,
        "minimum_gpu": "GTX 660",
        "recommended_gpu": "RTX 2060",
        "supports_raytracing": True,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2017,
        "engine": "Unreal Engine 5",
        "optimization_level": "excellent",
        "settings": [
            "Quality Preset", "3D Resolution", "View Distance", "Shadows",
            "Anti-Aliasing", "Textures", "Effects", "Post Processing",
            "Ray Tracing", "DLSS", "FSR"
        ]
    },
    "Counter-Strike 2": {
        "minimum_vram": 1024,
        "recommended_vram": 4096,
        "minimum_gpu": "GTX 650",
        "recommended_gpu": "RTX 2060",
        "supports_raytracing": False,
        "supports_dlss": False,
        "supports_fsr": False,
        "release_year": 2023,
        "engine": "Source 2",
        "optimization_level": "excellent",
        "settings": [
            "Global Shadow Quality", "Model/Texture Detail", "Texture Filtering",
            "Shader Detail", "Particle Detail", "Ambient Occlusion",
            "High Dynamic Range", "FidelityFX Super Resolution", "NVIDIA Reflex"
        ]
    },
    "Valorant": {
        "minimum_vram": 1024,
        "recommended_vram": 4096,
        "minimum_gpu": "GT 730",
        "recommended_gpu": "GTX 1050 Ti",
        "supports_raytracing": False,
        "supports_dlss": False,
        "supports_fsr": False,
        "release_year": 2020,
        "engine": "Unreal Engine 4",
        "optimization_level": "excellent",
        "settings": [
            "Material Quality", "Texture Quality", "Detail Quality",
            "UI Quality", "Vignette", "VSync", "Anti-Aliasing",
            "Anisotropic Filtering", "Improve Clarity", "Bloom",
            "Distortion", "Cast Shadows"
        ]
    },
    "The Witcher 3: Wild Hunt": {
        "minimum_vram": 2048,
        "recommended_vram": 8192,
        "minimum_gpu": "GTX 660",
        "recommended_gpu": "RTX 3070",
        "supports_raytracing": True,
        "supports_dlss": True,
        "supports_fsr": True,
        "release_year": 2015,
        "engine": "REDengine 3",
        "optimization_level": "excellent",
        "settings": [
            "Graphics Preset", "Post Processing", "Motion Blur",
            "Blur", "Anti-Aliasing", "Bloom", "Sharpening", "Ambient Occlusion",
            "Depth of Field", "Chromatic Aberration", "Vignetting",
            "Light Shafts", "Detail Level", "Shadow Quality", "Terrain Quality",
            "Water Quality", "Foliage Visibility Range", "Grass Density",
            "Texture Quality", "Number of Background Characters",
            "Ray Tracing", "DLSS"
        ]
    },
    "GTA V": {
        "minimum_vram": 1024,
        "recommended_vram": 4096,
        "minimum_gpu": "GTX 660",
        "recommended_gpu": "GTX 1060",
        "supports_raytracing": False,
        "supports_dlss": False,
        "supports_fsr": False,
        "release_year": 2015,
        "engine": "RAGE",
        "optimization_level": "excellent",
        "settings": [
            "FXAA", "MSAA", "TXAA", "Population Density", "Population Variety",
            "Distance Scaling", "Texture Quality", "Shader Quality",
            "Shadow Quality", "Reflection Quality", "Reflection MSAA",
            "Water Quality", "Particles Quality", "Grass Quality",
            "Post FX", "Anisotropic Filtering", "Ambient Occlusion",
            "Tessellation", "Long Shadows", "High Resolution Shadows",
            "High Detail Streaming While Flying", "Extended Distance Scaling",
            "Extended Shadows Distance"
        ]
    },
    "Minecraft": {
        "minimum_vram": 512,
        "recommended_vram": 4096,
        "minimum_gpu": "Intel HD 4000",
        "recommended_gpu": "RTX 2060",
        "supports_raytracing": True,
        "supports_dlss": True,
        "supports_fsr": False,
        "release_year": 2011,
        "engine": "Java/Bedrock Engine",
        "optimization_level": "average",
        "settings": [
            "Graphics", "Render Distance", "Simulation Distance",
            "Max Framerate", "View Bobbing", "GUI Scale", "Brightness",
            "Clouds", "Particles", "Smooth Lighting", "Biome Blend",
            "Entity Shadows", "Entity Distance", "FOV Effects", "Darkness Pulsing",
            "Ray Tracing"
        ]
    },
}


class GameAnalyzer:
    """
    Analyzes games and their requirements.
    
    This class provides functionality to check game compatibility,
    retrieve requirements, and analyze performance expectations.
    """
    
    def __init__(self, custom_database_path: Optional[str] = None):
        """
        Initialize the Game Analyzer.
        
        Args:
            custom_database_path: Optional path to a custom games database JSON file.
        """
        self.games_db = GAMES_DATABASE.copy()
        
        if custom_database_path:
            self._load_custom_database(custom_database_path)
    
    def _load_custom_database(self, path: str):
        """Load a custom games database from JSON file."""
        try:
            with open(path, 'r') as f:
                custom_db = json.load(f)
                self.games_db.update(custom_db)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load custom database: {e}")
    
    def get_game_requirements(self, game_name: str) -> Optional[GameRequirements]:
        """
        Get requirements for a specific game.
        
        Args:
            game_name: Name of the game.
            
        Returns:
            GameRequirements if found, None otherwise.
        """
        # Try exact match first
        game_data = self.games_db.get(game_name)
        
        # Try case-insensitive match
        if not game_data:
            for name, data in self.games_db.items():
                if name.lower() == game_name.lower():
                    game_data = data
                    game_name = name
                    break
        
        # Try partial match
        if not game_data:
            for name, data in self.games_db.items():
                if game_name.lower() in name.lower():
                    game_data = data
                    game_name = name
                    break
        
        if not game_data:
            return None
        
        return GameRequirements(
            name=game_name,
            minimum_vram=game_data.get("minimum_vram", 0),
            recommended_vram=game_data.get("recommended_vram", 0),
            minimum_gpu=game_data.get("minimum_gpu", "Unknown"),
            recommended_gpu=game_data.get("recommended_gpu", "Unknown"),
            supports_raytracing=game_data.get("supports_raytracing", False),
            supports_dlss=game_data.get("supports_dlss", False),
            supports_fsr=game_data.get("supports_fsr", False),
            release_year=game_data.get("release_year", 0),
            engine=game_data.get("engine", "Unknown"),
            optimization_level=game_data.get("optimization_level", "unknown"),
        )
    
    def check_compatibility(self, gpu_info: GPUInfo, game_name: str) -> Dict[str, Any]:
        """
        Check if a GPU is compatible with a game.
        
        Args:
            gpu_info: GPU information.
            game_name: Name of the game.
            
        Returns:
            Compatibility analysis results.
        """
        requirements = self.get_game_requirements(game_name)
        
        if not requirements:
            return {
                "game_name": game_name,
                "compatible": "unknown",
                "message": f"Game '{game_name}' not found in database",
                "suggestions": self.search_games(game_name)[:5]
            }
        
        vram_mb = gpu_info.vram_total
        
        # Determine compatibility level
        if vram_mb >= requirements.recommended_vram:
            compatibility = "excellent"
            message = "Your GPU exceeds the recommended requirements"
        elif vram_mb >= requirements.minimum_vram:
            compatibility = "good"
            message = "Your GPU meets minimum requirements but is below recommended"
        else:
            compatibility = "poor"
            message = "Your GPU does not meet minimum VRAM requirements"
        
        # Check feature support
        features = []
        if requirements.supports_raytracing:
            if "RTX" in gpu_info.name.upper():
                features.append("Ray Tracing supported ✓")
            else:
                features.append("Ray Tracing not supported on your GPU")
        
        if requirements.supports_dlss:
            if "RTX" in gpu_info.name.upper():
                features.append("DLSS supported ✓")
            else:
                features.append("DLSS not supported on your GPU")
        
        if requirements.supports_fsr:
            features.append("FSR supported ✓ (all GPUs)")
        
        return {
            "game_name": game_name,
            "compatible": compatibility,
            "message": message,
            "your_vram_mb": vram_mb,
            "minimum_vram_mb": requirements.minimum_vram,
            "recommended_vram_mb": requirements.recommended_vram,
            "minimum_gpu": requirements.minimum_gpu,
            "recommended_gpu": requirements.recommended_gpu,
            "engine": requirements.engine,
            "optimization_level": requirements.optimization_level,
            "features": features,
        }
    
    def list_games(self) -> List[str]:
        """Get list of all supported games."""
        return sorted(self.games_db.keys())
    
    def search_games(self, query: str) -> List[str]:
        """
        Search for games by name.
        
        Args:
            query: Search query.
            
        Returns:
            List of matching game names.
        """
        query_lower = query.lower()
        matches = []
        
        for game_name in self.games_db.keys():
            if query_lower in game_name.lower():
                matches.append(game_name)
        
        return sorted(matches)
    
    def get_game_settings(self, game_name: str) -> List[str]:
        """
        Get list of available settings for a game.
        
        Args:
            game_name: Name of the game.
            
        Returns:
            List of setting names.
        """
        game_data = self.games_db.get(game_name)
        
        if not game_data:
            for name, data in self.games_db.items():
                if game_name.lower() in name.lower():
                    game_data = data
                    break
        
        if game_data:
            return game_data.get("settings", [])
        
        return []
    
    def get_games_by_feature(self, feature: str) -> List[str]:
        """
        Get games that support a specific feature.
        
        Args:
            feature: Feature name ("raytracing", "dlss", "fsr").
            
        Returns:
            List of game names.
        """
        feature_map = {
            "raytracing": "supports_raytracing",
            "ray_tracing": "supports_raytracing",
            "rt": "supports_raytracing",
            "dlss": "supports_dlss",
            "fsr": "supports_fsr",
        }
        
        feature_key = feature_map.get(feature.lower())
        if not feature_key:
            return []
        
        return [
            name for name, data in self.games_db.items()
            if data.get(feature_key, False)
        ]
    
    def export_database(self, path: str):
        """Export the games database to a JSON file."""
        with open(path, 'w') as f:
            json.dump(self.games_db, f, indent=2)
    
    def add_game(self, name: str, requirements: Dict[str, Any]):
        """Add or update a game in the database."""
        self.games_db[name] = requirements
