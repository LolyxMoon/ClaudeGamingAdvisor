# Contributing to GPU Gaming Advisor

First off, thank you for considering contributing to GPU Gaming Advisor! It's people like you that make this tool better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to a welcoming and inclusive environment. By participating, you are expected to:

- Be respectful and considerate
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/gpu-gaming-advisor.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Push to your fork and submit a pull request

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **System information**: OS, Python version, GPU model
- **Error messages** in full

### Suggesting Features

Feature suggestions are welcome! Please include:

- **Clear description** of the feature
- **Use case** - why would this be useful?
- **Possible implementation** approach (optional)

### Adding Games to Database

Want to add a game to the database? Create a PR with:

```json
{
  "Game Name": {
    "minimum_vram": 4096,
    "recommended_vram": 8192,
    "minimum_gpu": "GTX 1060",
    "recommended_gpu": "RTX 3060",
    "supports_raytracing": true,
    "supports_dlss": true,
    "supports_fsr": true,
    "release_year": 2024,
    "engine": "Engine Name",
    "optimization_level": "good",
    "settings": ["Setting1", "Setting2"]
  }
}
```

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples
- Improve API documentation
- Translate documentation

### Writing Tests

Help improve test coverage:

- Add tests for uncovered code
- Add edge case tests
- Add integration tests

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- (Optional) NVIDIA GPU for full testing

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/gpu-gaming-advisor.git
cd gpu-gaming-advisor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov black isort mypy flake8

# Run tests
pytest

# Run linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/gpu_gaming_advisor --cov-report=html

# Run specific test file
pytest tests/test_game_analyzer.py

# Run specific test
pytest tests/test_game_analyzer.py::TestGameAnalyzer::test_get_game_requirements_exact_match
```

## Style Guidelines

### Python Code Style

We follow PEP 8 with some modifications:

- **Line length**: 100 characters max
- **Formatting**: Use Black for automatic formatting
- **Imports**: Use isort for import sorting
- **Type hints**: Use type hints where practical

```python
# Good
def get_game_requirements(
    self, game_name: str, include_settings: bool = False
) -> Optional[GameRequirements]:
    """
    Get requirements for a specific game.
    
    Args:
        game_name: Name of the game (case-insensitive).
        include_settings: Whether to include available settings.
        
    Returns:
        GameRequirements if found, None otherwise.
    """
    ...
```

### Documentation Style

- Use Google-style docstrings
- Include type information in docstrings
- Provide examples for complex functions

### Pre-commit Checks

Before committing, run:

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check for issues
flake8 src/ tests/
mypy src/gpu_gaming_advisor

# Run tests
pytest
```

## Commit Messages

Follow conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(games): add support for Elden Ring DLC

fix(detector): handle GPU detection timeout

docs(readme): update installation instructions

test(predictor): add tests for edge cases
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**: `pytest`
4. **Format code**: `black src/ tests/` and `isort src/ tests/`
5. **Update CHANGELOG** if applicable
6. **Write clear PR description**:
   - What does this PR do?
   - Why is this change needed?
   - How has it been tested?

### PR Checklist

- [ ] Tests pass locally
- [ ] Code is formatted with Black
- [ ] Imports are sorted with isort
- [ ] No linting errors
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG updated (if needed)

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## Questions?

Feel free to open an issue for any questions about contributing!

Thank you for helping make GPU Gaming Advisor better! 🎮
