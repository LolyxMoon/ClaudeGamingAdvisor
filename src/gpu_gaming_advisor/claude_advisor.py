"""
Claude AI Advisor Module.

This module provides integration with Claude AI for intelligent
gaming optimization recommendations.
"""

import os
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from anthropic import Anthropic

from .gpu_detector import GPUInfo


@dataclass
class GameRecommendation:
    """Data class for game optimization recommendations."""
    
    game_name: str
    gpu_name: str
    resolution: str
    target_fps: int
    settings: Dict[str, str]
    expected_fps_range: tuple
    tips: List[str]
    confidence: str  # "high", "medium", "low"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert recommendation to dictionary."""
        return {
            "game_name": self.game_name,
            "gpu_name": self.gpu_name,
            "resolution": self.resolution,
            "target_fps": self.target_fps,
            "settings": self.settings,
            "expected_fps_min": self.expected_fps_range[0],
            "expected_fps_max": self.expected_fps_range[1],
            "tips": self.tips,
            "confidence": self.confidence,
        }


class ClaudeAdvisor:
    """
    Claude AI integration for gaming optimization advice.
    
    This class uses Claude to analyze GPU specifications and provide
    intelligent recommendations for game settings.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize the Claude Advisor.
        
        Args:
            api_key: Anthropic API key. If not provided, reads from
                    ANTHROPIC_API_KEY environment variable.
            model: Claude model to use.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key is required. Set ANTHROPIC_API_KEY environment "
                "variable or pass api_key parameter."
            )
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        
        # System prompt for gaming optimization
        self.system_prompt = """You are an expert PC gaming optimization advisor with deep knowledge of:
- GPU architectures and capabilities (NVIDIA, AMD, Intel)
- Game engine requirements and optimization techniques
- Graphics settings and their performance impact
- Resolution scaling technologies (DLSS, FSR, XeSS)
- Ray tracing performance characteristics

Your role is to provide accurate, practical recommendations for game settings based on the user's hardware. Always consider:
1. The GPU's VRAM, CUDA cores/stream processors, and memory bandwidth
2. Target resolution and framerate
3. The specific game's engine and optimization level
4. Balance between visual quality and performance

Provide recommendations in a structured format with specific settings and expected performance. Be honest about limitations and uncertainties. If you're not confident about a specific game's performance, indicate lower confidence.

When giving recommendations, format your response as JSON with this structure:
{
    "preset": "recommended overall preset",
    "settings": {
        "setting_name": "value",
        ...
    },
    "expected_fps": {
        "min": number,
        "max": number,
        "average": number
    },
    "tips": ["tip1", "tip2", ...],
    "confidence": "high|medium|low",
    "reasoning": "brief explanation"
}"""

    def get_optimization_recommendation(
        self,
        gpu_info: GPUInfo,
        game_name: str,
        resolution: str = "1920x1080",
        target_fps: int = 60,
        priority: str = "balanced"
    ) -> GameRecommendation:
        """
        Get optimization recommendations for a specific game.
        
        Args:
            gpu_info: GPU information from GPUDetector.
            game_name: Name of the game to optimize.
            resolution: Target resolution (e.g., "1920x1080", "2560x1440", "3840x2160").
            target_fps: Target framerate.
            priority: Optimization priority ("quality", "balanced", "performance").
            
        Returns:
            GameRecommendation with optimized settings.
        """
        prompt = f"""Please provide optimized game settings for the following configuration:

GPU: {gpu_info.name}
- VRAM: {gpu_info.vram_total} MB ({gpu_info.vram_total / 1024:.1f} GB)
- Architecture: {gpu_info.architecture}
- CUDA Cores: {gpu_info.cuda_cores:,}
- Performance Tier: {gpu_info.tier}

Game: {game_name}
Target Resolution: {resolution}
Target FPS: {target_fps}
Priority: {priority} (quality vs performance)

Please analyze the GPU's capabilities and provide optimal settings for this game at the specified resolution and target framerate. Include specific graphics settings recommendations and expected performance.

Respond with JSON only, no additional text."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the response
        response_text = response.content[0].text
        
        try:
            # Try to extract JSON from the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                data = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
            
            return GameRecommendation(
                game_name=game_name,
                gpu_name=gpu_info.name,
                resolution=resolution,
                target_fps=target_fps,
                settings=data.get("settings", {}),
                expected_fps_range=(
                    data.get("expected_fps", {}).get("min", 0),
                    data.get("expected_fps", {}).get("max", 0)
                ),
                tips=data.get("tips", []),
                confidence=data.get("confidence", "medium")
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback if JSON parsing fails
            return GameRecommendation(
                game_name=game_name,
                gpu_name=gpu_info.name,
                resolution=resolution,
                target_fps=target_fps,
                settings={"preset": "High", "note": "Unable to parse detailed settings"},
                expected_fps_range=(target_fps - 10, target_fps + 10),
                tips=["Consider adjusting settings based on in-game performance"],
                confidence="low"
            )
    
    def predict_fps(
        self,
        gpu_info: GPUInfo,
        game_name: str,
        resolution: str,
        quality_preset: str
    ) -> Dict[str, Any]:
        """
        Predict FPS for a game at specific settings.
        
        Args:
            gpu_info: GPU information.
            game_name: Name of the game.
            resolution: Target resolution.
            quality_preset: Quality preset (Low, Medium, High, Ultra, etc.).
            
        Returns:
            Dictionary with FPS predictions.
        """
        prompt = f"""Predict the FPS performance for this configuration:

GPU: {gpu_info.name}
- VRAM: {gpu_info.vram_total / 1024:.1f} GB
- Architecture: {gpu_info.architecture}
- Performance Tier: {gpu_info.tier}

Game: {game_name}
Resolution: {resolution}
Quality Preset: {quality_preset}

Provide FPS prediction as JSON:
{{
    "fps_min": number,
    "fps_max": number,
    "fps_average": number,
    "fps_1_percent_low": number,
    "confidence": "high|medium|low",
    "bottleneck": "gpu|cpu|vram|none",
    "notes": "any relevant notes"
}}

Respond with JSON only."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response_text[json_start:json_end])
        except json.JSONDecodeError:
            pass
        
        return {
            "fps_min": 0,
            "fps_max": 0,
            "fps_average": 0,
            "confidence": "low",
            "notes": "Unable to predict FPS"
        }
    
    def compare_gpus(
        self,
        gpu1_info: GPUInfo,
        gpu2_name: str,
        game_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare two GPUs for gaming performance.
        
        Args:
            gpu1_info: Information about the first GPU (user's GPU).
            gpu2_name: Name of the GPU to compare against.
            game_name: Optional specific game for comparison.
            
        Returns:
            Comparison results.
        """
        game_context = f" specifically for {game_name}" if game_name else ""
        
        prompt = f"""Compare these two GPUs for gaming performance{game_context}:

GPU 1 (User's GPU): {gpu1_info.name}
- VRAM: {gpu1_info.vram_total / 1024:.1f} GB
- Architecture: {gpu1_info.architecture}
- CUDA Cores: {gpu1_info.cuda_cores:,}
- Performance Tier: {gpu1_info.tier}

GPU 2: {gpu2_name}

Provide comparison as JSON:
{{
    "gpu1_name": "name",
    "gpu2_name": "name",
    "performance_difference_percent": number (positive if GPU2 is faster),
    "gpu1_advantages": ["list of advantages"],
    "gpu2_advantages": ["list of advantages"],
    "recommendation": "which is better and why",
    "value_comparison": "price/performance analysis if applicable"
}}

Respond with JSON only."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response_text[json_start:json_end])
        except json.JSONDecodeError:
            pass
        
        return {"error": "Unable to compare GPUs"}
    
    def chat(self, gpu_info: GPUInfo, user_message: str, conversation_history: List[Dict] = None) -> str:
        """
        Have an interactive chat about gaming optimization.
        
        Args:
            gpu_info: GPU information for context.
            user_message: User's message.
            conversation_history: Previous messages in the conversation.
            
        Returns:
            Claude's response.
        """
        context = f"""The user has the following GPU:
- Model: {gpu_info.name}
- VRAM: {gpu_info.vram_total / 1024:.1f} GB
- Architecture: {gpu_info.architecture}
- Performance Tier: {gpu_info.tier}
- Current Temperature: {gpu_info.temperature}°C
- Current Usage: {gpu_info.gpu_usage}%

Please help them with their gaming-related questions."""

        messages = conversation_history or []
        messages.append({"role": "user", "content": user_message})
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt + "\n\n" + context,
            messages=messages
        )
        
        return response.content[0].text
    
    def analyze_gpu_health(self, gpu_info: GPUInfo) -> Dict[str, Any]:
        """
        Analyze GPU health and provide recommendations.
        
        Args:
            gpu_info: GPU information including current status.
            
        Returns:
            Health analysis and recommendations.
        """
        prompt = f"""Analyze the health and status of this GPU:

GPU: {gpu_info.name}
- VRAM Total: {gpu_info.vram_total} MB
- VRAM Used: {gpu_info.vram_used} MB ({gpu_info.vram_used / gpu_info.vram_total * 100:.1f}% used)
- Temperature: {gpu_info.temperature}°C
- GPU Usage: {gpu_info.gpu_usage}%
- Power Draw: {gpu_info.power_draw}W / {gpu_info.power_limit}W limit
- Driver Version: {gpu_info.driver_version}

Provide health analysis as JSON:
{{
    "overall_health": "good|warning|critical",
    "temperature_status": "normal|elevated|high|critical",
    "memory_status": "normal|high_usage|critical",
    "issues": ["list of any detected issues"],
    "recommendations": ["list of recommendations"],
    "driver_note": "any notes about the driver version"
}}

Respond with JSON only."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response_text[json_start:json_end])
        except json.JSONDecodeError:
            pass
        
        return {
            "overall_health": "unknown",
            "issues": ["Unable to analyze GPU health"],
            "recommendations": []
        }
