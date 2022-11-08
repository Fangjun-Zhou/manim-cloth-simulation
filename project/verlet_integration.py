from turtle import pos
from sympy import false, isolate
from manimlib import *
import manimlib


class EulerIntegrator(Scene):
    def construct(self) -> None:
        # Create a position function.
        f, f_desc = f_group = VGroup(
            Tex("f(x)", isolate=["f", "(", "x", ")"]),
            Text("Position of the object at time x.")
        )
        f_group.arrange(DOWN, buff=0.5)
        self.play(Write(f))
        self.play(Write(f_desc))

        self.wait(1)

        self.play(Uncreate(f_desc))

        # Create a velocity expression.
        f_prime, f_prime_desc = f_prime_group = VGroup(
            Tex("f'(x)", isolate=["f", "(", "x", ")"]),
            Text("Velocity of the object at time x.")
        )
        f_prime_group.arrange(DOWN, buff=0.5)

        self.play(TransformMatchingTex(f, f_prime))
        self.play(Write(f_prime_desc))

        self.wait(1)

        self.play(Uncreate(f_prime_desc))

        # Velocity integration.
        velocity_integration = Tex(
            "f(x) = \int f'(x) dx", isolate=["f", "(", "x", ")", "\int", "dx"])
        self.play(TransformMatchingTex(f_prime, velocity_integration))

        self.wait(1)

        # position at time t.
        pos_t = Tex(r"f(t) = \int_{0}^{t} f'(x) dx", isolate=[
                    "f", "(", "x", ")", "\int", "dx"])
        pos_t.move_to(velocity_integration)
        self.play(
            velocity_integration.animate.shift(UP*1.5),
            TransformMatchingTex(velocity_integration.copy(), pos_t)
        )

        self.wait(1)

        # When position at time t is known, we can calculate the position at t + dt.
        text = Text(
            "When position at time t is known, we can calculate the position at t + dt.")
        text.scale(0.5).next_to(pos_t, DOWN, buff=1)
        self.play(Write(text))

        self.wait(1)

        self.play(Uncreate(text))

        # Calculate the position at t + dt.
        pos_t_dt = Tex(r"f(t + \Delta t) = f(t) + \int_{t}^{t + \Delta t}f'(x) dx", isolate=[
            "f", "(", "x", ")", "\int", "dx"])
        pos_t_dt.next_to(pos_t, DOWN)

        self.play(TransformMatchingTex(pos_t.copy(), pos_t_dt))

        self.wait(1)

        # Fade out velocity_integration and pos_t.
        self.play(
            FadeOut(velocity_integration),
            FadeOut(pos_t)
        )

        self.play(pos_t_dt.animate.move_to(ORIGIN))

        self.wait(1)


class EulerIntegrationError(Scene):
    def construct(self) -> None:
        # Calculate the position at t + dt.
        pos_t_dt = Tex(r"f(t + \Delta t) = f(t) + \int_{t}^{t + \Delta t}f'(x) dx", isolate=[
            "f", "(", "x", ")", "\int", "dx"])
        pos_t_dt.move_to(ORIGIN)

        self.add(pos_t_dt)

        # Move the equation to the left side of the screen.
        self.play(pos_t_dt.animate.shift(LEFT*4 + UP*2))

        # Create a axis.
        ax = Axes(
            x_range=(0, 5),
            y_range=(0, 10),
            width=6,
            height=6,
            axis_config={
                "include_tip": True
            }
        )
        ax.add_coordinate_labels(font_size=16)
        ax.move_to(RIGHT*4)
        self.play(ShowCreation(ax))

        self.wait(1)

        # Create a function f(x) = x^2.
        f_x = ax.get_graph(lambda x: x**2, color=BLUE)
        f_x_tex = Tex("f(x) = x^2")
        f_x_tex.next_to(pos_t_dt, DOWN)

        self.play(
            Write(f_x_tex),
            ShowCreation(f_x)
        )

        self.wait(1)

        # Take the derivative of f(x) = x^2.
        f_p_x = ax.get_graph(lambda x: 2*x, color=RED)
        f_p_x_tex = Tex("f'(x) = 2x")
        f_p_x_tex.next_to(f_x_tex, DOWN)

        self.play(
            Write(f_p_x_tex),
            ShowCreation(f_p_x)
        )

        self.wait(1)

        # Current position at t.
        t = ValueTracker(1)

        t_tex, t_val = t_group = VGroup(
            Tex("t = "),
            DecimalNumber(t.get_value(), num_decimal_places=2)
        )
        t_group.arrange(RIGHT, buff=0.1)
        t_group.next_to(f_p_x_tex, DOWN)
        t_val.add_updater(lambda m: m.set_value(t.get_value()))

        self.play(
            Write(t_tex),
            Write(t_val)
        )

        self.wait(1)

        # Draw a dot at the current position.
        t_dot = Dot(ax.coords_to_point(
            t.get_value(), t.get_value()**2), color=BLUE)
        t_p_dot = Dot(ax.coords_to_point(
            t.get_value(), 2*t.get_value()), color=RED)

        t_dot.add_updater(lambda m: m.move_to(ax.coords_to_point(
            t.get_value(), t.get_value()**2)))
        t_p_dot.add_updater(lambda m: m.move_to(ax.coords_to_point(
            t.get_value(), 2*t.get_value())))

        self.play(
            GrowFromCenter(t_dot),
            GrowFromCenter(t_p_dot)
        )

        # Draw h and v lines for t_p_dot.
        t_p_dot_h_line = always_redraw(
            lambda: ax.get_h_line(t_p_dot.get_center(), color=RED))
        t_p_dot_v_line = always_redraw(
            lambda: ax.get_v_line(t_p_dot.get_center(), color=RED))

        self.play(
            ShowCreation(t_p_dot_h_line),
            ShowCreation(t_p_dot_v_line)
        )

        self.wait(1)

        def drawTangentLineAtT(t: float) -> Line:
            return ax.get_graph(lambda x: 2*t*x - t**2, color=GREEN)

        t_tangent_line = always_redraw(
            lambda: drawTangentLineAtT(t.get_value()))

        self.play(ShowCreation(t_tangent_line))

        self.play(t.animate.set_value(2))
        self.play(t.animate.set_value(1))

        self.wait(1)

        # Uncreate t_tangent_line.
        self.play(Uncreate(t_tangent_line))

        self.wait(1)

        # Indicate integral.
        self.play(Indicate(pos_t_dt))

        self.wait(1)

        # Remove h and v lines for t_p_dot.
        self.play(
            Uncreate(t_p_dot_h_line),
            Uncreate(t_p_dot_v_line)
        )

        # Delta t.
        delta_t = ValueTracker(1)
        delta_t_tex, delta_t_val = delta_t_group = VGroup(
            Tex(r"\Delta t = "),
            DecimalNumber(delta_t.get_value(), num_decimal_places=2)
        )
        delta_t_group.arrange(RIGHT, buff=0.1)
        delta_t_group.next_to(t_group, DOWN)
        delta_t_val.add_updater(lambda m: m.set_value(delta_t.get_value()))

        self.play(
            Write(delta_t_tex),
            Write(delta_t_val)
        )
        # Get generate vector from t_dot to t_dt_dot.
        print(ax.coords_to_point(t.get_value(), t.get_value()**2))
        move_vector = always_redraw(lambda: Arrow(
            t_dot.get_center(),
            ax.coords_to_point(
                t.get_value() + delta_t.get_value(), t.get_value()**2 +
                2*t.get_value()*delta_t.get_value()
            ),
            color=GREEN,
            buff=0
        ))

        self.play(GrowArrow(move_vector))

        self.wait(1)

        self.play(delta_t.animate.set_value(0.1))

        self.wait(1)

        self.play(delta_t.animate.set_value(1))

        self.wait(1)

        # Trace t_dot.
        trace = TracedPath(t_dot.get_center, stroke_width=2, stroke_color=BLUE)
        self.add(trace)

        # Move the t_dot and t_p_dot.
        t_dot.clear_updaters()

        self.play(
            t_dot.animate.move_to(ax.coords_to_point(
                t.get_value() + delta_t.get_value(), t.get_value()**2 +
                2*t.get_value()*delta_t.get_value()
            )),
            t.animate.set_value(t.get_value() + delta_t.get_value())
        )

        self.wait(1)
