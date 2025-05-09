from manim import *

class CircleToSquare(Scene):
    def construct(self):
        # Create a circle
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        
        # Create a square
        square = Square()
        square.set_fill(RED, opacity=0.5)
        
        # Add circle to scene
        self.play(Create(circle))
        self.wait(1)
        
        # Transform circle into square
        self.play(Transform(circle, square))
        self.wait(1)
        
        # Fade out the square
        self.play(FadeOut(square))
        self.wait(1)

# To run this, you would need to:
# 1. Install manim: pip install manim
# 2. Run from command line: python -m manim your_file_name.py CircleToSquare -pqh