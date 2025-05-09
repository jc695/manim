from manim import *

class ContainersAndKubernetes(Scene):
    def construct(self):
        # Title
        title = Text("Containers & Kubernetes", font_size=40)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # Step 1: Show a single Docker container
        container = Rectangle(width=2, height=1.5, color=BLUE, fill_opacity=0.2)
        app_label = Text("App", font_size=24).move_to(container.get_center())
        container_group = VGroup(container, app_label)
        container_label = Text("Docker Container", font_size=24).next_to(container, DOWN)
        
        self.play(Create(container), Write(app_label), Write(container_label))
        self.wait(1)
        
        # Step 2: Show multiple containers (scaling)
        container2 = container_group.copy().shift(RIGHT * 3)
        container3 = container_group.copy().shift(RIGHT * 6)
        scaling_text = Text("Multiple Containers (Docker)", font_size=30).next_to(container2, UP, buff=1)
        
        self.play(Create(container2), Create(container3), FadeOut(container_label))
        self.play(Write(scaling_text))
        self.wait(1)
        
        # Step 3: Introduce Kubernetes as orchestrator
        k8s_box = Rectangle(width=8, height=1, color=GREEN, fill_opacity=0.2).shift(UP * 2.5)
        k8s_label = Text("Kubernetes", font_size=30).move_to(k8s_box.get_center())
        arrows = VGroup(
            Arrow(k8s_box.get_bottom(), container.get_top(), color=YELLOW),
            Arrow(k8s_box.get_bottom(), container2.get_top(), color=YELLOW),
            Arrow(k8s_box.get_bottom(), container3.get_top(), color=YELLOW)
        )
        
        self.play(Create(k8s_box), Write(k8s_label), scaling_text.animate.shift(DOWN * 3))
        self.play(Create(arrows))
        self.wait(1)
        
        # Final explanation
        relation_text = Text("Docker builds containers, Kubernetes manages them", font_size=24).to_edge(DOWN)
        self.play(Write(relation_text))
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(VGroup(title, container_group, container2, container3, scaling_text, k8s_box, k8s_label, arrows, relation_text)))

# To run this, use: manim -pql script_name.py ContainersAndKubernetes