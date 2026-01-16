"""Setup script for GPU Gaming Advisor."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip()
        for line in fh
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="gpu-gaming-advisor",
    version="1.0.0",
    author="GPU Gaming Advisor Team",
    author_email="contact@gpugamingadvisor.dev",
    description="AI-powered GPU gaming optimization tool using Claude",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gpu-gaming-advisor",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/gpu-gaming-advisor/issues",
        "Documentation": "https://github.com/yourusername/gpu-gaming-advisor#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gpu-advisor=gpu_gaming_advisor.cli:app",
        ],
    },
    include_package_data=True,
    package_data={
        "gpu_gaming_advisor": ["../data/*.json", "../config/*.yaml"],
    },
)
