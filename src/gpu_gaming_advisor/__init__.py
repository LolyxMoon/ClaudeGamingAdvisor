"""
GPU Gaming Advisor - AI-powered GPU gaming optimization tool.

🤖 **100% Built with Claude AI by Anthropic**

This entire package was conceived, designed, and coded by Claude,
Anthropic's AI assistant. It demonstrates what's possible when
AI builds real-world applications.

This package provides tools for analyzing your GPU, getting game optimization
recommendations from Claude AI, and monitoring GPU performance in real-time.

Features:
    - GPU detection and specification retrieval
    - Claude AI-powered optimization recommendations
    - FPS prediction based on hardware analysis
    - Real-time GPU monitoring dashboard
    - Interactive chat with Claude about gaming

Learn more about Claude: https://www.anthropic.com/claude
Get your API key: https://console.anthropic.com/

Example:
    >>> from gpu_gaming_advisor import GPUDetector, ClaudeAdvisor
    >>> detector = GPUDetector()
    >>> detector.initialize()
    >>> gpu = detector.get_primary_gpu()
    >>> print(f"Detected: {gpu.name}")
    
Created by Claude AI | Powered by Anthropic
"""

__version__ = "1.0.0"
__author__ = "Claude AI (Anthropic)"
__credits__ = ["Claude AI by Anthropic - Built this entire project"]
__maintainer__ = "Claude AI"
__email__ = "https://www.anthropic.com/claude"
__status__ = "Production"
__url__ = "https://github.com/yourusername/gpu-gaming-advisor"
__description__ = "AI-powered GPU gaming optimization tool, built entirely by Claude AI"

# ASCII Art Banner
BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🎮  GPU Gaming Advisor                                      ║
║                                                               ║
║   🤖 100% Built with Claude AI by Anthropic                   ║
║                                                               ║
║   Get intelligent gaming optimization recommendations         ║
║   powered by Claude's advanced AI capabilities.               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""

from .gpu_detector import GPUDetector, GPUInfo
from .game_analyzer import GameAnalyzer
from .claude_advisor import ClaudeAdvisor
from .monitor import GPUMonitor
from .fps_predictor import FPSPredictor

__all__ = [
    "GPUDetector",
    "GPUInfo",
    "GameAnalyzer",
    "ClaudeAdvisor",
    "GPUMonitor",
    "FPSPredictor",
]
