# 🎮 GPU Gaming Advisor

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by Claude](https://img.shields.io/badge/🤖%20Powered%20by-Claude%20AI-blueviolet)](https://www.anthropic.com/claude)
[![Built with Claude](https://img.shields.io/badge/🛠️%20Built%20with-Claude%20Code-orange)](https://www.anthropic.com/)
[![Anthropic](https://img.shields.io/badge/Anthropic-API-black)](https://console.anthropic.com/)

<a href="https://freeimage.host/"><img src="https://iili.io/fSgTyiv.png" alt="fSgTyiv.png" border="0" /></a>

<a href="https://freeimage.host/"><img src="https://iili.io/fSgHxXn.png" alt="fSgHxXn.png" border="0" /></a>


###  **100% Built with Claude AI by Anthropic**

*This entire project was conceived, designed, and coded using Claude AI*

[Get Started](#-quick-start) · [Features](#-features) · [Documentation](#-documentation) · [About Claude](#-powered-by-claude-ai)

</div>

---

## 🧠 Powered by Claude AI

> **This project is a showcase of Claude AI's capabilities.** Every line of code, every piece of documentation, and every design decision in this repository was created by [Claude](https://www.anthropic.com/claude), Anthropic's AI assistant.

**GPU Gaming Advisor** demonstrates how Claude AI can:
 **Architect** complete software solutions from scratch
 **Write** production-quality Python code
**Create** comprehensive documentation
**Solve** real-world problems with intelligent analysis
 **Integrate** with its own API for recursive AI-powered features

### Why Claude?

Claude is Anthropic's frontier AI assistant, known for being helpful, harmless, and honest. This project leverages Claude's:

- **Deep technical knowledge** for GPU architecture understanding
- **Reasoning capabilities** for game optimization recommendations  
- **Code generation skills** for building robust Python applications
- **Natural language understanding** for interactive chat features

---

**GPU Gaming Advisor** is an intelligent tool that combines real-time GPU analysis with Claude AI to provide personalized gaming optimization recommendations. Get the best settings for your games based on your actual hardware capabilities.

![GPU Gaming Advisor Demo](docs/images/demo.gif)

##  Features

###  Claude AI-Powered Intelligence
- **Smart Recommendations** - Claude analyzes your GPU specs and provides tailored game settings
- **Natural Language Chat** - Ask Claude anything about gaming optimization in plain English
- **Intelligent FPS Prediction** - Claude estimates performance based on hardware analysis
- **Contextual Tips** - Get personalized advice that considers your specific setup

###  Hardware Analysis
- **GPU Detection & Analysis** - Automatically detects your GPU and retrieves detailed specifications
- **Real-time Monitoring** - Track GPU temperature, usage, and memory in real-time
- **Health Assessment** - Claude analyzes your GPU's current status and suggests improvements

###  Gaming Optimization  
- **Game Database** - Extensive database of popular games with requirements
- **Optimal Settings** - Get the perfect balance of quality and performance
- **Multi-Resolution Support** - Recommendations for 1080p, 1440p, and 4K gaming
- **Profile Export** - Save and share your optimized settings

##  Quick Start

### Prerequisites

- Python 3.8 or higher
- NVIDIA GPU (AMD support coming soon)
- Anthropic API key ([Get one here](https://console.anthropic.com/))

<a href="https://freeimage.host/"><img src="https://iili.io/fSgJC3x.png" alt="fSgJC3x.png" border="0" /></a>

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/gpu-gaming-advisor.git
cd gpu-gaming-advisor

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your API key
export ANTHROPIC_API_KEY="your-api-key-here"
# On Windows: set ANTHROPIC_API_KEY=your-api-key-here
```

### Basic Usage

```bash
# Analyze your GPU
python -m gpu_gaming_advisor analyze

# Get recommendations for a specific game
python -m gpu_gaming_advisor optimize "Cyberpunk 2077"

# Interactive mode
python -m gpu_gaming_advisor interactive

# Monitor GPU in real-time
python -m gpu_gaming_advisor monitor
```

## 📖 Documentation

### Commands

| Command | Description |
|---------|-------------|
| `analyze` | Analyze your GPU and display detailed specifications |
| `optimize <game>` | Get optimized settings for a specific game |
| `predict <game>` | Predict FPS for a game at different quality presets |
| `compare <gpu>` | Compare your GPU with another model |
| `monitor` | Real-time GPU monitoring dashboard |
| `interactive` | Interactive chat mode with Claude AI |
| `list-games` | Show all supported games |
| `export` | Export your settings profile |

### Configuration

Create a `config.yaml` file in the project root or use environment variables:

```yaml
# config.yaml
anthropic:
  api_key: ${ANTHROPIC_API_KEY}
  model: claude-sonnet-4-20250514

monitoring:
  refresh_rate: 1.0  # seconds
  log_metrics: true

preferences:
  target_fps: 60
  priority: quality  # quality | balanced | performance
  resolution: 1920x1080
```

### Example Output

```
🖥️  GPU Gaming Advisor - Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GPU Detected: NVIDIA GeForce RTX 3070
├── VRAM: 8 GB GDDR6
├── CUDA Cores: 5888
├── Base Clock: 1500 MHz
├── Boost Clock: 1725 MHz
└── Driver: 535.154.05

Current Status:
├── Temperature: 45°C
├── GPU Usage: 12%
├── Memory Used: 1.2 GB / 8 GB
└── Power Draw: 35W

🎮 Game: Cyberpunk 2077
━━━━━━━━━━━━━━━━━━━━━━━

 Claude AI Recommendations:

Based on your RTX 3070, here are the optimal settings for
Cyberpunk 2077 at 1080p targeting 60 FPS:

┌─────────────────────┬──────────────┐
│ Setting             │ Recommended  │
├─────────────────────┼──────────────┤
│ Quality Preset      │ High         │
│ Ray Tracing         │ Medium       │
│ DLSS                │ Quality      │
│ Crowd Density       │ High         │
│ Shadow Quality      │ High         │
│ Reflection Quality  │ High         │
│ Ambient Occlusion   │ High         │
└─────────────────────┴──────────────┘

 Expected Performance: 58-72 FPS (avg: 65 FPS)

 Tips:
• Enable DLSS for significant FPS boost with minimal quality loss
• Ray Tracing at Medium provides good visuals without major performance hit
• Consider lowering Crowd Density in dense areas if you experience drops
```

##  Project Structure

```
gpu-gaming-advisor/
├── src/
│   └── gpu_gaming_advisor/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py              # Command-line interface
│       ├── gpu_detector.py     # GPU detection and info
│       ├── game_analyzer.py    # Game analysis logic
│       ├── claude_advisor.py   # Claude AI integration
│       ├── monitor.py          # Real-time monitoring
│       ├── fps_predictor.py    # FPS prediction engine
│       └── utils.py            # Utility functions
├── data/
│   └── games_database.json     # Game requirements database
├── config/
│   └── default_config.yaml     # Default configuration
├── tests/
│   ├── test_gpu_detector.py
│   ├── test_game_analyzer.py
│   └── test_claude_advisor.py
├── docs/
│   └── images/
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```
<a href="https://freeimage.host/"><img src="https://iili.io/fSgJ46b.png" alt="fSgJ46b.png" border="0" /></a>

## 🔧 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gpu_gaming_advisor

# Run specific test file
pytest tests/test_gpu_detector.py
```

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🗺️ Roadmap

- [x] NVIDIA GPU detection and analysis
- [x] Claude AI integration for recommendations
- [x] Basic game database
- [x] CLI interface
- [ ] AMD GPU support
- [ ] Intel Arc GPU support
- [ ] GUI application
- [ ] Steam library integration
- [ ] Automatic game detection
- [ ] Cloud sync for profiles
- [ ] Community-driven game database
- [ ] Benchmark integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  About Claude & Anthropic

<div align="center">

<img src="docs/images/anthropic-logo.png" alt="Anthropic" width="200"/>

</div>

This project was **entirely created by Claude**, Anthropic's AI assistant. Claude is designed to be helpful, harmless, and honest.

### What is Claude?

[Claude](https://www.anthropic.com/claude) is a family of AI models created by [Anthropic](https://www.anthropic.com/). Claude excels at:

-  **Thoughtful conversation** - Engaging in nuanced, contextual dialogue
-  **Content creation** - Writing code, documentation, and creative content
-  **Analysis** - Understanding complex information and providing insights
-  **Problem-solving** - Breaking down challenges and offering solutions

### Get Your Own Claude API Key

To use the AI-powered features of GPU Gaming Advisor, you'll need an Anthropic API key:

1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Create an account or sign in
3. Generate an API key
4. Set it as `ANTHROPIC_API_KEY` environment variable

### Claude Built This!

Every aspect of this project showcases Claude's capabilities:

| Component | Created by Claude |
|-----------|-------------------|
| Architecture Design | ✅ |
| Python Source Code | ✅ |
| CLI Interface | ✅ |
| Documentation | ✅ |
| Configuration Files | ✅ |
| Test Suite | ✅ |
| Game Database | ✅ |

##  Acknowledgments

- [**Anthropic**](https://www.anthropic.com/) - For creating Claude AI, which built this entire project
- [**Claude AI**](https://www.anthropic.com/claude) - The AI assistant that designed and coded everything you see here
- [GPUtil](https://github.com/anderskm/gputil) - For GPU utilities
- [Rich](https://github.com/Textualize/rich) - For beautiful terminal output
- [Typer](https://github.com/tiangolo/typer) - For CLI framework

##  Disclaimer

FPS predictions and recommendations are estimates based on available data and Claude AI analysis. Actual performance may vary depending on system configuration, game updates, drivers, and other factors. Always test settings in-game for best results.

---

<div align="center">

###  Built Entirely with Claude AI

<a href="https://www.anthropic.com/claude">
  <img src="https://img.shields.io/badge/Created%20by-Claude%20AI-blueviolet?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnoiIGZpbGw9IiNmZmYiLz48L3N2Zz4=" alt="Built with Claude"/>
</a>

<p>
  <a href="https://www.anthropic.com/">Anthropic</a> · 
  <a href="https://www.anthropic.com/claude">Claude AI</a> · 
  <a href="https://console.anthropic.com/">API Console</a>
</p>

<sub>This project demonstrates the power of AI-assisted development.<br/>
Every line of code was written by Claude, Anthropic's AI assistant.</sub>

<br/>

**Made with  by Claude AI | Powered by Anthropic**

</div>
