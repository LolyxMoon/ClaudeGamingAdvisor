"""
Utility Functions Module.

This module provides various utility functions used across
the GPU Gaming Advisor application.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def get_config_path() -> Path:
    """Get the configuration file path."""
    # Check for config in current directory
    local_config = Path("config.yaml")
    if local_config.exists():
        return local_config
    
    # Check for config in user's home directory
    home_config = Path.home() / ".gpu-gaming-advisor" / "config.yaml"
    if home_config.exists():
        return home_config
    
    # Check for config in package directory
    package_config = Path(__file__).parent.parent.parent / "config" / "default_config.yaml"
    if package_config.exists():
        return package_config
    
    # Return default location
    return local_config


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file.
    
    Args:
        config_path: Optional path to config file. If None, uses default locations.
        
    Returns:
        Configuration dictionary.
    """
    if config_path:
        path = Path(config_path)
    else:
        path = get_config_path()
    
    default_config = {
        "anthropic": {
            "api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
            "model": "claude-sonnet-4-20250514",
        },
        "monitoring": {
            "refresh_rate": 1.0,
            "log_metrics": False,
        },
        "preferences": {
            "target_fps": 60,
            "priority": "balanced",
            "resolution": "1920x1080",
        },
    }
    
    if path.exists():
        try:
            with open(path, 'r') as f:
                file_config = yaml.safe_load(f) or {}
            
            # Merge with defaults
            config = deep_merge(default_config, file_config)
            
            # Handle environment variable substitution
            config = substitute_env_vars(config)
            
            return config
        except (yaml.YAMLError, IOError) as e:
            print(f"Warning: Could not load config from {path}: {e}")
    
    return default_config


def save_config(config: Dict[str, Any], config_path: Optional[str] = None):
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary.
        config_path: Optional path to save config. If None, uses default location.
    """
    if config_path:
        path = Path(config_path)
    else:
        path = Path.home() / ".gpu-gaming-advisor" / "config.yaml"
    
    # Create directory if needed
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)


def deep_merge(base: Dict, override: Dict) -> Dict:
    """
    Deep merge two dictionaries.
    
    Args:
        base: Base dictionary.
        override: Dictionary with values to override.
        
    Returns:
        Merged dictionary.
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def substitute_env_vars(config: Dict) -> Dict:
    """
    Substitute environment variables in config values.
    
    Supports ${VAR_NAME} syntax.
    
    Args:
        config: Configuration dictionary.
        
    Returns:
        Configuration with substituted values.
    """
    result = {}
    
    for key, value in config.items():
        if isinstance(value, dict):
            result[key] = substitute_env_vars(value)
        elif isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            var_name = value[2:-1]
            result[key] = os.environ.get(var_name, "")
        else:
            result[key] = value
    
    return result


def parse_resolution(resolution_str: str) -> tuple:
    """
    Parse resolution string to width and height.
    
    Args:
        resolution_str: Resolution string (e.g., "1920x1080").
        
    Returns:
        Tuple of (width, height).
    """
    try:
        parts = resolution_str.lower().split('x')
        return (int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return (1920, 1080)


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human-readable string.
    
    Args:
        bytes_value: Number of bytes.
        
    Returns:
        Formatted string (e.g., "8.0 GB").
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(bytes_value) < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"


def format_fps(fps: float) -> str:
    """
    Format FPS with appropriate color hint.
    
    Args:
        fps: Frames per second.
        
    Returns:
        Formatted string with color info.
    """
    if fps >= 60:
        return f"[green]{fps:.0f} FPS[/]"
    elif fps >= 30:
        return f"[yellow]{fps:.0f} FPS[/]"
    else:
        return f"[red]{fps:.0f} FPS[/]"


def validate_api_key(api_key: str) -> bool:
    """
    Validate Anthropic API key format.
    
    Args:
        api_key: API key to validate.
        
    Returns:
        True if valid format, False otherwise.
    """
    if not api_key:
        return False
    
    # Basic format check (starts with sk-ant-)
    if api_key.startswith("sk-ant-"):
        return True
    
    return False


def get_data_directory() -> Path:
    """Get the data directory path."""
    # Check for data in package directory
    package_data = Path(__file__).parent.parent.parent / "data"
    if package_data.exists():
        return package_data
    
    # Use user's home directory
    user_data = Path.home() / ".gpu-gaming-advisor" / "data"
    user_data.mkdir(parents=True, exist_ok=True)
    return user_data


def export_profile(
    profile_name: str,
    gpu_name: str,
    game_name: str,
    settings: Dict[str, Any],
    output_path: Optional[str] = None
) -> str:
    """
    Export a settings profile to JSON.
    
    Args:
        profile_name: Name for the profile.
        gpu_name: GPU name.
        game_name: Game name.
        settings: Settings dictionary.
        output_path: Optional output path.
        
    Returns:
        Path to the exported file.
    """
    from datetime import datetime
    
    profile = {
        "name": profile_name,
        "created_at": datetime.now().isoformat(),
        "gpu": gpu_name,
        "game": game_name,
        "settings": settings,
    }
    
    if output_path:
        path = Path(output_path)
    else:
        profiles_dir = get_data_directory() / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(c if c.isalnum() else "_" for c in profile_name)
        path = profiles_dir / f"{safe_name}.json"
    
    with open(path, 'w') as f:
        json.dump(profile, f, indent=2)
    
    return str(path)


def import_profile(profile_path: str) -> Dict[str, Any]:
    """
    Import a settings profile from JSON.
    
    Args:
        profile_path: Path to the profile JSON file.
        
    Returns:
        Profile dictionary.
    """
    with open(profile_path, 'r') as f:
        return json.load(f)


class ProgressTracker:
    """Simple progress tracking utility."""
    
    def __init__(self, total: int, description: str = "Processing"):
        """
        Initialize progress tracker.
        
        Args:
            total: Total number of items.
            description: Description of the task.
        """
        self.total = total
        self.current = 0
        self.description = description
    
    def update(self, increment: int = 1):
        """Update progress."""
        self.current += increment
    
    @property
    def percentage(self) -> float:
        """Get current percentage."""
        return (self.current / self.total * 100) if self.total > 0 else 0
    
    def __str__(self) -> str:
        """Get progress string."""
        return f"{self.description}: {self.current}/{self.total} ({self.percentage:.1f}%)"
