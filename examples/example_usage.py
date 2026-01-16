#!/usr/bin/env python3
"""
GPU Gaming Advisor - Example Usage

This script demonstrates the main features of GPU Gaming Advisor.
Run with: python examples/example_usage.py
"""

import sys
import os

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gpu_gaming_advisor import (
    GPUDetector,
    GameAnalyzer,
    FPSPredictor,
)


def example_gpu_detection():
    """Example: Detect and display GPU information."""
    print("=" * 60)
    print("Example 1: GPU Detection")
    print("=" * 60)
    
    detector = GPUDetector()
    
    if detector.initialize():
        gpu = detector.get_primary_gpu()
        
        if gpu:
            print(f"\n✓ GPU Detected: {gpu.name}")
            print(f"  - Vendor: {gpu.vendor}")
            print(f"  - VRAM: {gpu.vram_total / 1024:.0f} GB")
            print(f"  - Architecture: {gpu.architecture}")
            print(f"  - CUDA Cores: {gpu.cuda_cores:,}")
            print(f"  - Performance Tier: {gpu.tier}")
            print(f"  - Driver: {gpu.driver_version}")
            print(f"\n  Current Status:")
            print(f"  - Temperature: {gpu.temperature}°C")
            print(f"  - GPU Usage: {gpu.gpu_usage}%")
            print(f"  - VRAM Used: {gpu.vram_used / 1024:.1f} GB")
        else:
            print("No GPU detected. Running in simulation mode.")
            # Create a simulated GPU for demonstration
            from gpu_gaming_advisor.gpu_detector import GPUInfo
            gpu = GPUInfo(
                name="NVIDIA GeForce RTX 3070 (Simulated)",
                vendor="NVIDIA",
                vram_total=8192,
                cuda_cores=5888,
                architecture="Ampere",
                tier="High-End",
            )
            print(f"\n📋 Using simulated GPU: {gpu.name}")
        
        detector.shutdown()
        return gpu
    else:
        print("Failed to initialize GPU detector")
        return None


def example_game_analysis(gpu):
    """Example: Analyze game compatibility."""
    print("\n" + "=" * 60)
    print("Example 2: Game Analysis")
    print("=" * 60)
    
    analyzer = GameAnalyzer()
    
    # List some supported games
    games = analyzer.list_games()
    print(f"\n📚 Total games in database: {len(games)}")
    print(f"   Sample games: {', '.join(games[:5])}...")
    
    # Check compatibility for a specific game
    game = "Cyberpunk 2077"
    print(f"\n🎮 Checking compatibility for: {game}")
    
    result = analyzer.check_compatibility(gpu, game)
    print(f"   Compatibility: {result['compatible']}")
    print(f"   Message: {result['message']}")
    
    if 'features' in result:
        print(f"   Features:")
        for feature in result['features']:
            print(f"     - {feature}")
    
    # Get game requirements
    req = analyzer.get_game_requirements(game)
    if req:
        print(f"\n   Game Requirements:")
        print(f"     - Minimum VRAM: {req.minimum_vram / 1024:.0f} GB")
        print(f"     - Recommended VRAM: {req.recommended_vram / 1024:.0f} GB")
        print(f"     - Recommended GPU: {req.recommended_gpu}")
        print(f"     - Engine: {req.engine}")
    
    # Search for games with specific features
    print(f"\n🔍 Games with Ray Tracing support:")
    rt_games = analyzer.get_games_by_feature("raytracing")
    print(f"   {', '.join(rt_games[:5])}...")
    
    return analyzer


def example_fps_prediction(gpu):
    """Example: Predict FPS for games."""
    print("\n" + "=" * 60)
    print("Example 3: FPS Prediction")
    print("=" * 60)
    
    predictor = FPSPredictor()
    
    # Predict FPS for a single game
    game = "Cyberpunk 2077"
    resolution = "1920x1080"
    quality = "high"
    
    print(f"\n📊 FPS Prediction for {game}")
    print(f"   Resolution: {resolution}")
    print(f"   Quality: {quality}")
    
    prediction = predictor.predict(gpu, game, resolution, quality)
    print(f"\n   Results:")
    print(f"     - Average FPS: {prediction.fps_average}")
    print(f"     - FPS Range: {prediction.fps_min} - {prediction.fps_max}")
    print(f"     - 1% Low: {prediction.fps_1_percent_low}")
    print(f"     - Confidence: {prediction.confidence}")
    
    if prediction.notes:
        print(f"\n   Notes:")
        for note in prediction.notes:
            print(f"     - {note}")
    
    # Predict for all quality presets
    print(f"\n📈 FPS at all quality presets ({resolution}):")
    all_presets = predictor.predict_all_presets(gpu, game, resolution)
    for preset, pred in all_presets.items():
        print(f"     {preset.capitalize():8} → {pred.fps_average:3} FPS")
    
    # Predict for all resolutions
    print(f"\n📈 FPS at all resolutions (High quality):")
    all_res = predictor.predict_all_resolutions(gpu, game, "high")
    for res, pred in all_res.items():
        print(f"     {res:12} → {pred.fps_average:3} FPS")
    
    # Find optimal settings
    print(f"\n🎯 Finding optimal settings for 60 FPS target:")
    optimal = predictor.find_optimal_settings(gpu, game, target_fps=60, prefer_quality=True)
    print(f"     Resolution: {optimal['resolution']}")
    print(f"     Quality: {optimal['quality_preset']}")
    print(f"     Expected FPS: {optimal['prediction'].fps_average}")
    
    return predictor


def example_gpu_comparison(gpu):
    """Example: Compare GPUs."""
    print("\n" + "=" * 60)
    print("Example 4: GPU Comparison")
    print("=" * 60)
    
    predictor = FPSPredictor()
    
    compare_to = "RTX 4070"
    game = "Cyberpunk 2077"
    
    print(f"\n🔄 Comparing {gpu.name} vs {compare_to}")
    print(f"   Game: {game}")
    
    comparison = predictor.compare_gpus(gpu, compare_to, game)
    
    print(f"\n   Results:")
    print(f"     Your GPU ({comparison['gpu1_name']}): {comparison['gpu1_fps']} FPS")
    print(f"     {comparison['gpu2_name']}: {comparison['gpu2_fps']} FPS")
    print(f"     Difference: {comparison['fps_difference']:+d} FPS ({comparison['percentage_difference']:+.1f}%)")
    print(f"     Faster GPU: {comparison['faster_gpu']}")


def example_multiple_games(gpu):
    """Example: Analyze multiple games."""
    print("\n" + "=" * 60)
    print("Example 5: Multiple Games Analysis")
    print("=" * 60)
    
    predictor = FPSPredictor()
    
    games = [
        "Fortnite",
        "Valorant",
        "Counter-Strike 2",
        "Elden Ring",
        "Cyberpunk 2077",
        "Alan Wake 2",
    ]
    
    print(f"\n📊 FPS predictions at 1080p High:")
    print(f"\n   {'Game':<20} {'Avg FPS':>8} {'Confidence':>12}")
    print("   " + "-" * 42)
    
    for game in games:
        pred = predictor.predict(gpu, game, "1920x1080", "high")
        print(f"   {game:<20} {pred.fps_average:>8} {pred.confidence:>12}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("   GPU Gaming Advisor - Example Usage")
    print("=" * 60)
    
    # Example 1: GPU Detection
    gpu = example_gpu_detection()
    
    if not gpu:
        # Create simulated GPU if detection failed
        from gpu_gaming_advisor.gpu_detector import GPUInfo
        gpu = GPUInfo(
            name="NVIDIA GeForce RTX 3070 (Simulated)",
            vendor="NVIDIA",
            vram_total=8192,
            cuda_cores=5888,
            architecture="Ampere",
            tier="High-End",
        )
    
    # Example 2: Game Analysis
    example_game_analysis(gpu)
    
    # Example 3: FPS Prediction
    example_fps_prediction(gpu)
    
    # Example 4: GPU Comparison
    example_gpu_comparison(gpu)
    
    # Example 5: Multiple Games
    example_multiple_games(gpu)
    
    print("\n" + "=" * 60)
    print("   Examples completed!")
    print("=" * 60)
    print("\nFor AI-powered recommendations, run:")
    print("  python -m gpu_gaming_advisor interactive")
    print("\nOr get specific game recommendations:")
    print("  python -m gpu_gaming_advisor optimize 'Cyberpunk 2077'")
    print()


if __name__ == "__main__":
    main()
