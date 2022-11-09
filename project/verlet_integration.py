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


class VerletIntegration(Scene):
    def construct(self) -> None:
        # Calculate the position at t + dt.
        pos_t_dt = Tex(r"f(t + \Delta t) = f(t) + \int_{t}^{t + \Delta t}f'(x) dx", isolate=[
            "f", "(", "x", ")", "\int", "dx"])

        self.play(Write(pos_t_dt))

        self.wait(1)

        int_t_t_dt = Tex(r"\int_{t}^{t + \Delta t}f'(x) dx", isolate=[
            "f", "(", "x", ")", "\int", "dx"
        ])

        self.play(TransformMatchingTex(pos_t_dt, int_t_t_dt))

        self.wait(1)

        u_tex = Tex(r"u = f'(x)", isolate=["u", "f", "(", "x", ")"])
        dv_tex = Tex(r"dv = dx", isolate=["v", "dx"])

        u_dv_group = VGroup(u_tex, dv_tex)
        u_dv_group.arrange(RIGHT, buff=0.1)
        u_tex.shift(0.5*LEFT)
        dv_tex.shift(0.5*RIGHT)

        du_tex = Tex(r"du = f''(x) dx", isolate=["u", "f", "(", "x", ")"])
        v_tex = Tex(r"v = x + C", isolate=["v", "x"])

        du_v_group = VGroup(du_tex, v_tex)
        du_v_group.arrange(RIGHT, buff=0.1)
        du_tex.shift(0.5*LEFT)
        v_tex.shift(0.5*RIGHT)
        du_v_group.next_to(u_dv_group, DOWN)

        # Move the integral to the up.
        # Write u and dv.

        self.play(
            int_t_t_dt.animate.shift(UP*1.5)
        )
        self.play(
            Write(u_tex),
            Write(dv_tex)
        )

        # Write du and v.
        self.play(
            TransformMatchingTex(u_tex.copy(), du_tex),
            TransformMatchingTex(dv_tex.copy(), v_tex)
        )

        # int_t_t_dt by parts.
        int_t_t_dt_parts = Tex(
            r"""
            \int_{t}^{t + \Delta t}f'(x) dt = 
            ((x + C)f'(x)) \vert_{t}^{t + \Delta t} - 
            \int_{t}^{t + \Delta t} (x + C)f''(x) dx
            """,
            isolate=[
                "f", "(", "x", ")", "\int", "dx", "C"
            ]
        )
        int_t_t_dt_parts.next_to(int_t_t_dt, ORIGIN)

        self.play(
            TransformMatchingTex(int_t_t_dt, int_t_t_dt_parts)
        )

        self.wait(1)

        # Choose C = -(t + dt).
        c_tex = Tex(r"C = -(t + \Delta t)", isolate=["C", "t", "\Delta t"])
        c_tex.next_to(du_v_group, DOWN)

        self.play(
            Write(c_tex)
        )

        self.wait(1)

        # Replace C.
        v_tex_new = Tex(r"v = x - (t + \Delta t)",
                        isolate=["v", "x", "t", "\Delta t"])
        v_tex_new.next_to(v_tex, ORIGIN)
        int_t_t_dt_parts_new = Tex(
            r"""
            \int_{t}^{t + \Delta t}f'(x) dt = 
            ((x - (t + \Delta t))f'(x)) \vert_{t}^{t + \Delta t} - 
            \int_{t}^{t + \Delta t} (x - (t + \Delta t))f''(x) dx
            """,
            isolate=[
                "f", "(", "x", ")", "\int", "dx", "C"
            ]
        )
        int_t_t_dt_parts_new.next_to(int_t_t_dt_parts, ORIGIN)

        self.play(
            TransformMatchingTex(v_tex, v_tex_new),
            TransformMatchingTex(int_t_t_dt_parts, int_t_t_dt_parts_new)
        )

        self.wait(1)

        # Fade out the u, dv, du, v, and C.
        self.play(
            FadeOut(u_tex),
            FadeOut(dv_tex),
            FadeOut(du_tex),
            FadeOut(v_tex_new),
            FadeOut(c_tex)
        )

        self.wait(1)

        # When x = t + dt.
        prompt, tex = group = VGroup(
            Tex(r"When\ x = t + \Delta t \ ,"),
            Tex(r"(x - (t + \Delta t))f'(x) = 0", isolate=[
                "x", "t", "\Delta t", "f", "(", ")", "0"
            ])
        )
        group.arrange(RIGHT, buff=0.1)
        prompt.shift(LEFT*0.5)

        self.play(
            Write(prompt),
            Write(tex)
        )

        self.wait(1)

        # Expand ((x - (t + \Delta t))f'(x)) \vert_{t}^{t + \Delta t}

        l1, l2, l3 = expanded_tex = VGroup(
            Tex(
                r"""
                ((x - (t + \Delta t))f'(x)) \vert_{t}^{t + \Delta t} 
                = 0 - ((t - (t + \Delta t))f'(t))
                """
            ),
            Tex(
                r"""
                = 0 - (- \Delta t f'(t))
                """,
                isolate=[
                    "t", "\Delta t", "f", "(", ")", "0"
                ]
            ),
            Tex(
                r"""
                = \Delta t f'(t)
                """,
                isolate=[
                    "t", "\Delta t", "f", "(", ")"
                ]
            ),
        )

        expanded_tex.arrange(DOWN, buff=0.1)
        expanded_tex.next_to(group, ORIGIN)
        expanded_tex.shift(DOWN*0.5)

        l2.shift(1.83*RIGHT)
        l3.shift(1.05*RIGHT)

        self.play(FadeOut(prompt))
        self.play(TransformMatchingTex(tex, expanded_tex))

        self.wait(1)

        # int_t_t_dt_parts new
        int_t_t_dt_parts_new2 = Tex(
            r"""
            \int_{t}^{t + \Delta t}f'(x) dt = 
            \Delta t f'(t) - 
            \int_{t}^{t + \Delta t} (x - (t + \Delta t))f''(x) dx
            """,
            isolate=[
                "f", "(", "x", ")", "\int", "dx", "C"
            ]
        )

        int_t_t_dt_parts_new2.next_to(int_t_t_dt_parts, ORIGIN)

        self.play(
            TransformMatchingTex(int_t_t_dt_parts_new, int_t_t_dt_parts_new2)
        )

        self.wait(1)

        # Bring back pos_t_dt.
        self.play(
            FadeOut(expanded_tex)
        )
        self.play(
            Write(pos_t_dt)
        )

        # Expand pos_t_dt.
        expanded_tex = Tex(
            r"""
            f(t + \Delta t) = f(t) +
            \Delta t f'(t) - 
            \int_{t}^{t + \Delta t} (x - (t + \Delta t))f''(x) dx
            """,
            isolate=[
                "f", "(", "x", ")", "\int", "dx", "C"
            ]
        )

        self.play(
            TransformMatchingTex(pos_t_dt, expanded_tex),
            TransformMatchingTex(int_t_t_dt_parts_new2, expanded_tex),
        )

        self.wait(1)

        # Expand the pos_t_dt 2.
        f_t_plus_dt = Tex(
            r"f(t", r"+", r"\Delta t)", r"=", r"f(t)", r"+", r"\Delta t f'(t)", r"+",
            r"\Delta t^2", r"{f''(t)", r"\over", r"2!}", r"+",
            r"\Delta t^3", r"{f^{(3)}(t)", r"\over", r"3!}", r"+",
            r"\cdots"
        )

        self.play(
            TransformMatchingTex(expanded_tex, f_t_plus_dt),
        )

        self.wait(1)

        # Expand f_t_minus_dt.
        f_t_minus_dt = Tex(
            r"f(t", r"-", r"\Delta t)", r"=", r"f(t)", r"-", r"\Delta t f'(t)", r"+",
            r"\Delta t^2", r"{f''(t)", r"\over", r"2!}", r"-",
            r"\Delta t^3", r"{f^{(3)}(t)", r"\over", r"3!}", r"+",
            r"\cdots"
        )

        self.play(
            f_t_plus_dt.animate.shift(UP*0.75),
        )

        f_t_minus_dt.next_to(f_t_plus_dt, DOWN*1.5)

        self.play(
            TransformMatchingTex(f_t_plus_dt.copy(), f_t_minus_dt),
        )

        self.wait(1)

        # Trow away latter terms.
        f_t_plus_dt_approx = Tex(
            r"f(t", r"+", r"\Delta t) \approx f(t)", r"+", r"\Delta t f'(t)", r"+",
            r"\Delta t^2", r"{f''(t)", r"\over", r"2!}", r"+",
            r"\Delta t^3", r"{f^{(3)}(t)", r"\over", r"3!}"
        )
        f_t_plus_dt_approx.next_to(f_t_plus_dt, ORIGIN)
        f_t_minus_dt_approx = Tex(
            r"f(t", r"-", r"\Delta t) \approx f(t)", r"-", r"\Delta t f'(t)", r"+",
            r"\Delta t^2", r"{f''(t)", r"\over", r"2!}", r"-",
            r"\Delta t^3", r"{f^{(3)}(t)", r"\over", r"3!}"
        )
        f_t_minus_dt_approx.next_to(f_t_minus_dt, ORIGIN)

        self.play(
            TransformMatchingTex(f_t_plus_dt, f_t_plus_dt_approx),
            TransformMatchingTex(f_t_minus_dt, f_t_minus_dt_approx),
        )

        self.wait(1)

        # Combine together.

        combine = Tex(
            r"f(t + \Delta t)", r"+", r"f(t - \Delta t) \approx 2f(t)", r"+",
            r"2", r"\Delta t^2", r"{f''(t)", r"\over", r"2!}",
        )

        self.play(
            TransformMatchingTex(f_t_plus_dt_approx, combine),
            TransformMatchingTex(f_t_minus_dt_approx, combine),
        )

        self.wait(1)

        # Final result.
        final_result = Tex(
            r"f(t + \Delta t) \approx 2f(t)", r"-",
            r"f(t - \Delta t)", r"+",
            r"\Delta t^2", r"f''(t)",
        )

        self.play(
            TransformMatchingTex(combine, final_result),
        )
