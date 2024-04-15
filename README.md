## Inspiration
We are a group of PhD Physicists.

Space industry is growing developing faster than in many years. Many space agencies from around the globe are deploying space missions such as lunar landing or the launch of satellites. There is also growth in the private space sector, with space missions like NeuraLink from Space X that has the aim to put over 42,000 satellites on orbit. With the growth of space missions, the amount of space debris orbiting the Low Earth Orbit is increasing. This can pose an important risk to all space activities as more satellites are put in orbit around Earth. The likelihood of catastrophic scenarios such as the Kessler syndrome is increasing, which could cease all space activities while posing a serious risk to astronauts. We wanted to contribute to help finding a solution to the space debris problem by creating an interactive animation and simulation of the orbit of small objects around Earth.

The way we choose to visualise our simulation was inspired by the well-known educational YouTube channel about mathematics called 3Blue1Brown, run by Grant Sanderson. His minimalistic and elegant approach inspired us to try out the animation package deployed for Python called manim (maths animation).

## What it does
The user using a GUI can add many different space debris and put them into orbit. The program calculates the geodesics followed under the influence of Earth's gravitational field. The program then exports an animation, which is done using manim, showing a 2D projection of the object orbiting Earth together with its velocity vector. The information on the perpendicular position of the object is given by the scale of the object in the simulation. Furthermore, the initial conditions of the velocities and positions of the debris can be used to predict the time in which a rocket could be launched to minimise the collision probability. This is implemented with a Deep Learning Model that takes into account the launch coordinates and the initial condition of the debris to return the safest launch time.

## How we built it
The main implementation was done in Python. The GUI was implemented using pyqt5. The animation was performed with manim. The neural network was implemented using the pytorch module. We first started writing the simulation code from which the animation can be produced. The GUI was implemented to facilitate user accessibility. Data obtained from the simulations was then used to train the Deep Learning model.

## Challenges we ran into
Using the package manim was quite challenging since we had no experience with it before. We also found quite challenging merging the GUI with the animation. The neural network was quite challenging, since it wasn't very clear how to obtain a good dataset that would allow a good training of the model.

## Accomplishments that we're proud of
The code successfully predicts the geodesics of many space debris around the Earth. The GUI incorporates a click and drag feature to include different objects in the orbit. The animation accurately shows the motions of these objects around Earth. The model gives an approximate estimation for good launching times.

## What we learned
We have learned to produce aesthetically pleasing animations using the manim package. We have also learned to integrate GUI in python with other packages as manim. We also gained a deeper knowledge and more practical experience working with creating the data for neural networks, picking the right architecture and training them.

## What's next for Space trash
The model can be improved to allow for more efficiency in the code, allowing to include many more objects in orbit. The neural network model can be expanded to also allow the user to calculate potential collisions once the rocket is in orbit around Earth. The model could also try predict collisions with the space debris with the idea of helping a potential space debris collector. With a more advanced interface, the model can also be adapted for educational purposes, since it allows the user to explore the law of gravitation interactively.
