from manim import *

class Example(Scene):   
    def construct(self):
        if len(sys.argv) < 5:
            print("Usage: python animate_png.py <image_file_path>")
            sys.exit(1)
        image_name = sys.argv[1]
        pos1 = float(sys.argv[2])
        pos2 = float(sys.argv[3])
        pos3 = float(sys.argv[4])

        # Load PNG image
        obj= ImageMobject("./Objects/icons/" + image_name)
        obj.scale(1)

        self.add(obj)

        # Define target positions and displacement vector
        target_position = (pos1, pos2, pos3)
        displacement_vector = [0.5, 0.5, 0]

        self.play(obj.animate.move_to(target_position))
        for i in range(3):
            self.play(obj.animate.shift(displacement_vector))
        self.play(obj.animate.scale(1.5))
        self.wait()
        
if __name__ == "__main__":
    # To view the animation, run the script with the command 'manim -pql custom_animation.py CustomAnimation'
    Example().render()