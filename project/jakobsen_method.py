from manimlib import *


class JakobsenMethod(Scene):
    def construct(self) -> None:
        # Create an axis.
        ax = Axes(
            x_range=(-6, 6),
            y_range=(-4, 4),
            height=7,
            width=7*(6/4),
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 1,
                "include_tip": True,
            }
        )
        ax.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )

        ax.shift(3*RIGHT)

        self.play(ShowCreation(ax))

        self.wait(1)

        # Constraint desc.

        constraints_desc = Text(
            """
            The length of all constrains = 1.
            """
        )
        constraints_desc.scale(0.5)
        constraints_desc.shift(6*LEFT + 2*UP)

        self.play(Write(constraints_desc))

        self.wait(1)

        # Create 5 points.
        # Create 4 constraints.
        points_coords = [
            VMobject()
            for i in range(5)
        ]
        points = [
            Dot().set_color(RED)
            for i in range(5)
        ]

        for i in range(5):
            points[i].add_updater(
                lambda m, i=i: m.move_to(ax.c2p(
                    points_coords[i].get_center()[0],
                    points_coords[i].get_center()[1],
                ))
            )

        # Move the points.
        for i in range(5):
            points_coords[i].move_to([2-i, 0, 0])

        constraints = [
            always_redraw(
                lambda i=i: Line(
                    ax.c2p(
                        points_coords[i].get_center()[0],
                        points_coords[i].get_center()[1],
                    ),
                    ax.c2p(
                        points_coords[i+1].get_center()[0],
                        points_coords[i+1].get_center()[1],
                    ),
                    color=RED,
                )
            )
            for i in range(4)
        ]

        # Draw the points.
        self.play(
            *[GrowFromCenter(points[i]) for i in range(5)]
        )

        for i in range(4):
            self.play(ShowCreation(constraints[i]), run_time=0.1)
