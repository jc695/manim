from manim import *

class ConsistentHashingScene(Scene):
    def construct(self):
        # Scene 1: Introduction to the Hash Ring
        hash_ring = Circle(radius=3, color=WHITE)
        hash_ring_label = Text("Hash Ring", font_size=36).next_to(hash_ring, UP)
        positions = [Text(str(i), font_size=24).move_to(hash_ring.point_at_angle(angle))
                     for i, angle in [(0, 0), (256, -PI/2), (512, -PI), (768, -3*PI/2), (1023, 2*PI-0.01)]]
        
        self.play(Create(hash_ring), Write(hash_ring_label))
        self.play(*[FadeIn(pos) for pos in positions])
        arrow = CurvedArrow(hash_ring.get_top(), hash_ring.get_right(), angle=PI/2, color=YELLOW)
        self.play(Create(arrow))
        intro_text = Text("Consistent Hashing uses a virtual ring structure.", font_size=24).to_edge(DOWN)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(arrow), FadeOut(intro_text))

        # Scene 2: Adding Nodes to the Hash Ring
        nodes = [
            (Dot(color=RED).move_to(hash_ring.point_from_proportion(200/1024)), "Node A", 200),
            (Dot(color=BLUE).move_to(hash_ring.point_from_proportion(500/1024)), "Node B", 500),
            (Dot(color=GREEN).move_to(hash_ring.point_from_proportion(800/1024)), "Node C", 800),
        ]
        # Fixed: Unpack node tuple (dot, label, pos) in the list comprehension
        node_labels = [Text(label, font_size=24).next_to(dot, UP+RIGHT, buff=0.2) for dot, label, pos in nodes]
        node_hashes = [Text(f"Hash({label}) = {pos}", font_size=24).to_edge(LEFT) for _, label, pos in nodes]

        for (dot, _, _), label, hash_text in zip(nodes, node_labels, node_hashes):
            self.play(FadeIn(dot), Write(label), Write(hash_text))
            self.wait(1)
            self.play(FadeOut(hash_text))
        node_text = Text("Nodes are hashed and placed on the ring.", font_size=24).to_edge(DOWN)
        self.play(Write(node_text))
        self.wait(2)
        self.play(FadeOut(node_text))

        # Scene 3: Storing a Data Object (Key)
        key_dot = Square(side_length=0.3, color=YELLOW).move_to(hash_ring.point_from_proportion(300/1024))
        key_label = Text("Key: 'xyz'", font_size=24).next_to(key_dot, DOWN+RIGHT, buff=0.2)
        key_hash = Text("Hash('xyz') = 300", font_size=24).to_edge(LEFT)
        self.play(FadeIn(key_dot), Write(key_label), Write(key_hash))
        traversal = CurvedArrow(key_dot.get_center(), nodes[1][0].get_center(), angle=PI/2, color=YELLOW)
        self.play(Create(traversal))
        self.play(key_dot.animate.move_to(nodes[1][0]), key_label.animate.next_to(nodes[1][0], DOWN+RIGHT))
        store_text = Text("Stored on Node B", font_size=24).to_edge(DOWN)
        self.play(Write(store_text), FadeOut(traversal), FadeOut(key_hash))
        self.wait(2)
        self.play(FadeOut(store_text))

        # Scene 4: Retrieving a Data Object
        key_dot.move_to(hash_ring.point_from_proportion(300/1024))
        key_label.next_to(key_dot, DOWN+RIGHT)
        self.play(FadeIn(key_dot), Write(key_label), Write(key_hash))
        traversal = CurvedArrow(key_dot.get_center(), nodes[1][0].get_center(), angle=PI/2, color=YELLOW)
        self.play(Create(traversal))
        retrieve_text = Text("Retrieved from Node B", font_size=24).to_edge(DOWN)
        self.play(Write(retrieve_text), FadeOut(traversal), FadeOut(key_hash))
        self.wait(2)
        self.play(FadeOut(retrieve_text), FadeOut(key_dot), FadeOut(key_label))

        # Scene 5: Node Addition
        node_d = Dot(color=PURPLE).move_to(hash_ring.point_from_proportion(400/1024))
        node_d_label = Text("Node D", font_size=24).next_to(node_d, UP+RIGHT, buff=0.2)
        node_d_hash = Text("Hash(Node D) = 400", font_size=24).to_edge(LEFT)
        self.play(FadeIn(node_d), Write(node_d_label), Write(node_d_hash))
        self.play(FadeIn(key_dot.move_to(hash_ring.point_from_proportion(300/1024))), Write(key_label))
        traversal = CurvedArrow(key_dot.get_center(), node_d.get_center(), angle=PI/4, color=YELLOW)
        self.play(Create(traversal))
        self.play(key_dot.animate.move_to(node_d), key_label.animate.next_to(node_d, DOWN+RIGHT))
        add_text = Text("Adding a node reassigns keys minimally.", font_size=24).to_edge(DOWN)
        self.play(Write(add_text), FadeOut(traversal), FadeOut(node_d_hash))
        self.wait(2)
        self.play(FadeOut(add_text))

        # Scene 6: Node Deletion
        crash_x = Cross(color=RED).move_to(node_d)
        self.play(Create(crash_x))
        self.play(FadeOut(node_d), FadeOut(node_d_label), FadeOut(crash_x))
        traversal = CurvedArrow(key_dot.get_center(), nodes[1][0].get_center(), angle=PI/2, color=YELLOW)
        self.play(Create(traversal))
        self.play(key_dot.animate.move_to(nodes[1][0]), key_label.animate.next_to(nodes[1][0], DOWN+RIGHT))
        del_text = Text("Removing a node shifts keys to the next node.", font_size=24).to_edge(DOWN)
        self.play(Write(del_text), FadeOut(traversal))
        self.wait(2)
        self.play(FadeOut(del_text))

        # Scene 7: Non-Uniform Distribution and Virtual Nodes
        self.play(*[FadeOut(node[0], node_labels[i]) for i, node in enumerate(nodes[1:])])  # Keep only Node A
        nodes = [(nodes[0][0], "Node A", 200)]  # Reset to Node A only
        node_labels = [node_labels[0]]
        new_nodes = [
            (Dot(color=BLUE).move_to(hash_ring.point_from_proportion(210/1024)), "Node B", 210),
            (Dot(color=GREEN).move_to(hash_ring.point_from_proportion(800/1024)), "Node C", 800),
        ]
        new_labels = [Text(label, font_size=24).next_to(dot, UP+RIGHT, buff=0.2) for dot, label, pos in new_nodes]
        self.play(*[FadeIn(node[0], label) for node, label in zip(new_nodes, new_labels)])
        keys = [Square(side_length=0.3, color=YELLOW).move_to(hash_ring.point_from_proportion(pos/1024)) for pos in [220, 230, 240, 250]]
        for key in keys:
            self.play(FadeIn(key))
            self.play(key.animate.move_to(new_nodes[1][0]))
        hotspot = Text("Hotspot", color=RED, font_size=24).next_to(new_nodes[1][0], UP)
        self.play(Write(hotspot))
        virtual_nodes = [
            (Dot(color=RED).move_to(hash_ring.point_from_proportion(300/1024)), "Node A1", 300),
            (Dot(color=RED).move_to(hash_ring.point_from_proportion(600/1024)), "Node A2", 600),
        ]
        virtual_labels = [Text(label, font_size=24).next_to(dot, UP+RIGHT, buff=0.2) for dot, label, pos in virtual_nodes]
        self.play(*[FadeIn(node[0], label) for node, label in zip(virtual_nodes, virtual_labels)])
        self.play(keys[0].animate.move_to(virtual_nodes[0][0]), keys[1].animate.move_to(virtual_nodes[1][0]))
        virt_text = Text("Virtual nodes balance the load.", font_size=24).to_edge(DOWN)
        self.play(Write(virt_text), FadeOut(hotspot))
        self.wait(2)
        self.play(FadeOut(virt_text))

        # Scene 8: Summary and Real-World Examples
        self.play(*[FadeOut(key) for key in keys[2:]], FadeOut(key_dot), FadeOut(key_label))
        benefits = VGroup(
            Text("• Horizontally scalable", font_size=24),
            Text("• Minimal data movement", font_size=24),
            Text("• Supports dynamic load", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        examples = VGroup(
            Text("Discord", font_size=24),
            Text("Amazon DynamoDB", font_size=24),
            Text("Netflix", font_size=24)
        ).arrange(DOWN, aligned_edge=RIGHT).to_edge(RIGHT)
        self.play(Write(benefits), Write(examples))
        self.wait(3)
        self.play(FadeOut(benefits), FadeOut(examples), *[FadeOut(node[0]) for node in nodes + new_nodes + virtual_nodes],
                  *[FadeOut(label) for label in node_labels + new_labels + virtual_labels], FadeOut(hash_ring_label),
                  *[FadeOut(pos) for pos in positions], FadeOut(hash_ring))

if __name__ == "__main__":
    from manim import config
    config.media_dir = "./media"
    config.quality = "low"  # Adjust to "high" for better quality
    scene = ConsistentHashingScene()
    scene.render()