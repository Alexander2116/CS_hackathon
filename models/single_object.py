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

        # # initial parameters
        # positions = [
        #     [3, 3, 3],
        #     [3, -3, 3],
        #     [-2, 1, 3]
        # ]
        # velocities = [
        #     [0, 0, 0],
        #     [0.5, 0, 0],
        #     [0.1, 0.2, 0.3]
        # ]
        # masses = [1, 2, 3]
        #TODO: for negative z values the dot should go behind the earth
        #TODO: apply for multiple objects 

        # Create a circle Mobject
        earth_radius = 1
        earth = Circle(radius=earth_radius)

        # Display the circle on the screen
        self.add(earth)

        init_pos = [1.5, 1.5, 1] #initial position of the trash
        init_vel = [0, 0, 0] #initial velocity of the trash, otherwise should be small (0-1 probably)
        trash = Dot(color=BLUE).move_to(init_pos)
        self.add(trash)

        # time parameters
        timestep = 0.01
        timeline = np.arange(1, 4, timestep)

        # convert to spherical coordinates
        vel_sphere = [5, 0, 10] # forget the carthesian one for now
        pos_sphere = cartesian_to_spherical(init_pos)

        # initialise the position
        pos_cartes = init_pos
        for t in timeline:
            r_squared = pos_cartes[0]**2 + pos_cartes[1]**2 + pos_cartes[2]**2
            if np.sqrt(r_squared)<=earth_radius:
                line = Line(pos_cartes, pos_cartes)
                self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.03))
            else:    
                # get acceleration
                acceleration_rad = -80/r_squared
                #update 
                vel_sphere[0] = vel_sphere[0] + acceleration_rad * timestep
                
                pos_0 = pos_cartes
                pos_sphere = [a + b * timestep for a, b in zip(pos_sphere, vel_sphere)]

                pos_cartes = spherical_to_cartesian(pos_sphere)

                line = Line(pos_0, pos_cartes)
                self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.03))