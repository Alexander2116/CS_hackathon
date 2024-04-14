from manim import *
import numpy as np
import math 
def cartesian_to_spherical(coords):
    if len(coords) != 3:
        raise ValueError("Input list should contain 3 elements.")

    x, y, z = coords
    r = math.sqrt(x**2 + y**2 + z**2)

        # Check if r is zero to avoid division by zero
    if r == 0:
        print("Warning: Cartesian coordinates result in r = 0.")
        return [0, 0, 0]

    theta = math.acos(z / r)
    phi = math.atan2(y, x)
    return [r, theta, phi]

def spherical_to_cartesian(coords):
    if len(coords) != 3:
        raise ValueError("Input list should contain 3 elements.")
    
    r, theta, phi = coords
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    return [x, y, z]

class Example(Scene):
    def construct(self):

        # initial parameters
        positions = [
            [1.5, 1.5, 1],
            [1.5, -1.5, -1],
            [2, 1, 1]
        ]
        velocities_spherical = [
            [5, 0, 10],
            [0, 0, 0],
            [1, 2, 1]
        ]
        colours = [BLUE, GREEN, ORANGE]
        #TODO: for negative z values the dot should go behind the earth
        #TODO: apply for multiple objects 

        # time parameters
        timestep = 0.01
        timeline = np.arange(1, 2, timestep)

        # Create a circle Mobject
        earth_radius = 1
        earth = Circle(radius=earth_radius)
        # Display the circle on the screen
        self.add(earth)

        trash_list = [None for _ in range(len(positions))]
        pos_sphere = [[None for _ in range(3)] for _ in range(len(positions))]
        for index, pos in enumerate(positions):

            init_pos = pos #initial position of the trash
            pos_sphere[index] = cartesian_to_spherical(pos)
            trash_list[index] = Dot(color=colours[index]).move_to(init_pos)
        
        for trash in trash_list:
            self.add(trash)

        for t in timeline:
            for index, trash in enumerate(trash_list):
                r_squared = positions[index][0]**2 + positions[index][1]**2 + positions[index][2]**2
                if np.sqrt(r_squared)<=earth_radius:
                    line = Line(positions[index], positions[index])
                    self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.03))
                else:
                    # get acceleration
                    acceleration_rad = -80/r_squared
                    #update 
                    velocities_spherical[index][0] = velocities_spherical[index][0] + acceleration_rad * timestep
                    
                    pos_0 = positions[index]
                    pos_sphere[index] = [a + b * timestep for a, b in zip(pos_sphere[index], velocities_spherical[index])]
                    positions[index] = spherical_to_cartesian(pos_sphere[index])

                    line = Line(pos_0, positions[index])
                    self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.03))