from manim import *
import hashlib
import bisect

# Simplified ConsistentHashing class for visualization
class ConsistentHashingVisualizer:
    def __init__(self, num_replicas=3):
        self.num_replicas = num_replicas
        self.ring = {}
        self.sorted_keys = []
        self.nodes = set()

    def _hash(self, key):
        # Simplified hash for visualization (maps to 0-360 degrees)
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % 360

    def add_node(self, node):
        self.nodes.add(node)
        for i in range(self.num_replicas):
            key = f"{node}:{i}"
            hash_val = self._hash(key)
            self.ring[hash_val] = node
            bisect.insort(self.sorted_keys, hash_val)

    def get_node(self, key):
        if not self.ring:
            return None
        hash_val = self._hash(key)
        index = bisect.bisect(self.sorted_keys, hash_val) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[index]]

class ConsistentHashingScene(Scene):
    def construct(self):
        # Step 1: Draw the hash ring
        ring = Circle(radius=3, color=BLUE)
        ring_label = Text("Hash Ring").next_to(ring, UP, buff=0.5)
        self.play(Create(ring), Write(ring_label))
        self.wait(1)

        # Step 2: Initialize consistent hashing
        ch = ConsistentHashingVisualizer(num_replicas=3)
        nodes = ["NodeA", "NodeB", "NodeC"]
        node_dots = {}
        labels = {}

        # Step 3: Add nodes and their replicas
        for node in nodes:
            ch.add_node(node)
            for i in range(3):  # 3 replicas
                key = f"{node}:{i}"
                angle = ch._hash(key) * DEGREES  # Convert to radians
                pos = ring.point_at_angle(angle)
                dot = Dot(pos, color=YELLOW if i == 0 else GREEN)
                label = Text(f"{node}:{i}", font_size=20).next_to(pos, direction=pos/np.linalg.norm(pos), buff=0.1)
                node_dots[key] = dot
                labels[key] = label
                self.play(FadeIn(dot), Write(label), run_time=0.5)

        self.wait(1)

        # Step 4: Map some keys
        keys = ["apple", "banana", "cherry"]
        key_dots = {}
        for key in keys:
            key_hash = ch._hash(key)
            angle = key_hash * DEGREES
            key_pos = ring.point_at_angle(angle)
            key_dot = Dot(key_pos, color=RED)
            key_label = Text(key, font_size=20, color=RED).next_to(key_dot, RIGHT, buff=0.1)
            self.play(FadeIn(key_dot), Write(key_label), run_time=0.5)

            # Find the target node
            target_node = ch.get_node(key)
            for i in range(3):
                node_key = f"{target_node}:{i}"
                if node_key in node_dots:
                    target_pos = node_dots[node_key].get_center()
                    arrow = Arrow(key_pos, target_pos, color=WHITE)
                    self.play(Create(arrow), run_time=0.5)
                    self.play(FadeOut(arrow), run_time=0.5)
                    break
            key_dots[key] = (key_dot, key_label)

        self.wait(1)

        # Step 5: Remove NodeB and update
        node_to_remove = "NodeB"
        self.play(Write(Text(f"Removing {node_to_remove}", font_size=30).to_edge(DOWN)))
        for i in range(3):
            key = f"{node_to_remove}:{i}"
            if key in node_dots:
                self.play(FadeOut(node_dots[key]), FadeOut(labels[key]), run_time=0.5)
                del node_dots[key]
                del labels[key]
        ch.nodes.remove(node_to_remove)
        ch.ring = {k: v for k, v in ch.ring.items() if v != node_to_remove}
        ch.sorted_keys = sorted(ch.ring.keys())

        # Step 6: Reassign keys
        for key in keys:
            target_node = ch.get_node(key)
            key_dot, key_label = key_dots[key]
            for i in range(3):
                node_key = f"{target_node}:{i}"
                if node_key in node_dots:
                    target_pos = node_dots[node_key].get_center()
                    arrow = Arrow(key_dot.get_center(), target_pos, color=WHITE)
                    self.play(Create(arrow), run_time=0.5)
                    self.play(FadeOut(arrow), run_time=0.5)
                    break

        self.wait(2)

if __name__ == "__main__":
    from manim import config
    config.media_dir = "./media"
    scene = ConsistentHashingScene()
    scene.render()