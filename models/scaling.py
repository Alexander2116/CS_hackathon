from manim import *
import numpy as np
import math 

def spherical_to_cartesian_velocity(vel, coords):
    if len(vel) != 3:
        raise ValueError("Input list should contain 3 elements.")
    
    r, theta, phi = coords
    vr, vtheta, vphi = vel
    vx = vr * math.sin(theta) * math.cos(phi) - vphi * r * math.sin(phi) * math.sin(theta) + r * math.cos(phi) * math.cos(theta) * vtheta
    vy = vr * math.sin(theta) * math.sin(phi) + vtheta * r * math.cos(theta) * math.sin(phi) + r * math.cos(phi) * math.sin(theta) * vphi
    vz = vr * math.cos(theta) - vtheta * r * math.sin(theta)
    return [vx, vy, vz]

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

        # initial positions; NB defines how many objects ve have!
        positions = [
            [1.5, 1.5, 1],
            [1.5, -1.5, -1],
            [2, 1, 1]
        ]
        velocities_spherical = [
            [5, 0, 10],
            [5, 10, 0],
            [1, 4, 7]
        ]
        # masses = [1, 2, 3]
        colours = [BLUE, GREEN, ORANGE]

        # time parameters
        timestep = 0.01
        timeline = np.arange(1, 3, timestep)

        # Create an Earth and Display it on the screen
        earth_radius = 1
        earth = Circle(color=RED, fill_opacity=0.8, radius=earth_radius)
        self.add(earth)

        # create a list for pieces of trash; should have the correct dimensions for indexing purpose
        trash_list = [None for _ in range(len(positions))]
        arrow_list = [None for _ in range(len(positions))]
        pos_sphere = [[None for _ in range(3)] for _ in range(len(positions))]
        for index, pos in enumerate(positions):

            init_pos = pos # initial position of the trash
            pos_sphere[index] = cartesian_to_spherical(pos) # initial position in spherical coordinates
            trash_list[index] = Dot(color=colours[index]).move_to(init_pos) # add a piece of trash for each initial coordinate
            end = [a * 0.05 for a in spherical_to_cartesian_velocity(velocities_spherical[index], pos_sphere[index])]
            arrow_list[index] = Arrow(start=ORIGIN, end=end, color=colours[index])
            arrow_list[index].shift(pos)

        # display trash on the screen
        for trash, arrow in zip(trash_list, arrow_list):
            self.add(trash, arrow)

        # start the time evolution
        for t in timeline:

            # need to update each piece of trash
            for index, trash in enumerate(trash_list):
                r_squared = positions[index][0]**2 + positions[index][1]**2 + positions[index][2]**2
                if np.sqrt(r_squared)<=earth_radius:
                    line = Line(positions[index], positions[index])
                    self.remove(arrow_list[index])
                    self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.01))
                else:
                    z = positions[index][2]
                    if z <= 0:
                        # bring the object behind the earth
                        self.bring_to_front(earth)
                        scale_factor = 1 + z/2
                    else:
                        self.bring_to_front(trash)
                        self.bring_to_front(arrow_list[index])
                        scale_factor = z
                    # get acceleration
                    acceleration_rad = -80/r_squared
                    # update radial velocity
                    velocities_spherical[index][0] = velocities_spherical[index][0] + acceleration_rad * timestep
                    # set initial position for the line
                    pos_0 = positions[index]
                    # update position
                    pos_sphere[index] = [a + b * timestep for a, b in zip(pos_sphere[index], velocities_spherical[index])]
                    # convert to carthesian for the animation
                    positions[index] = spherical_to_cartesian(pos_sphere[index])

                    end = [a * 0.05 for a in spherical_to_cartesian_velocity(velocities_spherical[index], pos_sphere[index])]
                    arrow_list[index].put_start_and_end_on(ORIGIN, end)
                    arrow_list[index].shift(positions[index])

                    line = Line(pos_0, positions[index])
                    trash.scale(scale_factor)
                    self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.01))
                    trash.scale(1/scale_factor)

Example().render()