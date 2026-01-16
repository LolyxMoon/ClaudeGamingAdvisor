# Usage Guide

This guide covers all the features and commands available in GPU Gaming Advisor.

## Table of Contents

- [Quick Start](#quick-start)
- [Commands](#commands)
- [Interactive Mode](#interactive-mode)
- [Configuration](#configuration)
- [Examples](#examples)
- [Tips & Best Practices](#tips--best-practices)

## Quick Start

```bash
# Analyze your GPU
python -m gpu_gaming_advisor analyze

# Get recommendations for a game
python -m gpu_gaming_advisor optimize "Cyberpunk 2077"

# Predict FPS
python -m gpu_gaming_advisor predict "Fortnite" --quality ultra

# Start real-time monitoring
python -m gpu_gaming_advisor monitor
```

## Commands

### analyze

Analyze your GPU and display detailed specifications.

```bash
python -m gpu_gaming_advisor analyze
```

**Output includes:**
- GPU model and architecture
- VRAM capacity and usage
- CUDA core count
- Clock speeds
- Current temperature and power draw
- Driver version

### optimize

Get AI-powered optimization recommendations for a specific game.

```bash
python -m gpu_gaming_advisor optimize <game_name> [options]
```

**Options:**
| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--resolution` | `-r` | Target resolution | 1920x1080 |
| `--fps` | `-f` | Target framerate | 60 |
| `--priority` | `-p` | quality/balanced/performance | balanced |

**Examples:**
```bash
# Basic optimization
python -m gpu_gaming_advisor optimize "Elden Ring"

# 1440p at 144fps, prioritizing performance
python -m gpu_gaming_advisor optimize "Valorant" -r 2560x1440 -f 144 -p performance

# 4K with quality priority
python -m gpu_gaming_advisor optimize "Red Dead Redemption 2" -r 3840x2160 -p quality
```

### predict

Predict FPS for a game at different settings.

```bash
python -m gpu_gaming_advisor predict <game_name> [options]
```

**Options:**
| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--resolution` | `-r` | Target resolution | 1920x1080 |
| `--quality` | `-q` | Quality preset | high |

**Examples:**
```bash
# Predict at default settings
python -m gpu_gaming_advisor predict "Cyberpunk 2077"

# Predict at 4K Ultra
python -m gpu_gaming_advisor predict "Fortnite" -r 3840x2160 -q ultra
```

### compare

Compare your GPU with another model.

```bash
python -m gpu_gaming_advisor compare <other_gpu> [options]
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--game` | `-g` | Specific game for comparison |

**Examples:**
```bash
# General comparison
python -m gpu_gaming_advisor compare "RTX 4070"

# Game-specific comparison
python -m gpu_gaming_advisor compare "RTX 4080" --game "Alan Wake 2"
```

### monitor

Real-time GPU monitoring with live dashboard.

```bash
python -m gpu_gaming_advisor monitor [options]
```

**Options:**
| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--duration` | `-d` | Duration in seconds | indefinite |
| `--refresh` | `-r` | Refresh rate in seconds | 1.0 |

**Examples:**
```bash
# Monitor indefinitely
python -m gpu_gaming_advisor monitor

# Monitor for 60 seconds with 0.5s refresh
python -m gpu_gaming_advisor monitor -d 60 -r 0.5
```

**Dashboard shows:**
- Temperature with color-coded status
- GPU utilization percentage
- VRAM usage
- Power draw
- Session statistics

### list-games

List all supported games in the database.

```bash
python -m gpu_gaming_advisor list-games [options]
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--search` | `-s` | Search for games by name |
| `--feature` | `-f` | Filter by feature (raytracing/dlss/fsr) |

**Examples:**
```bash
# List all games
python -m gpu_gaming_advisor list-games

# Search for games
python -m gpu_gaming_advisor list-games --search "duty"

# List games with ray tracing
python -m gpu_gaming_advisor list-games --feature raytracing
```

### interactive

Start an interactive chat session with Claude AI.

```bash
python -m gpu_gaming_advisor interactive
```

**Features:**
- Ask any gaming-related question
- Get personalized advice based on your GPU
- Conversation context is maintained
- Type 'quit' or 'exit' to end

**Example session:**
```
You: What games can I play at 4K?
Claude: Based on your RTX 3070 with 8GB VRAM...

You: Should I upgrade to an RTX 4070?
Claude: Comparing your current RTX 3070...
```

### export

Export your GPU profile and settings.

```bash
python -m gpu_gaming_advisor export [options]
```

**Options:**
| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file path | profile.json |
| `--game` | `-g` | Include game compatibility |  |

### version

Show version information.

```bash
python -m gpu_gaming_advisor version
```

## Interactive Mode

Interactive mode provides a conversational interface with Claude AI:

```bash
python -m gpu_gaming_advisor interactive
```

### Sample Questions

- "What settings should I use for Cyberpunk 2077?"
- "Can my GPU handle 4K gaming?"
- "Why is my FPS low in Starfield?"
- "Should I enable ray tracing?"
- "Compare my GPU to an RTX 4080"
- "What upcoming games will my GPU struggle with?"

### Commands in Interactive Mode

- `quit` or `exit` - End the session
- `clear` - Clear conversation history
- `help` - Show available commands

## Configuration

### Configuration File

Create `config.yaml` in the project root:

```yaml
anthropic:
  api_key: ${ANTHROPIC_API_KEY}
  model: claude-sonnet-4-20250514

monitoring:
  refresh_rate: 1.0
  log_metrics: false

preferences:
  target_fps: 60
  priority: balanced
  resolution: 1920x1080
  quality_preset: high
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `DEFAULT_TARGET_FPS` | Default target framerate |
| `DEFAULT_RESOLUTION` | Default resolution |

## Examples

### Complete Workflow Example

```bash
# 1. First, analyze your GPU
python -m gpu_gaming_advisor analyze

# 2. Check if a game is compatible
python -m gpu_gaming_advisor list-games --search "cyberpunk"

# 3. Get optimized settings
python -m gpu_gaming_advisor optimize "Cyberpunk 2077" -r 2560x1440 -f 60

# 4. Check expected FPS at different presets
python -m gpu_gaming_advisor predict "Cyberpunk 2077" -r 2560x1440 -q ultra

# 5. Monitor while gaming
python -m gpu_gaming_advisor monitor -d 3600
```

### Scripting Example

```python
from gpu_gaming_advisor import GPUDetector, GameAnalyzer, FPSPredictor

# Detect GPU
detector = GPUDetector()
detector.initialize()
gpu = detector.get_primary_gpu()

# Analyze game
analyzer = GameAnalyzer()
compatibility = analyzer.check_compatibility(gpu, "Elden Ring")
print(f"Compatibility: {compatibility['compatible']}")

# Predict FPS
predictor = FPSPredictor()
prediction = predictor.predict(gpu, "Elden Ring", "1920x1080", "high")
print(f"Expected FPS: {prediction.fps_average}")

detector.shutdown()
```

## Tips & Best Practices

### For Best Recommendations

1. **Keep drivers updated** - Latest drivers often improve performance
2. **Be specific** - Use exact game names when possible
3. **Consider your monitor** - No point targeting 144fps on a 60Hz monitor
4. **Enable upscaling** - DLSS/FSR can significantly boost FPS

### Resolution Guidelines

| Resolution | Best For |
|------------|----------|
| 1080p | Competitive gaming, older GPUs |
| 1440p | Sweet spot for most modern GPUs |
| 4K | High-end GPUs (RTX 4080+) |

### Priority Settings

| Priority | When to Use |
|----------|-------------|
| Quality | Single-player, visually impressive games |
| Balanced | Most games, general use |
| Performance | Competitive multiplayer, e-sports |

### Monitoring Tips

- Run monitor during gaming to identify issues
- Watch for temperature spikes above 85°C
- High VRAM usage may cause stuttering
- Export session data for analysis
