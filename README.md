# GravitySim
A fun little gravity simulator :]



## Running The Gravity Simulator
Windows: run the executable file found in /output/grav_sim.exe

On Alternate OS: install pygame module found [here](https://www.pygame.org/wiki/GettingStarted) and run the grav_sim.py script


## Project Description
This program simulates Newtonian Gravity in **python** using the **pygame module**. This was just a fun project to make using 
simple game design elements. I wanted to make something that looked visually interesting and challenging.

### Algorithm / Runtime
This program uses the most intuitive solution to the N - Body Simulation Problem which compares the gravitational force of each body
on each other at each time step. The sum of these forces affect the acceleration of each body which affects its position at each time step.
Program Runtime of this algorithm is simply O(n^2) n is the number of celestial bodies.

Upon collision a body is chosen to continue forward so we can avoid overlapping of bodies and clean up the simulation with successful orbits.






---
### The Simulators Current Presets:
- 1 Dense Large Mass with an absolute position in the center
- 50 Smaller Masses with randomly generated positions and velocities
- Custom Gravitational Constant and other Gravity Properties
