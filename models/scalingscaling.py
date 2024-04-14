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

class Example1(Scene):
    def construct(self):

        # Create a circle Mobject
        earth_radius = 1
        earth = Circle(color=RED, fill_opacity=1, radius=earth_radius)

        # Display the circle on the screen
        self.add(earth)

        init_pos = [1.5, 1.5, 1] #initial position of the trash
        trash = Dot(color=BLUE).move_to(init_pos)
        self.add(trash)

        # time parameters
        timestep = 0.01
        timeline = np.arange(1, 2.5, timestep)

        # convert to spherical coordinates
        vel_sphere = [5, 10, 0] # forget the carthesian one for now
        pos_sphere = cartesian_to_spherical(init_pos)

        arrow = Arrow(start=ORIGIN, end=spherical_to_cartesian_velocity(vel_sphere, pos_sphere), color=BLUE)
        self.add(arrow)

        # initialise the position
        pos_cartes = init_pos
        for t in timeline:
            r_squared = pos_cartes[0]**2 + pos_cartes[1]**2 + pos_cartes[2]**2
            if np.sqrt(r_squared)<=earth_radius:
                line = Line(pos_cartes, pos_cartes)
                self.remove(arrow)
                self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.03))

            else:
                z = pos_cartes[2]
                if z <= 0:
                    self.bring_to_front(earth)
                    # get acceleration
                    acceleration_rad = -80/r_squared
                    #update 
                    vel_sphere[0] = vel_sphere[0] + acceleration_rad * timestep
                    end = [a * 0.05 for a in spherical_to_cartesian_velocity(vel_sphere, pos_sphere)]
                    arrow.put_start_and_end_on(ORIGIN, end)
                    arrow.shift(pos_cartes)

                    pos_0 = pos_cartes
                    pos_sphere = [a + b * timestep for a, b in zip(pos_sphere, vel_sphere)]
                    pos_cartes = spherical_to_cartesian(pos_sphere)
                    line = Line(pos_0, pos_cartes)
                    scale_factor = 1 + z/4
                    trash.scale(scale_factor)
                    #self.play(trash.animate.scale(1.1))
                    self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.03))
                    trash.scale(1/scale_factor)
                    
                # elif z == 0:
                #     # get acceleration
                #     acceleration_rad = -80/r_squared
                #     #update 
                #     vel_sphere[0] = vel_sphere[0] + acceleration_rad * timestep
                #     end = [a * 0.05 for a in spherical_to_cartesian_velocity(vel_sphere, pos_sphere)]
                #     arrow.put_start_and_end_on(ORIGIN, end)
                #     arrow.shift(pos_cartes)

                #     pos_0 = pos_cartes
                #     pos_sphere = [a + b * timestep for a, b in zip(pos_sphere, vel_sphere)]
                #     pos_cartes = spherical_to_cartesian(pos_sphere)
                #     line = Line(pos_0, pos_cartes)
                #     #self.play(trash.animate.scale(1.1))
                #     self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.03))

                else:
                    self.bring_to_front(trash)
                    self.bring_to_front(arrow)
                    # get acceleration
                    acceleration_rad = -80/r_squared
                    #update 
                    vel_sphere[0] = vel_sphere[0] + acceleration_rad * timestep
                    end = [a * 0.05 for a in spherical_to_cartesian_velocity(vel_sphere, pos_sphere)]
                    arrow.put_start_and_end_on(ORIGIN, end)
                    arrow.shift(pos_cartes)

                    pos_0 = pos_cartes
                    pos_sphere = [a + b * timestep for a, b in zip(pos_sphere, vel_sphere)]
                    pos_cartes = spherical_to_cartesian(pos_sphere)
                    line = Line(pos_0, pos_cartes)
                    scale_factor = z
                    trash.scale(scale_factor)
                    #self.play(trash.animate.scale(1.1))
                    self.play(MoveAlongPath(trash, line, rate_func=linear, run_time=0.03))
                    trash.scale(1/scale_factor)
Example1().render()