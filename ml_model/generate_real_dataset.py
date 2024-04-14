import numpy as np
import math
import csv
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

def spherical_to_cartesian_velocity(vel, coords):
    if len(vel) != 3:
        raise ValueError("Input list should contain 3 elements.")
    
    r, theta, phi = coords
    vr, vtheta, vphi = vel
    vx = vr * math.sin(theta) * math.cos(phi) - vphi * r * math.sin(theta) * math.sin(phi) + vtheta * r * math.cos(theta) * math.cos(phi)
    vy = vr * math.sin(theta) * math.sin(phi) + vtheta * r * math.cos(theta) * math.sin(phi) + vphi * r * math.sin(theta) * math.cos(phi)
    vz = vr * math.cos(theta) - vtheta * r * math.sin(theta)
    return [vx, vy, vz]

def ra_dec_to_cartesian(coords):
    r = 1 #change if earth radius changes
    ra,dec = coords
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)
    
    # Convert to spherical coordinates
    theta = np.pi/2 - dec_rad
    phi = ra_rad
    
    return [r, theta, phi]

def difference_between_objects(coords_list,trash_number):
    difference_between_rocket_trash = np.zeros((trash_number))
    for trash in range(trash_number):
        difference_between_rocket_trash[trash] = np.abs(np.sqrt(coords_list[-1][0]**2+coords_list[-1][1]**2+coords_list[-1][2]**2) - np.sqrt(coords_list[trash][0]**2+coords_list[trash][1]**2+coords_list[trash][2]**2))
    return np.mean(difference_between_rocket_trash)

class Example(object):
    def __init__(self):
        self.trash_number = 3
        self.max_trash_number = 10
        # initial parameters
        
        self.initial_positions = [
            [np.random.uniform(-40,40), np.random.uniform(-40,40), np.random.uniform(-40,40)],
            [np.random.uniform(-40,40), np.random.uniform(-40,40), np.random.uniform(-40,40)],
            [np.random.uniform(-40,40), np.random.uniform(-40,40), np.random.uniform(-40,40)]
        ]
        self.positions = self.initial_positions.copy()
        self.initial_velocities = [
            [np.random.uniform(-10,10), np.random.uniform(-10,10), np.random.uniform(-10,10)],
            [np.random.uniform(-10,10), np.random.uniform(-10,10), np.random.uniform(-10,10)],
            [np.random.uniform(-10,10), np.random.uniform(-10,10), np.random.uniform(-10,10)]
        ]
        self.velocities_spherical = self.initial_velocities.copy()
        
        """
        self.initial_positions = [
            [11.9470917115432527,2,8.6053049700144255],
            [20.2509250275769026, 17.108062552027151, 15.403023058681398],
            [3.8201057698650374, -9.31202782292605, -20.9130278558299967]
        ]
        self.positions = self.initial_positions.copy()
        self.initial_velocities = [
            [0.2375451888082769, 0.0, 1.300830492196746],
            [0.47753379820005915, 0.8108062552027151, 0.7927436013105087],
            [-0.7396830108200877, -2.705154781254021, -2.339597421832245]
        ]
        self.velocities_spherical = self.initial_velocities.copy()
        """
        #TODO: for negative z values the dot should go behind the earth
        #TODO: apply for multiple objects 

        # time parameters
        self.timestep = 0.01
        self.timeline = np.arange(self.timestep, 60, self.timestep)

        #set the radius to one for simplicity
        self.earth_radius = 1

        self.trash_list = [None for _ in range(self.trash_number)]
        self.pos_sphere = [[None for _ in range(3)] for _ in range(self.trash_number)]
        for index, pos in enumerate(self.positions):
            init_pos = pos #initial position of the trash
            self.pos_sphere[index] = cartesian_to_spherical(pos)
        #Initialise the rocket at random ra and dec
        self.RA = np.random.uniform(0,359)
        self.DEC = np.random.uniform(-90,90)
        self.rocket_init_pos = ra_dec_to_cartesian([self.RA,self.DEC])
        #Give the rocket a random starting velocity
        self.rocket_vel = [4,0,0]#= spherical_to_cartesian_velocity([5,0,0],self.rocket_init_pos)

    def calculate_orbits(self,number_of_time_trials):
        #initialise array to save time of rocket launch and min radial distance
        rocket_launch_times_and_minimum_distances = np.zeros((number_of_time_trials,2))
        for index_rocket_launch_time, rocket_launch_time in enumerate(np.arange(0.1,0.1*number_of_time_trials)):
            # initialise array to save difference between pos vector of trash and rocket
            distance_rocket_trash = np.zeros((len(self.timeline)))
            # initialise the position
            rocket_pos_cartes = self.rocket_init_pos
            rocket_pos = cartesian_to_spherical(rocket_pos_cartes)
            has_rocket_launched_yet = False #initialise the rocket launch variable to False at the beginning

            #Iterate through all time steps
            for index_t, t in enumerate(self.timeline):
                #At each time step, update all trash positions
                for index, trash in enumerate(self.trash_list):
                    r_squared = self.positions[index][0]**2 + self.positions[index][1]**2 + self.positions[index][2]**2
                    if np.sqrt(r_squared)<=1: # Change number 1 if Earth radius changes
                        self.pos_sphere[index] = self.pos_sphere[index]
                    else:
                        # get acceleration
                        acceleration_rad = -(80)/r_squared
                        #update 
                        self.velocities_spherical[index][0] = self.velocities_spherical[index][0] + acceleration_rad * self.timestep
                        
                        self.pos_sphere[index] = [a + b * self.timestep for a, b in zip(self.pos_sphere[index], self.velocities_spherical[index])]
                        self.positions[index] = spherical_to_cartesian(self.pos_sphere[index])
                #Check whether the rocket launch time is larger than the time step
                if rocket_launch_time < t:
                    if has_rocket_launched_yet == False:
                        #print('YYYAAAAASSSS QUEEEEEEEN',index_t)
                        index_t_launch = index_t
                    has_rocket_launched_yet = True

                #If the rocket started moving, update its position
                if has_rocket_launched_yet:
                    rocket_r_squared = rocket_pos_cartes[0]**2+rocket_pos_cartes[1]**2+rocket_pos_cartes[2]**2
                    rocket_acceleration_rad = 0 #-80/rocket_r_squared
                    self.rocket_vel[0] = self.rocket_vel[0] + rocket_acceleration_rad * self.timestep
                    rocket_pos = [a + b * self.timestep for a, b in zip(rocket_pos, self.rocket_vel)]
                    #print(rocket_pos)
                    rocket_pos_cartes = spherical_to_cartesian(rocket_pos)
                    #Calculate average distance between the rocket and the trash
                    list_for_distance_calculation = self.positions + [rocket_pos_cartes]
                    distance_rocket_trash[index_t] = difference_between_objects(list_for_distance_calculation,self.trash_number)
            #After the time step looping, find the minimum average distance from the rocket to trash across the rocket launch
            #print(np.min(distance_rocket_trash[index_t_launch::]))
            #print(np.where(distance_rocket_trash[index_t_launch::]==np.min(distance_rocket_trash[index_t_launch])),has_rocket_launched_yet)
            index_minimum_distance = np.where(distance_rocket_trash[index_t_launch::] == np.min(distance_rocket_trash[index_t_launch::]))[0][0]
            rocket_launch_times_and_minimum_distances[index_rocket_launch_time] = [self.timeline[index_minimum_distance],np.min(distance_rocket_trash)]
        self.time_label = rocket_launch_times_and_minimum_distances[np.where(rocket_launch_times_and_minimum_distances[::,1]==np.max(rocket_launch_times_and_minimum_distances[::,1]))[0][0]][0]

    def generate_dataset(self,number_of_time_trials):
        self.calculate_orbits(number_of_time_trials)
        row=[]
        self.pos_sphere = [[None for _ in range(3)] for _ in range(self.trash_number)]
        for index, pos in enumerate(self.initial_positions):
            self.pos_sphere[index] = cartesian_to_spherical(pos)
        self.vel_sphere = [[None for _ in range(3)] for _ in range(self.trash_number)]
        for index, vel in enumerate(self.initial_velocities):
            self.vel_sphere[index] = vel
        row.append(self.RA)
        row.append(self.DEC)
        for i in range(self.trash_number):
            row.append(self.pos_sphere[i][0])
            row.append(self.pos_sphere[i][1])
            row.append(self.pos_sphere[i][2])
            row.append(self.vel_sphere[i][0])
            row.append(self.vel_sphere[i][1])
            row.append(self.vel_sphere[i][2])
        for i in range(self.trash_number - self.max_trash_number):
            row.append(0)
            row.append(0)
            row.append(0)
        row.append(self.time_label)
        return row

def generate_row(number_of_time_trials):
    example = Example()
    row = example.generate_dataset(number_of_time_trials)
    return row

number_of_rows = 100
number_of_time_trials = 500

examples_row = [generate_row(number_of_time_trials) for _ in range(number_of_rows)]

# Define the CSV file name
csv_file = "test_data.csv"

# Write rows to the CSV file
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(examples_row)




