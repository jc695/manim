from manim import *

class TwoSumScene(Scene):
    def construct(self):
        # Input data
        nums = [2, 7, 11, 15]
        target = 9

        # Step 1: Display the array
        array_title = Text("Array: nums", font_size=30).to_edge(UP)
        boxes = []
        labels = []
        for i, num in enumerate(nums):
            box = Rectangle(width=1, height=1, color=WHITE)
            label = Text(str(num), font_size=24).move_to(box.get_center())
            group = VGroup(box, label).shift(RIGHT * i * 1.2 - RIGHT * 2)
            boxes.append(group)
            labels.append(Text(f"[{i}]", font_size=20).next_to(group, DOWN))
        
        array_group = VGroup(*boxes, *labels)
        self.play(Write(array_title), Create(array_group))
        self.wait(1)

        # Step 2: Display the target
        target_text = Text(f"Target: {target}", font_size=30, color=YELLOW).to_edge(UP).shift(DOWN * 1.5)
        self.play(Write(target_text))
        self.wait(1)

        # Step 3: Simulate hash map construction
        hash_title = Text("Hash Map", font_size=30).shift(UP * 2 + LEFT * 4)
        hash_map = {}
        hash_boxes = {}
        hash_labels = {}

        self.play(Write(hash_title))
        for i, num in enumerate(nums):
            complement = target - num
            if complement in hash_map:
                # Solution found
                break
            hash_map[num] = i

            # Animate adding to hash map
            key_box = Rectangle(width=1.5, height=0.8, color=BLUE)
            value_box = Rectangle(width=1.5, height=0.8, color=BLUE)
            key_label = Text(f"{num}", font_size=20).move_to(key_box.get_center())
            value_label = Text(f"{i}", font_size=20).move_to(value_box.get_center())
            hash_entry = VGroup(key_box, key_label, value_box, value_label).arrange(RIGHT, buff=0.2)
            hash_entry.shift(LEFT * 4 + DOWN * (len(hash_map) - 1))
            hash_boxes[num] = hash_entry

            self.play(
                boxes[i].animate.set_color(YELLOW),
                Create(hash_entry),
                run_time=1
            )
            self.wait(0.5)
            self.play(boxes[i].animate.set_color(WHITE))

        # Step 4: Highlight the solution
        solution_found = False
        for i, num in enumerate(nums):
            complement = target - num
            if complement in hash_map and hash_map[complement] != i:
                solution_found = True
                idx1, idx2 = hash_map[complement], i
                
                # Highlight the two numbers
                self.play(
                    boxes[idx1].animate.set_color(GREEN),
                    boxes[idx2].animate.set_color(GREEN),
                    Flash(boxes[idx1], color=GREEN),
                    Flash(boxes[idx2], color=GREEN),
                    run_time=1
                )
                
                # Show the sum
                sum_text = Text(f"{nums[idx1]} + {nums[idx2]} = {target}", font_size=30, color=GREEN)
                sum_text.shift(DOWN * 3)
                self.play(Write(sum_text))
                
                # Show result
                result = Text(f"Indices: [{idx1}, {idx2}]", font_size=30, color=GREEN).next_to(sum_text, DOWN)
                self.play(Write(result))
                break

        if not solution_found:
            self.play(Write(Text("No solution found", font_size=30, color=RED).shift(DOWN * 3)))

        self.wait(2)

if __name__ == "__main__":
    from manim import config
    config.media_dir = "./media"
    scene = TwoSumScene()
    scene.render()