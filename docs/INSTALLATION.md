# Installation Guide

This guide covers the installation process for GPU Gaming Advisor on different platforms.

## Table of Contents

- [Requirements](#requirements)
- [Quick Install](#quick-install)
- [Detailed Installation](#detailed-installation)
- [Platform-Specific Notes](#platform-specific-notes)
- [Troubleshooting](#troubleshooting)

## Requirements

### Hardware
- NVIDIA GPU (GTX 600 series or newer)
- At least 4GB RAM
- 100MB free disk space

### Software
- Python 3.8 or higher
- NVIDIA GPU drivers (latest recommended)
- pip (Python package manager)

### API Key
- Anthropic API key for Claude AI integration
- Get your key at: https://console.anthropic.com/

## Quick Install

```bash
# Clone and install
git clone https://github.com/yourusername/gpu-gaming-advisor.git
cd gpu-gaming-advisor
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Verify installation
python -m gpu_gaming_advisor version
```

## Detailed Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/gpu-gaming-advisor.git
cd gpu-gaming-advisor
```

### Step 2: Create Virtual Environment (Recommended)

Using a virtual environment keeps dependencies isolated.

**On Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

For development (includes testing tools):
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black isort mypy
```

### Step 4: Configure API Key

**Option A: Environment Variable (Recommended)**

Linux/macOS:
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

Windows Command Prompt:
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Windows PowerShell:
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Option B: Configuration File**

Create `config.yaml` in the project root:
```yaml
anthropic:
  api_key: sk-ant-your-key-here
```

**Option C: .env File**

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` and add your key:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Step 5: Verify Installation

```bash
# Check version
python -m gpu_gaming_advisor version

# Test GPU detection
python -m gpu_gaming_advisor analyze

# Run tests (optional)
pytest
```

## Platform-Specific Notes

### Windows

1. **NVIDIA Drivers**: Download from [NVIDIA's website](https://www.nvidia.com/drivers)
2. **Python**: Download from [python.org](https://www.python.org/downloads/windows/)
3. **PATH**: Ensure Python is added to PATH during installation

### Linux (Ubuntu/Debian)

```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Install NVIDIA drivers (if not installed)
sudo ubuntu-drivers autoinstall
```

### Linux (Fedora/RHEL)

```bash
# Install Python
sudo dnf install python3 python3-pip

# Install NVIDIA drivers (RPM Fusion required)
sudo dnf install akmod-nvidia
```

### macOS

Note: GPU Gaming Advisor is primarily designed for NVIDIA GPUs. macOS support is limited.

```bash
# Install Python via Homebrew
brew install python

# Install dependencies
pip3 install -r requirements.txt
```

## Installing as a Package

For system-wide installation:

```bash
pip install .
```

Or in development mode:

```bash
pip install -e .
```

After installation, you can use:
```bash
gpu-advisor analyze
gpu-advisor optimize "Cyberpunk 2077"
```

## Troubleshooting

### "No GPU detected"

1. Verify NVIDIA drivers are installed:
   ```bash
   nvidia-smi
   ```
2. Check if pynvml can find the GPU:
   ```python
   import pynvml
   pynvml.nvmlInit()
   print(pynvml.nvmlDeviceGetCount())
   ```

### "ANTHROPIC_API_KEY not set"

Ensure your API key is correctly configured:
```bash
echo $ANTHROPIC_API_KEY  # Linux/macOS
echo %ANTHROPIC_API_KEY%  # Windows CMD
```

### Import Errors

If you see import errors, try:
```bash
pip install --upgrade -r requirements.txt
```

### Permission Errors on Linux

If you get permission errors accessing the GPU:
```bash
sudo usermod -aG video $USER
# Log out and back in
```

### SSL Certificate Errors

If you encounter SSL errors:
```bash
pip install --upgrade certifi
```

## Upgrading

To upgrade to the latest version:

```bash
cd gpu-gaming-advisor
git pull
pip install --upgrade -r requirements.txt
```

## Uninstalling

```bash
# If installed as package
pip uninstall gpu-gaming-advisor

# Remove the directory
cd ..
rm -rf gpu-gaming-advisor
```

## Next Steps

After installation, check out:
- [Usage Guide](USAGE.md) - Learn how to use all features
- [API Documentation](API.md) - For developers and advanced users
