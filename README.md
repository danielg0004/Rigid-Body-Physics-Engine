# Rigid Body Physics Simulator
A 3D rigid body physics simulator built from scratch in Python using Pygame, implementing 3D rendering, collision detection, and rigid body physics.

# Key Features
- **Custom 3D Rendering:** Implemenets 3D to 2D projection and vertex and camera rotations (with pitch, yaw, and roll) without relying on external libraries
- **Collision detection and resolution:** Uses axis-alinged bounding box (AABB) for collision detection and implements impulse-based collisions that account for both translational and rotational motion
- **Interactive GUI:** Allows to move/rotate the camera and create/delete new bodies

# How to run
Requires Python 3.10+.
1. Clone the repository. Use git clone https://github.com/danielg0004/Rigid-Body-Physics-Engine to download the code.
2. Install pygame using pip install pygame
3. Run the main.py file
4. Create new bodies by pressing "m." Aditional controls are shown in the terminal when running main.py
