from manim import *

class Earth(Scene):   
    def construct(self):
        # Create the object (e.g., a dot)
        obj = Dot(color=BLUE)
        obj.move_to(LEFT)
        
        circle = Circle(radius=1)
        # Create the circular path

        # Animate the object along the circular path
        self.play(Rotating(obj, radians=TAU, about_point=circle.get_center(), run_time=2, rate_func=linear))
        
if __name__ == "__main__":
    # To view the animation, run the script with the command 'manim -pql custom_animation.py CustomAnimation'
    Earth().render()
