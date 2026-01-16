"""
Tests for Game Analyzer Module.
"""

import pytest
from unittest.mock import Mock, patch
import tempfile
import json
import os

import sys
sys.path.insert(0, 'src')

from gpu_gaming_advisor.game_analyzer import (
    GameAnalyzer,
    GameRequirements,
    GAMES_DATABASE,
)
from gpu_gaming_advisor.gpu_detector import GPUInfo


class TestGameRequirements:
    """Tests for GameRequirements dataclass."""
    
    def test_game_requirements_creation(self):
        """Test creating a GameRequirements instance."""
        req = GameRequirements(
            name="Cyberpunk 2077",
            minimum_vram=3072,
            recommended_vram=8192,
            minimum_gpu="GTX 970",
            recommended_gpu="RTX 2060",
            supports_raytracing=True,
            supports_dlss=True,
            supports_fsr=True,
            release_year=2020,
            engine="REDengine 4",
            optimization_level="good",
        )
        
        assert req.name == "Cyberpunk 2077"
        assert req.minimum_vram == 3072
        assert req.supports_raytracing == True
        assert req.supports_dlss == True
    
    def test_game_requirements_to_dict(self):
        """Test converting GameRequirements to dictionary."""
        req = GameRequirements(
            name="Elden Ring",
            minimum_vram=3072,
            recommended_vram=8192,
            minimum_gpu="GTX 1060",
            recommended_gpu="RTX 3060",
            supports_raytracing=True,
            supports_dlss=False,
            supports_fsr=False,
            release_year=2022,
            engine="FromSoftware Engine",
            optimization_level="average",
        )
        
        data = req.to_dict()
        
        assert isinstance(data, dict)
        assert data["name"] == "Elden Ring"
        assert data["minimum_vram_mb"] == 3072
        assert data["supports_raytracing"] == True


class TestGamesDatabase:
    """Tests for the built-in games database."""
    
    def test_database_not_empty(self):
        """Test that the games database is not empty."""
        assert len(GAMES_DATABASE) > 0
    
    def test_database_contains_popular_games(self):
        """Test that database contains popular games."""
        popular_games = [
            "Cyberpunk 2077",
            "Elden Ring",
            "Fortnite",
            "Counter-Strike 2",
            "GTA V",
        ]
        
        for game in popular_games:
            assert game in GAMES_DATABASE, f"Missing popular game: {game}"
    
    def test_game_entries_have_required_fields(self):
        """Test that all game entries have required fields."""
        required_fields = [
            "minimum_vram",
            "recommended_vram",
            "minimum_gpu",
            "recommended_gpu",
            "supports_raytracing",
            "supports_dlss",
            "supports_fsr",
            "release_year",
            "engine",
            "optimization_level",
        ]
        
        for game_name, game_data in GAMES_DATABASE.items():
            for field in required_fields:
                assert field in game_data, f"{game_name} missing field: {field}"


class TestGameAnalyzer:
    """Tests for GameAnalyzer class."""
    
    @pytest.fixture
    def analyzer(self):
        """Create a GameAnalyzer instance."""
        return GameAnalyzer()
    
    @pytest.fixture
    def sample_gpu(self):
        """Create a sample GPU for testing."""
        return GPUInfo(
            name="NVIDIA GeForce RTX 3070",
            vendor="NVIDIA",
            vram_total=8192,
            vram_used=1024,
            vram_free=7168,
            cuda_cores=5888,
            architecture="Ampere",
            tier="High-End",
        )
    
    def test_get_game_requirements_exact_match(self, analyzer):
        """Test getting requirements with exact game name."""
        req = analyzer.get_game_requirements("Cyberpunk 2077")
        
        assert req is not None
        assert req.name == "Cyberpunk 2077"
        assert req.supports_raytracing == True
    
    def test_get_game_requirements_case_insensitive(self, analyzer):
        """Test getting requirements is case insensitive."""
        req = analyzer.get_game_requirements("cyberpunk 2077")
        
        assert req is not None
        assert req.name == "Cyberpunk 2077"
    
    def test_get_game_requirements_partial_match(self, analyzer):
        """Test getting requirements with partial name."""
        req = analyzer.get_game_requirements("Witcher 3")
        
        assert req is not None
        assert "Witcher" in req.name
    
    def test_get_game_requirements_not_found(self, analyzer):
        """Test getting requirements for unknown game."""
        req = analyzer.get_game_requirements("Unknown Game XYZ 2099")
        
        assert req is None
    
    def test_check_compatibility_excellent(self, analyzer, sample_gpu):
        """Test compatibility check with excellent GPU."""
        # RTX 3070 with 8GB should be excellent for most games
        result = analyzer.check_compatibility(sample_gpu, "Fortnite")
        
        assert result["compatible"] in ["excellent", "good"]
        assert "game_name" in result
    
    def test_check_compatibility_unknown_game(self, analyzer, sample_gpu):
        """Test compatibility check for unknown game."""
        result = analyzer.check_compatibility(sample_gpu, "Unknown Game")
        
        assert result["compatible"] == "unknown"
        assert "suggestions" in result
    
    def test_list_games(self, analyzer):
        """Test listing all games."""
        games = analyzer.list_games()
        
        assert isinstance(games, list)
        assert len(games) > 0
        assert games == sorted(games)  # Should be sorted
    
    def test_search_games(self, analyzer):
        """Test searching for games."""
        results = analyzer.search_games("duty")
        
        assert isinstance(results, list)
        assert any("Duty" in game for game in results)
    
    def test_search_games_no_results(self, analyzer):
        """Test searching for non-existent game."""
        results = analyzer.search_games("xyznonexistent123")
        
        assert results == []
    
    def test_get_game_settings(self, analyzer):
        """Test getting available settings for a game."""
        settings = analyzer.get_game_settings("Cyberpunk 2077")
        
        assert isinstance(settings, list)
        assert len(settings) > 0
        assert "DLSS" in settings or "Ray Tracing" in settings
    
    def test_get_games_by_feature_raytracing(self, analyzer):
        """Test getting games that support ray tracing."""
        games = analyzer.get_games_by_feature("raytracing")
        
        assert isinstance(games, list)
        assert "Cyberpunk 2077" in games
    
    def test_get_games_by_feature_dlss(self, analyzer):
        """Test getting games that support DLSS."""
        games = analyzer.get_games_by_feature("dlss")
        
        assert isinstance(games, list)
        assert len(games) > 0
    
    def test_get_games_by_feature_unknown(self, analyzer):
        """Test getting games with unknown feature."""
        games = analyzer.get_games_by_feature("unknownfeature")
        
        assert games == []
    
    def test_add_game(self, analyzer):
        """Test adding a custom game."""
        custom_game = {
            "minimum_vram": 4096,
            "recommended_vram": 8192,
            "minimum_gpu": "GTX 1060",
            "recommended_gpu": "RTX 3060",
            "supports_raytracing": False,
            "supports_dlss": False,
            "supports_fsr": True,
            "release_year": 2024,
            "engine": "Custom Engine",
            "optimization_level": "good",
        }
        
        analyzer.add_game("Custom Test Game", custom_game)
        
        assert "Custom Test Game" in analyzer.games_db
        req = analyzer.get_game_requirements("Custom Test Game")
        assert req is not None
        assert req.engine == "Custom Engine"
    
    def test_load_custom_database(self):
        """Test loading a custom games database."""
        # Create a temporary custom database
        custom_db = {
            "Test Game": {
                "minimum_vram": 2048,
                "recommended_vram": 4096,
                "minimum_gpu": "GTX 960",
                "recommended_gpu": "GTX 1060",
                "supports_raytracing": False,
                "supports_dlss": False,
                "supports_fsr": False,
                "release_year": 2023,
                "engine": "Test Engine",
                "optimization_level": "good",
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(custom_db, f)
            temp_path = f.name
        
        try:
            analyzer = GameAnalyzer(custom_database_path=temp_path)
            req = analyzer.get_game_requirements("Test Game")
            
            assert req is not None
            assert req.engine == "Test Engine"
        finally:
            os.unlink(temp_path)
    
    def test_export_database(self, analyzer):
        """Test exporting the games database."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            analyzer.export_database(temp_path)
            
            with open(temp_path, 'r') as f:
                exported = json.load(f)
            
            assert isinstance(exported, dict)
            assert len(exported) > 0
        finally:
            os.unlink(temp_path)


class TestCompatibilityFeatures:
    """Tests for compatibility feature detection."""
    
    @pytest.fixture
    def analyzer(self):
        return GameAnalyzer()
    
    @pytest.fixture
    def rtx_gpu(self):
        """Create an RTX GPU for testing."""
        return GPUInfo(
            name="NVIDIA GeForce RTX 3070",
            vram_total=8192,
        )
    
    @pytest.fixture
    def gtx_gpu(self):
        """Create a GTX GPU for testing."""
        return GPUInfo(
            name="NVIDIA GeForce GTX 1660",
            vram_total=6144,
        )
    
    def test_rtx_dlss_support(self, analyzer, rtx_gpu):
        """Test that RTX GPUs show DLSS support."""
        result = analyzer.check_compatibility(rtx_gpu, "Cyberpunk 2077")
        
        features = result.get("features", [])
        dlss_supported = any("DLSS supported" in f for f in features)
        assert dlss_supported
    
    def test_gtx_no_dlss(self, analyzer, gtx_gpu):
        """Test that GTX GPUs don't support DLSS."""
        result = analyzer.check_compatibility(gtx_gpu, "Cyberpunk 2077")
        
        features = result.get("features", [])
        dlss_not_supported = any("DLSS not supported" in f for f in features)
        assert dlss_not_supported
    
    def test_fsr_universal_support(self, analyzer, gtx_gpu):
        """Test that FSR is shown as supported for all GPUs."""
        result = analyzer.check_compatibility(gtx_gpu, "Baldur's Gate 3")
        
        features = result.get("features", [])
        fsr_supported = any("FSR supported" in f for f in features)
        assert fsr_supported
