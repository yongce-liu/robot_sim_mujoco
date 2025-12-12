#!/usr/bin/env python3
"""Standalone MuJoCo simulator for Unitree G1"""
import sys
from pathlib import Path

# Add sim module to path
sys.path.insert(0, str(Path(__file__).parent))

import yaml

from robot_sim.simulator_factory import SimulatorFactory, init_channel


def main(n_envs=1, use_async_envs: bool = False, 
             publish_images=True, camera_port=5554, cameras=None, **kwargs):
    # Use default values
    publish_images = True
    camera_port = 5554
    cameras = None
    
    # Load config
    config_path = Path(__file__).parent.parent / "configs" / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Override config with default values
    enable_offscreen = publish_images or config.get("ENABLE_OFFSCREEN", False)
    
    print("="*60)
    print("🤖 Starting Unitree G1 MuJoCo Simulator")
    print("="*60)
    print(f"📁 Scene: {config['ROBOT_SCENE']}")
    print(f"⏱️  Timestep: {config['SIMULATE_DT']}s ({int(1/config['SIMULATE_DT'])} Hz)")
    print(f"👁️  Visualization: {'ON' if config.get('ENABLE_ONSCREEN', True) else 'OFF'}")
    
    # Configure cameras if requested
    camera_configs = {}
    if enable_offscreen:
        camera_list = cameras or ["head_camera"]
        for cam_name in camera_list:
            camera_configs[cam_name] = {"height": 480, "width": 640}
        print(f"📷 Cameras: {', '.join(camera_list)} → ZMQ port {camera_port}")
    
    print("="*60)
    
    # Initialize DDS channel
    init_channel(config=config)
    
    # Create simulator
    sim = SimulatorFactory.create_simulator(
        config=config,
        env_name="default",
        onscreen=config.get("ENABLE_ONSCREEN", True),
        offscreen=enable_offscreen,
        camera_configs=camera_configs,
    )
    
    # Start simulator (blocking)
    print("\nSimulator running. Press Ctrl+C to exit.")
    if enable_offscreen and publish_images:
        print(f"Camera images publishing on tcp://localhost:{camera_port}")
    try:
        SimulatorFactory.start_simulator(
            sim,
            as_thread=False,
            enable_image_publish=publish_images,
            camera_port=camera_port,
        )
    except KeyboardInterrupt:
        print("\nShutting down simulator...")
        robot_sim.close()

if __name__ == "__main__":
    main()

