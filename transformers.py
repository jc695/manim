from manim import *

class TransformerArchitecture(Scene):
    def construct(self):
        # Title
        title = Text("How Transformers Work", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Step 1: Input Tokens
        tokens = ["I", "love", "Manim"]
        token_boxes = VGroup(*[
            Rectangle(width=1.5, height=0.8, color=BLUE).add(Text(tok, font_size=24))
            for tok in tokens
        ]).arrange(RIGHT, buff=0.6).shift(UP * 2)
        self.play(Create(token_boxes))
        self.wait(0.5)

        # Step 2: Positional Encoding
        pos_enc = VGroup(*[
            Rectangle(width=1.5, height=0.5, color=GREEN).add(Text(f"Pos {i}", font_size=20))
            for i in range(len(tokens))
        ]).arrange(RIGHT, buff=0.6).next_to(token_boxes, DOWN, buff=0.2)
        self.play(Create(pos_enc))
        self.wait(0.5)

        # Step 3: Add token + position
        added = Text("Token + Position Embedding", font_size=24).next_to(pos_enc, DOWN, buff=0.5)
        self.play(Write(added))
        self.wait(0.5)

        # Step 4: Self-Attention
        sa_box = Rectangle(width=5, height=1.5, color=YELLOW).shift(DOWN * 0.5)
        sa_text = Text("Self-Attention", font_size=28).move_to(sa_box.get_center())
        self.play(FadeIn(sa_box), Write(sa_text))
        self.wait(0.5)

        arrows_to_sa = VGroup(*[
            Arrow(start.get_bottom(), sa_box.get_top(), buff=0.1, stroke_width=2)
            for start in pos_enc
        ])
        self.play(*[Create(arrow) for arrow in arrows_to_sa])
        self.wait(0.5)

        # Step 5: Feed Forward
        ff_box = Rectangle(width=5, height=1.2, color=ORANGE).next_to(sa_box, DOWN, buff=0.8)
        ff_text = Text("Feed Forward", font_size=28).move_to(ff_box.get_center())
        self.play(FadeIn(ff_box), Write(ff_text))
        self.play(Create(Arrow(sa_box.get_bottom(), ff_box.get_top(), buff=0.1)))
        self.wait(0.5)

        # Step 6: Output
        output_boxes = VGroup(*[
            Rectangle(width=1.5, height=0.8, color=RED).add(Text("Out", font_size=24))
            for _ in tokens
        ]).arrange(RIGHT, buff=0.6).next_to(ff_box, DOWN, buff=1)
        self.play(Create(output_boxes))

        self.wait(2)
        self.play(FadeOut(*self.mobjects))

if __name__ == "__main__":
    # run code directly instead of CLI.
    # Demo to illustrate how transformers work.
    from manim import *
    config.media_dir = './media'
    config.quality = 'low'
    scene = TransformerArchitecture()
    scene.render()