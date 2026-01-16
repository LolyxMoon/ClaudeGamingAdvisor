"""
Tests for Claude Advisor Module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

import sys
sys.path.insert(0, 'src')

from gpu_gaming_advisor.claude_advisor import (
    ClaudeAdvisor,
    GameRecommendation,
)
from gpu_gaming_advisor.gpu_detector import GPUInfo


class TestGameRecommendation:
    """Tests for GameRecommendation dataclass."""
    
    def test_recommendation_creation(self):
        """Test creating a GameRecommendation instance."""
        rec = GameRecommendation(
            game_name="Cyberpunk 2077",
            gpu_name="RTX 3070",
            resolution="1920x1080",
            target_fps=60,
            settings={"Quality": "High", "DLSS": "Quality"},
            expected_fps_range=(55, 70),
            tips=["Enable DLSS for better performance"],
            confidence="high",
        )
        
        assert rec.game_name == "Cyberpunk 2077"
        assert rec.target_fps == 60
        assert rec.settings["DLSS"] == "Quality"
        assert rec.confidence == "high"
    
    def test_recommendation_to_dict(self):
        """Test converting recommendation to dictionary."""
        rec = GameRecommendation(
            game_name="Elden Ring",
            gpu_name="RTX 4070",
            resolution="2560x1440",
            target_fps=60,
            settings={"Quality": "High"},
            expected_fps_range=(50, 65),
            tips=[],
            confidence="medium",
        )
        
        data = rec.to_dict()
        
        assert isinstance(data, dict)
        assert data["game_name"] == "Elden Ring"
        assert data["expected_fps_min"] == 50
        assert data["expected_fps_max"] == 65


class TestClaudeAdvisor:
    """Tests for ClaudeAdvisor class."""
    
    @pytest.fixture
    def sample_gpu(self):
        """Create a sample GPU for testing."""
        return GPUInfo(
            name="NVIDIA GeForce RTX 3070",
            vendor="NVIDIA",
            vram_total=8192,
            cuda_cores=5888,
            architecture="Ampere",
            tier="High-End",
            temperature=55.0,
            gpu_usage=20.0,
        )
    
    def test_advisor_requires_api_key(self):
        """Test that advisor requires API key."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="API key is required"):
                ClaudeAdvisor(api_key=None)
    
    def test_advisor_accepts_api_key_param(self):
        """Test that advisor accepts API key as parameter."""
        with patch('gpu_gaming_advisor.claude_advisor.Anthropic'):
            advisor = ClaudeAdvisor(api_key="sk-ant-test-key")
            assert advisor.api_key == "sk-ant-test-key"
    
    def test_advisor_uses_env_variable(self):
        """Test that advisor uses environment variable."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'sk-ant-env-key'}):
            with patch('gpu_gaming_advisor.claude_advisor.Anthropic'):
                advisor = ClaudeAdvisor()
                assert advisor.api_key == "sk-ant-env-key"
    
    @patch('gpu_gaming_advisor.claude_advisor.Anthropic')
    def test_get_optimization_recommendation(self, mock_anthropic, sample_gpu):
        """Test getting optimization recommendations."""
        # Setup mock response
        mock_response = Mock()
        mock_response.content = [Mock(text=json.dumps({
            "preset": "High",
            "settings": {
                "Quality Preset": "High",
                "DLSS": "Quality",
                "Ray Tracing": "Medium"
            },
            "expected_fps": {
                "min": 55,
                "max": 70,
                "average": 62
            },
            "tips": ["Enable DLSS for better performance"],
            "confidence": "high",
            "reasoning": "RTX 3070 handles this well"
        }))]
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        advisor = ClaudeAdvisor(api_key="sk-ant-test")
        recommendation = advisor.get_optimization_recommendation(
            gpu_info=sample_gpu,
            game_name="Cyberpunk 2077",
            resolution="1920x1080",
            target_fps=60,
        )
        
        assert isinstance(recommendation, GameRecommendation)
        assert recommendation.game_name == "Cyberpunk 2077"
        assert "DLSS" in recommendation.settings
    
    @patch('gpu_gaming_advisor.claude_advisor.Anthropic')
    def test_predict_fps(self, mock_anthropic, sample_gpu):
        """Test FPS prediction."""
        mock_response = Mock()
        mock_response.content = [Mock(text=json.dumps({
            "fps_min": 50,
            "fps_max": 70,
            "fps_average": 60,
            "fps_1_percent_low": 45,
            "confidence": "high",
            "bottleneck": "none",
            "notes": "Good performance expected"
        }))]
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        advisor = ClaudeAdvisor(api_key="sk-ant-test")
        prediction = advisor.predict_fps(
            gpu_info=sample_gpu,
            game_name="Fortnite",
            resolution="1920x1080",
            quality_preset="High",
        )
        
        assert isinstance(prediction, dict)
        assert prediction["fps_average"] == 60
        assert prediction["confidence"] == "high"
    
    @patch('gpu_gaming_advisor.claude_advisor.Anthropic')
    def test_compare_gpus(self, mock_anthropic, sample_gpu):
        """Test GPU comparison."""
        mock_response = Mock()
        mock_response.content = [Mock(text=json.dumps({
            "gpu1_name": "RTX 3070",
            "gpu2_name": "RTX 4070",
            "performance_difference_percent": 25,
            "gpu1_advantages": ["Good value"],
            "gpu2_advantages": ["Newer architecture", "Better ray tracing"],
            "recommendation": "RTX 4070 is faster but more expensive",
            "value_comparison": "RTX 3070 offers better value if budget is limited"
        }))]
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        advisor = ClaudeAdvisor(api_key="sk-ant-test")
        comparison = advisor.compare_gpus(
            gpu1_info=sample_gpu,
            gpu2_name="RTX 4070",
        )
        
        assert isinstance(comparison, dict)
        assert "performance_difference_percent" in comparison
    
    @patch('gpu_gaming_advisor.claude_advisor.Anthropic')
    def test_chat(self, mock_anthropic, sample_gpu):
        """Test interactive chat."""
        mock_response = Mock()
        mock_response.content = [Mock(text="Based on your RTX 3070, you can play most games at high settings.")]
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        advisor = ClaudeAdvisor(api_key="sk-ant-test")
        response = advisor.chat(
            gpu_info=sample_gpu,
            user_message="What games can I play?",
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    @patch('gpu_gaming_advisor.claude_advisor.Anthropic')
    def test_analyze_gpu_health(self, mock_anthropic, sample_gpu):
        """Test GPU health analysis."""
        mock_response = Mock()
        mock_response.content = [Mock(text=json.dumps({
            "overall_health": "good",
            "temperature_status": "normal",
            "memory_status": "normal",
            "issues": [],
            "recommendations": ["Consider updating drivers"],
            "driver_note": "Driver is current"
        }))]
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        advisor = ClaudeAdvisor(api_key="sk-ant-test")
        health = advisor.analyze_gpu_health(sample_gpu)
        
        assert isinstance(health, dict)
        assert health["overall_health"] == "good"
    
    @patch('gpu_gaming_advisor.claude_advisor.Anthropic')
    def test_handles_invalid_json_response(self, mock_anthropic, sample_gpu):
        """Test handling of invalid JSON responses."""
        mock_response = Mock()
        mock_response.content = [Mock(text="This is not valid JSON")]
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        advisor = ClaudeAdvisor(api_key="sk-ant-test")
        recommendation = advisor.get_optimization_recommendation(
            gpu_info=sample_gpu,
            game_name="Test Game",
        )
        
        # Should return a fallback recommendation with low confidence
        assert recommendation.confidence == "low"
