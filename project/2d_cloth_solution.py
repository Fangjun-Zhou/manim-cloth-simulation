from audioop import alaw2lin
from decimal import DecimalTuple
from matplotlib import widgets
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import xlabel
from manimlib import *


class EulerMethod(Scene):
    def construct(self) -> None:
        # Create an axis.
        axes = Axes(
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
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )

        self.play(ShowCreation(axes))

        # Create a particle coordinate.
        particle_coord = VMobject()

        # Create a praticle
        particle = Dot(color=RED, radius=0.1)
        # Sync the particle coordinate with the particle.
        particle.add_updater(lambda m: m.move_to(
            axes.c2p(particle_coord.get_center()[0], particle_coord.get_center()[1])))

        # Move the particle.
        particle_coord.move_to([1, 1, 0])
        self.play(FadeIn(particle))

        # Move the particle around.
        self.play(particle_coord.animate.move_to([3, 2, 0]))
        self.play(particle_coord.animate.move_to([1, 3, 0]))

        self.wait(1)

        # Create horizontal line and vertical line
        h_line = always_redraw(lambda: axes.get_h_line(particle.get_center()))
        v_line = always_redraw(lambda: axes.get_v_line(particle.get_center()))

        self.play(ShowCreation(h_line), ShowCreation(v_line))

        # Create particle position label.
        particle_position_label = always_redraw(
            lambda: Text(f"({particle_coord.get_center()[0]:.1f}, {particle_coord.get_center()[1]:.1f})").scale(0.5).next_to(particle, UP + RIGHT))

        self.play(Write(particle_position_label))

        self.wait(1)

        # Create a velocity vector.
        velocity = VMobject()
        velocity.move_to([1, -1, 0])
        # Create a velocity vector arrow.
        velocityArrow = Arrow(color=GREEN, buff=0)
        velocityArrow.put_start_and_end_on(
            axes.c2p(particle_coord.get_center()[
                     0], particle_coord.get_center()[1]),
            axes.c2p((particle_coord.get_center() + velocity.get_center())
                     [0], (particle_coord.get_center() + velocity.get_center())[1])
        )

        # Draw the velocity vector.
        self.play(GrowArrow(velocityArrow))

        # Update the velocity vector.
        velocityArrow.add_updater(lambda m: m.put_start_and_end_on(
            axes.c2p(particle_coord.get_center()[
                     0], particle_coord.get_center()[1]),
            axes.c2p((particle_coord.get_center() + velocity.get_center())
                     [0], (particle_coord.get_center() + velocity.get_center())[1])
        ))

        # Add velocity vector label.
        velocity_label = always_redraw(
            lambda: Text(f"({velocity.get_center()[0]:.1f}, {velocity.get_center()[1]:.1f})").set_color(GREEN).scale(0.5).next_to(particle, RIGHT))

        self.play(Write(velocity_label))

        self.wait(1)

        particle_coord.add_updater(
            lambda m, dt: m.shift(velocity.get_center() * dt))

        self.wait(1)

        self.play(velocity.animate.move_to([0, -1, 0]))

        self.wait(2)

        self.play(velocity.animate.move_to([0, 0, 0]))

        particle_coord.clear_updaters()

        self.wait(1)

        self.play(particle_coord.animate.move_to([4, 0, 0]))

        self.wait(1)

        # Mass label.
        mass_label = Text("Particle Mass = 1").scale(
            0.5).next_to(axes, LEFT)

        self.play(Write(mass_label))

        self.wait(1)

        # Add a force vector.
        force = VMobject()
        force.move_to([-1.414/2, 1.414/2, 0])
        # Create a force vector arrow.
        force_arrow = Arrow(color=BLUE, buff=0)
        force_arrow.put_start_and_end_on(
            axes.c2p(particle_coord.get_center()[
                0], particle_coord.get_center()[1]),
            axes.c2p((particle_coord.get_center() + force.get_center())
                     [0], (particle_coord.get_center() + force.get_center())[1])
        )

        # Draw the force vector.
        self.play(GrowArrow(force_arrow))

        # Add force vector label.
        def getForceLabelPosition():
            coord = particle_coord.get_center() + force.get_center() + UP*0.5
            return axes.c2p(coord[0], coord[1])

        force_label = always_redraw(lambda: Text(
            f"F = {math.sqrt(force.get_center()[0]**2 + force.get_center()[1]**2):.1f}").set_color(BLUE).scale(0.5).move_to(getForceLabelPosition()))

        self.play(Write(force_label))

        # Update the force vector.
        force_arrow.add_updater(lambda m: m.put_start_and_end_on(
            axes.c2p(particle_coord.get_center()[
                0], particle_coord.get_center()[1]),
            axes.c2p((particle_coord.get_center() + force.get_center())
                     [0], (particle_coord.get_center() + force.get_center())[1])
        ))

        self.wait(1)

        particle_coord.add_updater(
            lambda m, dt: m.shift(velocity.get_center() * dt))

        velocity.add_updater(
            lambda m, dt: m.shift(force.get_center() * dt))

        self.wait(2)

        self.play(force.animate.move_to([0, -1, 0]))

        self.wait(2)

        self.play(force.animate.move_to([0, 0, 0]), Uncreate(force_label))
        self.play(velocity.animate.move_to([0, 0, 0]))

        self.wait(1)

        self.play(FadeOut(particle), FadeOut(h_line), FadeOut(v_line), Uncreate(particle_position_label), FadeOut(
            velocityArrow), Uncreate(velocity_label), FadeOut(force_arrow), Uncreate(mass_label))


class SpringConstraint(Scene):
    def construct(self) -> None:
        # Create an axis.
        axes = Axes(
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
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )

        # Add the axis to the scene.
        self.add(axes)

        self.wait(1)

        # Move the axis to the right side of the screen.
        self.play(axes.animate.move_to(ORIGIN + RIGHT*3))

        # Add a Latex Hookes Law.
        hookes_law_tex = Tex(r"F_s = -kx").move_to(ORIGIN + UP*3 + LEFT*6)

        self.play(Write(hookes_law_tex))

        self.wait(1)

        # Add two particles.
        particle_a_coord = VMobject()
        particle_a_coord.move_to([-1, 0, 0])
        particle_b_coord = VMobject()
        particle_b_coord.move_to([1, 0, 0])
        particle_a = Dot(color=RED)
        particle_b = Dot(color=RED)
        f_always(particle_a.move_to, lambda: axes.c2p(
            particle_a_coord.get_center()[0],
            particle_a_coord.get_center()[1]
        ))
        f_always(particle_b.move_to, lambda: axes.c2p(
            particle_b_coord.get_center()[0],
            particle_b_coord.get_center()[1]
        ))

        # Add a line between the two particles.
        line = Line(particle_a.get_center(),
                    particle_b.get_center(), color=RED)

        self.play(
            GrowFromCenter(particle_a),
            GrowFromCenter(particle_b),
            ShowCreation(line)
        )

        always(line.put_start_and_end_on,
               particle_a.get_center(), particle_b.get_center())

        # Show the coordinates of the particles.
        _0, ax, _1, ay, _2 = coord_a_group = VGroup(
            Tex("x_A = ("),
            DecimalNumber(0, num_decimal_places=1),
            Tex(", "),
            DecimalNumber(0, num_decimal_places=1),
            Tex(")")
        )
        coord_a_group.arrange(RIGHT).next_to(hookes_law_tex, DOWN, buff=0.5)
        ax.add_updater(lambda m: m.set_value(particle_a_coord.get_center()[0]))
        ay.add_updater(lambda m: m.set_value(particle_a_coord.get_center()[1]))
        self.play(Write(_0), Write(ax), Write(_1), Write(ay), Write(_2))

        _0, bx, _1, by, _2 = coord_b_group = VGroup(
            Tex("x_B = ("),
            DecimalNumber(0, num_decimal_places=1),
            Tex(", "),
            DecimalNumber(0, num_decimal_places=1),
            Tex(")")
        )
        coord_b_group.arrange(RIGHT).next_to(coord_a_group, DOWN, buff=0.5)
        bx.add_updater(lambda m: m.set_value(particle_b_coord.get_center()[0]))
        by.add_updater(lambda m: m.set_value(particle_b_coord.get_center()[1]))
        self.play(Write(_0), Write(bx), Write(_1), Write(by), Write(_2))

        # Add constants of the spring.
        ORIGINAL_LENGTH = 2
        SPRING_K = 3
        original_length = Tex(f"L = {ORIGINAL_LENGTH}, k = {SPRING_K}").next_to(
            coord_b_group, DOWN, buff=0.5)
        self.play(Write(original_length))

        # Add current length of the spring.
        current_length_label, current_length = current_length_group = VGroup(
            Tex(r"d_{A, B} = "),
            DecimalNumber(0, num_decimal_places=1)
        )
        current_length_group.arrange(RIGHT).next_to(
            original_length, DOWN, buff=0.5)
        current_length.add_updater(lambda m: m.set_value(
            np.sqrt(
                (particle_a_coord.get_center()[0] - particle_b_coord.get_center()[0])**2 + (
                    particle_a_coord.get_center()[1] - particle_b_coord.get_center()[1])**2
            )
        ))
        self.play(Write(current_length_label), Write(current_length))

        # Add x value of the spring.
        x_value_label, x_value = x_value_group = VGroup(
            Tex("x = "),
            DecimalNumber(0, num_decimal_places=1)
        )
        x_value_group.arrange(RIGHT).next_to(
            current_length_group, DOWN, buff=0.5)
        x_value.add_updater(lambda m: m.set_value(
            np.sqrt(
                (particle_a_coord.get_center()[0] - particle_b_coord.get_center()[0])**2 + (
                    particle_a_coord.get_center()[1] - particle_b_coord.get_center()[1])**2
            ) - ORIGINAL_LENGTH
        ))
        self.play(Write(x_value_label), Write(x_value))

        # Calculate the force.
        force_label, force = force_group = VGroup(
            Tex(r"F_s = "),
            DecimalNumber(0, num_decimal_places=1)
        )
        force_group.arrange(RIGHT).next_to(
            x_value_group, DOWN, buff=0.5)
        force.add_updater(lambda m: m.set_value(
            -SPRING_K * (np.sqrt(
                (particle_a_coord.get_center()[0] - particle_b_coord.get_center()[0])**2 + (
                    particle_a_coord.get_center()[1] - particle_b_coord.get_center()[1])**2
            ) - ORIGINAL_LENGTH)
        ))
        self.play(Write(force_label), Write(force))

        # Move a and b.
        self.play(
            particle_a_coord.animate.move_to([-1, -1, 0]),
            particle_b_coord.animate.move_to([1, 1, 0]),
        )
        self.play(
            particle_a_coord.animate.move_to([-2, 3, 0]),
            particle_b_coord.animate.move_to([4, 1, 0]),
        )
        self.play(
            particle_a_coord.animate.move_to([0, 0.5, 0]),
            particle_b_coord.animate.move_to([0.5, 1, 0]),
        )
        self.play(
            particle_a_coord.animate.move_to([1, 4, 0]),
            particle_b_coord.animate.move_to([3, -4, 0]),
        )
        self.play(
            particle_a_coord.animate.move_to([-2, -3, 0]),
            particle_b_coord.animate.move_to([-3, 3, 0]),
        )
        self.play(
            particle_a_coord.animate.move_to([-1, 0, 0]),
            particle_b_coord.animate.move_to([1, 0, 0]),
        )

        # Fade out.
        self.play(
            FadeOut(particle_a_coord),
            FadeOut(particle_b_coord),
            FadeOut(hookes_law_tex),
            FadeOut(coord_a_group),
            FadeOut(coord_b_group),
            FadeOut(original_length),
            FadeOut(current_length_group),
            FadeOut(x_value_group),
            FadeOut(force_group),
        )

        self.play(
            FadeOut(particle_a),
            FadeOut(particle_b),
            FadeOut(line),
        )

        self.play(
            Uncreate(axes),
        )
