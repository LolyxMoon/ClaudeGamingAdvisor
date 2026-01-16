# API Documentation

This document provides detailed API documentation for developers who want to integrate GPU Gaming Advisor into their applications.

## Table of Contents

- [Installation](#installation)
- [Core Classes](#core-classes)
- [GPUDetector](#gpudetector)
- [GameAnalyzer](#gameanalyzer)
- [ClaudeAdvisor](#claudeadvisor)
- [FPSPredictor](#fpredictor)
- [GPUMonitor](#gpumonitor)
- [Data Classes](#data-classes)
- [Utilities](#utilities)

## Installation

```python
# Install the package
pip install gpu-gaming-advisor

# Or for development
pip install -e .
```

## Core Classes

### Quick Import

```python
from gpu_gaming_advisor import (
    GPUDetector,
    GPUInfo,
    GameAnalyzer,
    ClaudeAdvisor,
    FPSPredictor,
    GPUMonitor,
)
```

---

## GPUDetector

Detects and retrieves information about installed NVIDIA GPUs.

### Class: `GPUDetector`

```python
from gpu_gaming_advisor import GPUDetector

detector = GPUDetector()
```

### Methods

#### `initialize() -> bool`

Initialize the GPU detection system.

```python
detector = GPUDetector()
success = detector.initialize()
if success:
    print("GPU detection initialized")
```

**Returns:** `bool` - True if initialization was successful

#### `shutdown()`

Clean up resources. Should be called when done.

```python
detector.shutdown()
```

#### `detect_gpus() -> List[GPUInfo]`

Detect all available GPUs.

```python
gpus = detector.detect_gpus()
for gpu in gpus:
    print(f"Found: {gpu.name}")
```

**Returns:** `List[GPUInfo]` - List of detected GPUs

#### `get_primary_gpu() -> Optional[GPUInfo]`

Get the primary (first) GPU.

```python
gpu = detector.get_primary_gpu()
if gpu:
    print(f"Primary GPU: {gpu.name}")
```

**Returns:** `Optional[GPUInfo]` - Primary GPU or None

#### `refresh_gpu_status(gpu_index: int = 0) -> Optional[GPUInfo]`

Refresh the status of a specific GPU.

```python
gpu = detector.refresh_gpu_status(0)
print(f"Temperature: {gpu.temperature}°C")
```

**Parameters:**
- `gpu_index` (int): Index of the GPU to refresh

**Returns:** `Optional[GPUInfo]` - Updated GPU info

### Example Usage

```python
from gpu_gaming_advisor import GPUDetector

detector = GPUDetector()
try:
    if detector.initialize():
        gpu = detector.get_primary_gpu()
        print(f"GPU: {gpu.name}")
        print(f"VRAM: {gpu.vram_total / 1024:.0f} GB")
        print(f"Temperature: {gpu.temperature}°C")
finally:
    detector.shutdown()
```

---

## GameAnalyzer

Analyzes games and their requirements.

### Class: `GameAnalyzer`

```python
from gpu_gaming_advisor import GameAnalyzer

analyzer = GameAnalyzer()
# Or with custom database
analyzer = GameAnalyzer(custom_database_path="path/to/games.json")
```

### Methods

#### `get_game_requirements(game_name: str) -> Optional[GameRequirements]`

Get requirements for a specific game.

```python
req = analyzer.get_game_requirements("Cyberpunk 2077")
if req:
    print(f"Minimum VRAM: {req.minimum_vram} MB")
    print(f"Supports Ray Tracing: {req.supports_raytracing}")
```

**Parameters:**
- `game_name` (str): Name of the game (case-insensitive, partial match supported)

**Returns:** `Optional[GameRequirements]` - Game requirements or None

#### `check_compatibility(gpu_info: GPUInfo, game_name: str) -> Dict[str, Any]`

Check if a GPU is compatible with a game.

```python
result = analyzer.check_compatibility(gpu, "Elden Ring")
print(f"Compatibility: {result['compatible']}")
print(f"Message: {result['message']}")
```

**Parameters:**
- `gpu_info` (GPUInfo): GPU information
- `game_name` (str): Name of the game

**Returns:** `Dict[str, Any]` - Compatibility analysis

#### `list_games() -> List[str]`

Get list of all supported games.

```python
games = analyzer.list_games()
print(f"Total games: {len(games)}")
```

#### `search_games(query: str) -> List[str]`

Search for games by name.

```python
matches = analyzer.search_games("call of duty")
print(f"Found: {matches}")
```

#### `get_games_by_feature(feature: str) -> List[str]`

Get games that support a specific feature.

```python
rt_games = analyzer.get_games_by_feature("raytracing")
dlss_games = analyzer.get_games_by_feature("dlss")
fsr_games = analyzer.get_games_by_feature("fsr")
```

**Parameters:**
- `feature` (str): Feature name ("raytracing", "dlss", or "fsr")

#### `add_game(name: str, requirements: Dict[str, Any])`

Add or update a game in the database.

```python
analyzer.add_game("New Game", {
    "minimum_vram": 4096,
    "recommended_vram": 8192,
    "minimum_gpu": "GTX 1060",
    "recommended_gpu": "RTX 3060",
    "supports_raytracing": True,
    "supports_dlss": True,
    "supports_fsr": True,
    "release_year": 2024,
    "engine": "Unreal Engine 5",
    "optimization_level": "good",
})
```

---

## ClaudeAdvisor

Claude AI integration for gaming optimization advice.

### Class: `ClaudeAdvisor`

```python
from gpu_gaming_advisor import ClaudeAdvisor

advisor = ClaudeAdvisor(api_key="sk-ant-...")
# Or use environment variable
advisor = ClaudeAdvisor()  # Uses ANTHROPIC_API_KEY
```

### Methods

#### `get_optimization_recommendation(...) -> GameRecommendation`

Get optimization recommendations for a specific game.

```python
recommendation = advisor.get_optimization_recommendation(
    gpu_info=gpu,
    game_name="Cyberpunk 2077",
    resolution="1920x1080",
    target_fps=60,
    priority="balanced"  # "quality", "balanced", or "performance"
)

print(f"Settings: {recommendation.settings}")
print(f"Expected FPS: {recommendation.expected_fps_range}")
```

**Parameters:**
- `gpu_info` (GPUInfo): GPU information
- `game_name` (str): Name of the game
- `resolution` (str): Target resolution (default: "1920x1080")
- `target_fps` (int): Target framerate (default: 60)
- `priority` (str): Optimization priority (default: "balanced")

**Returns:** `GameRecommendation` - Optimization recommendations

#### `predict_fps(...) -> Dict[str, Any]`

Predict FPS for a game at specific settings.

```python
prediction = advisor.predict_fps(
    gpu_info=gpu,
    game_name="Fortnite",
    resolution="2560x1440",
    quality_preset="High"
)

print(f"Average FPS: {prediction['fps_average']}")
```

#### `compare_gpus(...) -> Dict[str, Any]`

Compare two GPUs for gaming performance.

```python
comparison = advisor.compare_gpus(
    gpu1_info=gpu,
    gpu2_name="RTX 4070",
    game_name="Elden Ring"  # Optional
)

print(f"Difference: {comparison['performance_difference_percent']}%")
```

#### `chat(...) -> str`

Have an interactive chat about gaming optimization.

```python
response = advisor.chat(
    gpu_info=gpu,
    user_message="What games can I play at 4K?",
    conversation_history=[]  # Optional
)
```

#### `analyze_gpu_health(gpu_info: GPUInfo) -> Dict[str, Any]`

Analyze GPU health and provide recommendations.

```python
health = advisor.analyze_gpu_health(gpu)
print(f"Health: {health['overall_health']}")
```

---

## FPSPredictor

Predicts FPS performance based on GPU and game parameters.

### Class: `FPSPredictor`

```python
from gpu_gaming_advisor import FPSPredictor

predictor = FPSPredictor()
```

### Methods

#### `predict(...) -> FPSPrediction`

Predict FPS for a specific configuration.

```python
prediction = predictor.predict(
    gpu_info=gpu,
    game_name="Cyberpunk 2077",
    resolution="1920x1080",
    quality_preset="high"
)

print(f"Average: {prediction.fps_average}")
print(f"Range: {prediction.fps_min}-{prediction.fps_max}")
print(f"Confidence: {prediction.confidence}")
```

#### `predict_all_presets(...) -> Dict[str, FPSPrediction]`

Predict FPS for all quality presets.

```python
predictions = predictor.predict_all_presets(gpu, "Fortnite", "1920x1080")
for preset, pred in predictions.items():
    print(f"{preset}: {pred.fps_average} FPS")
```

#### `predict_all_resolutions(...) -> Dict[str, FPSPrediction]`

Predict FPS for all common resolutions.

```python
predictions = predictor.predict_all_resolutions(gpu, "Fortnite", "high")
for res, pred in predictions.items():
    print(f"{res}: {pred.fps_average} FPS")
```

#### `find_optimal_settings(...) -> Dict[str, Any]`

Find optimal settings to achieve target FPS.

```python
result = predictor.find_optimal_settings(
    gpu_info=gpu,
    game_name="Cyberpunk 2077",
    target_fps=60,
    prefer_quality=True
)

print(f"Resolution: {result['resolution']}")
print(f"Quality: {result['quality_preset']}")
```

#### `compare_gpus(...) -> Dict[str, Any]`

Compare FPS predictions between two GPUs.

```python
comparison = predictor.compare_gpus(
    gpu1_info=gpu,
    gpu2_name="RTX 4080",
    game_name="Cyberpunk 2077"
)

print(f"Difference: {comparison['fps_difference']} FPS")
```

---

## GPUMonitor

Real-time GPU monitoring with terminal dashboard.

### Class: `GPUMonitor`

```python
from gpu_gaming_advisor import GPUMonitor

monitor = GPUMonitor(refresh_rate=1.0)
```

### Methods

#### `start_monitoring(...)`

Start real-time GPU monitoring with dashboard.

```python
# Monitor indefinitely
monitor.start_monitoring()

# Monitor for 60 seconds
monitor.start_monitoring(duration=60.0)

# With callback
def on_update(gpu_info):
    print(f"Temp: {gpu_info.temperature}")

monitor.start_monitoring(callback=on_update)
```

#### `stop_monitoring()`

Stop the monitoring loop.

```python
monitor.stop_monitoring()
```

#### `get_current_metrics() -> Optional[GPUInfo]`

Get current GPU metrics (single snapshot).

```python
gpu = monitor.get_current_metrics()
print(f"Current temp: {gpu.temperature}°C")
```

#### `export_session(filepath: str)`

Export session data to JSON.

```python
monitor.export_session("session.json")
```

---

## Data Classes

### GPUInfo

```python
@dataclass
class GPUInfo:
    name: str
    vendor: str = "Unknown"
    vram_total: int = 0  # MB
    vram_used: int = 0  # MB
    vram_free: int = 0  # MB
    cuda_cores: int = 0
    base_clock: int = 0  # MHz
    boost_clock: int = 0  # MHz
    temperature: float = 0.0  # Celsius
    gpu_usage: float = 0.0  # Percentage
    memory_usage: float = 0.0  # Percentage
    power_draw: float = 0.0  # Watts
    power_limit: float = 0.0  # Watts
    driver_version: str = "Unknown"
    architecture: str = "Unknown"
    tier: str = "Unknown"
```

### GameRequirements

```python
@dataclass
class GameRequirements:
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
    optimization_level: str
```

### GameRecommendation

```python
@dataclass
class GameRecommendation:
    game_name: str
    gpu_name: str
    resolution: str
    target_fps: int
    settings: Dict[str, str]
    expected_fps_range: tuple
    tips: List[str]
    confidence: str
```

### FPSPrediction

```python
@dataclass
class FPSPrediction:
    game_name: str
    gpu_name: str
    resolution: str
    quality_preset: str
    fps_min: int
    fps_max: int
    fps_average: int
    fps_1_percent_low: int
    confidence: str
    notes: list
```

---

## Utilities

### Configuration

```python
from gpu_gaming_advisor.utils import load_config, save_config

# Load configuration
config = load_config()
config = load_config("path/to/config.yaml")

# Save configuration
save_config(config)
```

### Profile Export

```python
from gpu_gaming_advisor.utils import export_profile, import_profile

# Export settings profile
path = export_profile(
    profile_name="Cyberpunk High",
    gpu_name="RTX 3070",
    game_name="Cyberpunk 2077",
    settings={"Quality": "High", "DLSS": "Quality"}
)

# Import profile
profile = import_profile("profile.json")
```

---

## Complete Example

```python
from gpu_gaming_advisor import (
    GPUDetector,
    GameAnalyzer,
    ClaudeAdvisor,
    FPSPredictor,
)

# Initialize detector
detector = GPUDetector()
detector.initialize()

try:
    # Get GPU info
    gpu = detector.get_primary_gpu()
    print(f"GPU: {gpu.name}")
    print(f"VRAM: {gpu.vram_total / 1024:.0f} GB")
    
    # Check game compatibility
    analyzer = GameAnalyzer()
    compat = analyzer.check_compatibility(gpu, "Cyberpunk 2077")
    print(f"Compatibility: {compat['compatible']}")
    
    # Predict FPS
    predictor = FPSPredictor()
    prediction = predictor.predict(gpu, "Cyberpunk 2077", "1920x1080", "high")
    print(f"Expected FPS: {prediction.fps_average}")
    
    # Get AI recommendations
    advisor = ClaudeAdvisor()
    rec = advisor.get_optimization_recommendation(
        gpu, "Cyberpunk 2077", "1920x1080", 60
    )
    print(f"Recommended settings: {rec.settings}")
    
finally:
    detector.shutdown()
```
