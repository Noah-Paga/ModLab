from manim import *
import numpy as np

class Rank2D(Scene):
    def construct(self):
        title = Text("Geometric Meaning of Matrix Rank (2D)").scale(0.8).to_edge(UP)
        self.play(FadeIn(title))

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_width": 1, "stroke_opacity": 0.6},
        )
        self.play(Create(plane))

        # Basis and unit square
        e1 = Vector(RIGHT, color=YELLOW)
        e2 = Vector(UP, color=BLUE)
        e1_label = Text("e1").scale(0.5).next_to(e1, DOWN).set_color(YELLOW)
        e2_label = Text("e2").scale(0.5).next_to(e2, LEFT).set_color(BLUE)

        unit_square = Polygon(ORIGIN, RIGHT, RIGHT + UP, UP, color=WHITE, stroke_width=2)
        area_label = Text("Area = 1").scale(0.5).next_to(unit_square, UR)

        self.play(Create(e1), Create(e2))
        self.play(Write(e1_label), Write(e2_label))
        self.play(Create(unit_square), FadeIn(area_label))

        def show_transformation(A, title_text, color=GREEN):
            subtitle = Text(title_text).scale(0.5).to_edge(DOWN)
            box = SurroundingRectangle(subtitle, buff=0.15, color=color, stroke_width=2)

            Ae1 = A @ np.array([1, 0])
            Ae2 = A @ np.array([0, 1]) 

            v1 = Vector(Ae1, color=YELLOW)
            v2 = Vector(Ae2, color=BLUE)

            self.play(FadeIn(subtitle), Create(box), run_time=0.6)
            self.play(
                ApplyMatrix(A, plane),
                ApplyMatrix(A, e1),
                ApplyMatrix(A, e2),
                ApplyMatrix(A, unit_square),
                Transform(e1_label, Text("A e1").scale(0.5).set_color(YELLOW).next_to(v1.get_end(), DOWN)),
                Transform(e2_label, Text("A e2").scale(0.5).set_color(BLUE).next_to(v2.get_end(), LEFT)),
                run_time=1.4,
            )

            p0 = np.array([0, 0, 0])
            p1 = np.array([Ae1[0], Ae1[1], 0])
            p2 = np.array([Ae1[0] + Ae2[0], Ae1[1] + Ae2[1], 0])
            p3 = np.array([Ae2[0], Ae2[1], 0])
            para = Polygon(p0, p1, p2, p3, color=color, stroke_width=3)
            self.play(Create(v1), Create(v2), Create(para), run_time=0.8)

            det = np.linalg.det(A)
            if abs(det) > 1e-8:
                txt = Text(f"Area = |det A| = {abs(det):.2f}").scale(0.5)
            else:
                txt = Text("Area = 0 (collapse)").scale(0.5)

            txt.next_to(para, UR)
            self.play(FadeIn(txt))
            self.wait(1.0)
            self.play(FadeOut(VGroup(v1, v2, para, txt, subtitle, box)), run_time=0.6)

        A_full = np.array([[1, 1.2],[0.2, 1.0]])
        show_transformation(A_full, "rank(A) = 2 → 2D region (nonzero area)", color=GREEN)

        A_rank1 = np.array([[1, 2],[2, 4]])  # rank 1
        show_transformation(A_rank1, "rank(A) = 1 → line (area = 0)", color=ORANGE)

        A_rank0 = np.zeros((2, 2))           # rank 0
        show_transformation(A_rank0, "rank(A) = 0 → point (origin)", color=RED)

        wrap = Text("Takeaway: Rank = dimension of the image").scale(0.6).to_edge(DOWN)
        self.play(Write(wrap))
        self.wait(1.2)
