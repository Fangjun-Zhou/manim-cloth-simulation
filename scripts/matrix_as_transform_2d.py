#!/usr/bin/env python

import numpy as np
import itertools as it
from copy import deepcopy
import sys


from animation import *
from mobject import *
from constants import *
from region import *
from scene import Scene, NumberLineScene
from script_wrapper import command_line_create_scene

MOVIE_PREFIX = "matrix_as_transform_2d/"

def matrix_to_string(matrix):
    return "--".join(["-".join(map(str, row)) for row in matrix])

def matrix_mobject(matrix):
    return text_mobject(
        """
        \\left(
            \\begin{array}{%s}
                %d & %d \\\\
                %d & %d
            \\end{array}
        \\right)
        """%tuple(["c"*matrix.shape[1]] + list(matrix.flatten())),
        size = "\\Huge"
    )

class ShowMultiplication(NumberLineScene):
    args_list = [
        (2, False),
        (0.5, False),
        (-3, False),
        (-3, True),
        (2, True),
        (6, True),
    ]
    @staticmethod
    def args_to_string(num, show_original_line):
        end_string = "WithCopiedOriginalLine" if show_original_line else ""
        return str(num) + end_string

    def construct(self, num, show_original_line):
        config = {"density" : abs(num)*DEFAULT_POINT_DENSITY_1D}
        if abs(num) < 1:
            config["numerical_radius"] = SPACE_WIDTH/num

        NumberLineScene.construct(self, **config)
        if show_original_line:
            self.copy_original_line()
        self.dither()
        self.show_multiplication(num, run_time = 2.0)
        self.dither()

    def copy_original_line(self):
        copied_line = deepcopy(self.number_line)
        copied_num_mobs = deepcopy(self.number_mobs)
        self.play(
            ApplyFunction(
                lambda m : m.shift(DOWN).highlight("green"), 
                copied_line
            ), *[
                ApplyMethod(mob.shift, DOWN)
                for mob in copied_num_mobs
            ]
        )
        self.dither()

class ExamplesOfOneDimensionalLinearTransforms(ShowMultiplication):
    args_list = []
    @staticmethod
    def args_to_string():
        return ""

    def construct(self):
        for num in [2, 0.5, -3]:
            ShowMultiplication.construct(self, num, False)
            self.clear()


class ExamplesOfNonlinearOneDimensionalTransforms(NumberLineScene):
    def construct(self):
        def sinx_plux_x((x, y, z)):
            return (np.sin(x) + 1.2*x, y, z)
        def shift_zero((x, y, z)):
            return (2*x+4, y, z)
        self.nonlinear = text_mobject("Not a Linear Transform")
        self.nonlinear.highlight("red").to_edge(UP)
        pairs = [
            (sinx_plux_x, "numbers don't remain evenly spaced"),
            (shift_zero, "zero does not remain fixed")
        ]
        for func, explanation in pairs:
            self.dither()
            self.run_function(func, explanation)
            self.dither()

    def run_function(self, function, explanation):
        self.clear()
        self.add(self.nonlinear)
        NumberLineScene.construct(self)
        words = text_mobject(explanation).highlight("red")
        words.next_to(self.nonlinear, DOWN, buff = 0.5)
        self.add(words)

        self.play(
            ApplyPointwiseFunction(function, self.number_line),
            *[
                ApplyMethod(
                    mob.shift,
                    function(mob.get_center()) - mob.get_center()
                )
                for mob in self.number_mobs
            ],
            run_time = 2.0
        )


class ShowTwoThenThree(ShowMultiplication):
    args_list = []
    @staticmethod
    def args_to_string():
        return ""

    def construct(self):
        NumberLineScene.construct(self, density = 10*DEFAULT_POINT_DENSITY_1D)
        self.copy_original_line()
        self.show_multiplication(2)
        self.dither()
        self.show_multiplication(3)
        self.dither()



########################################################

class TransformScene2D(Scene):
    def add_number_plane(self, density_factor = 1, use_faded_lines = True):
        config = {
            "x_radius" : 2*SPACE_WIDTH,
            "y_radius" : 2*SPACE_HEIGHT,
            "density" : DEFAULT_POINT_DENSITY_1D*density_factor
        }
        if not use_faded_lines:
            config["x_faded_line_frequency"] = None
            config["y_faded_line_frequency"] = None
        self.number_plane = NumberPlane(**config)
        self.add(self.number_plane)

    def add_background(self):
        self.paint_into_background(
            NumberPlane(color = "grey").add_coordinates()
        )

    def add_x_y_arrows(self):
        self.x_arrow = Arrow(
            ORIGIN, 
            self.number_plane.num_pair_to_point((1, 0)),
            color = "green"
        )
        self.y_arrow = Arrow(
            ORIGIN,
            self.number_plane.num_pair_to_point((0, 1)),
            color = "red"
        )
        self.add(self.x_arrow, self.y_arrow)
        self.number_plane.filter_out(
            lambda (x, y, z) : (0 < x) and (x < 1) and (abs(y) < 0.1)
        )
        self.number_plane.filter_out(
            lambda (x, y, z) : (0 < y) and (y < 1) and (abs(x) < 0.1)
        )
        return self


class ShowMatrixTransform(TransformScene2D):
    args_list = [
        ([[1, 0.5], [0.5, 1]], True, False),
        ([[2, 0], [0, 2]], True, False),
        ([[0.5, 0], [0, 0.5]], True, False),
        ([[-1, 0], [0, -1]], True, False),
        ([[0, 1], [1, 0]], True, False),
        ([[-2, 0], [-1, -1]], True, False),
    ]
    @staticmethod
    def args_to_string(matrix, with_background, show_matrix):
        background_string = "WithBackground" if with_background else "WithoutBackground"
        show_string = "ShowingMatrix" if show_matrix else ""
        return matrix_to_string(matrix) + background_string + show_string

    def construct(self, matrix, with_background, show_matrix):
        matrix = np.array(matrix)
        number_plane_config = {
            "density_factor" : self.get_density_factor(matrix)
        }
        if with_background:
            self.add_background()
            number_plane_config["use_faded_lines"] = False
            self.add_number_plane(**number_plane_config)
            self.add_x_y_arrows()
        else:
            self.add_number_plane(**number_plane_config)
        self.save_image()
        if show_matrix:
            self.add(matrix_mobject(matrix).to_corner(UP+LEFT))
        def func(mobject):
            mobject.points[:, :2] = np.dot(mobject.points[:, :2], np.transpose(matrix))
            return mobject

        self.dither()
        kwargs = {
            "run_time" : 2.0,
            "interpolation_function" : self.get_interpolation_function(matrix)
        }
        anims = [ApplyFunction(func, self.number_plane, **kwargs)]
        if hasattr(self, "x_arrow") and hasattr(self, "y_arrow"):
            for arrow, index in (self.x_arrow, 0), (self.y_arrow, 1):
                new_arrow = Arrow(
                    ORIGIN,
                    self.number_plane.num_pair_to_point(matrix[:,index]),
                    color = arrow.get_color()
                )
                arrow.remove_tip()
                new_arrow.remove_tip()
                Mobject.align_data(arrow, new_arrow)
                arrow.add_tip()
                new_arrow.add_tip()
                anims.append(Transform(arrow, new_arrow, **kwargs))
        self.play(*anims)
        self.dither()
        self.set_name(str(self) + self.args_to_string(matrix, with_background, show_matrix))
        self.save_image(os.path.join(MOVIE_DIR, MOVIE_PREFIX, "images"))

    def get_density_factor(self, matrix):
        max_norm = max([
            abs(np.linalg.norm(column))
            for column in np.transpose(matrix)
        ])
        return max(max_norm, 1)

    def get_interpolation_function(self, matrix):
        def toggled_sign(n, i):
            return int(i%2 == 0)^int(n >= 0)
        rotational_components = [
            sign*np.arccos(matrix[i,i]/np.linalg.norm(matrix[:,i]))
            for i in [0, 1]
            for sign in [toggled_sign(matrix[1-i, i], i)]
        ]
        average_rotation = sum(rotational_components)/2
        if abs(average_rotation) < np.pi / 2:
            return straight_path
        elif average_rotation > 0:
            return counterclockwise_path
        else:
            return clockwise_path


class ExamplesOfTwoDimensionalLinearTransformations(ShowMatrixTransform):
    args_list = []
    @staticmethod
    def args_to_string():
        return ""

    def construct(self):
        matrices = [
            [[1, 0.5], 
             [0.5, 1]],
            [[0, -1],
             [2, 0]],
            [[1, 3],
             [-2, 0]],
        ]
        for matrix in matrices:
            self.clear()
            ShowMatrixTransform.construct(self, matrix, False, False)


class ExamplesOfNonlinearTwoDimensionalTransformations(Scene):
    def construct(self):
        Scene.construct(self)
        def squiggle((x, y, z)):
            return (x+np.sin(y), y+np.cos(x), z)
        def shift_zero((x, y, z)):
            return (2*x + 3*y + 4, -1*x+y+2, z)
        self.nonlinear = text_mobject("Nonlinear Transform")
        self.nonlinear.highlight("red").to_edge(UP)
        pairs = [
            (squiggle, "lines to not remain straight"),
            (shift_zero, "the origin does not remain fixed")
        ]
        for function, explanation in pairs:
            self.apply_function(function, explanation)


    def apply_function(self, function, explanation):
        self.clear()
        number_plane = NumberPlane(
            x_radius = 1.5*SPACE_WIDTH,
            y_radius = 1.5*SPACE_HEIGHT,
            density = 3*DEFAULT_POINT_DENSITY_1D,
        )
        numbers = number_plane.get_coordinate_labels()
        words = text_mobject(explanation).highlight("red")
        words.next_to(self.nonlinear, DOWN, buff = 0.5)

        self.add(number_plane, self.nonlinear, words, *numbers)
        self.dither()
        self.play(
            ApplyPointwiseFunction(function, number_plane),
            *[
                ApplyMethod(
                    mob.shift,
                    function(mob.get_center())-mob.get_center()
                )
                for mob in numbers
            ],
            run_time = 2.0
        )
        self.dither(2)


class TrickyExamplesOfNonlinearTwoDimensionalTransformations(Scene):
    def construct(self):
        number_plane = NumberPlane()
        phrase1, phrase2 = text_mobject([
            "These might look like they keep lines straight...",
            "but diagonal lines get curved"
        ]).to_edge(UP).split()
        phrase2.highlight("red")
        diagonal = Line(
            DOWN*SPACE_HEIGHT+LEFT*SPACE_WIDTH,
            UP*SPACE_HEIGHT+RIGHT*SPACE_WIDTH
        )
        def sunrise((x, y, z)):
            return ((SPACE_HEIGHT+y)*x, y, z)

        def squished((x, y, z)):
            return (x + np.sin(x), y+np.sin(y), z)

        self.add(phrase1)
        self.run_function(sunrise, number_plane)
        self.run_function(squished, number_plane)
        self.add(phrase2)
        self.play(ShowCreation(diagonal))
        self.remove(diagonal)
        number_plane.add(diagonal)
        self.run_function(sunrise, number_plane)
        self.run_function(squished, number_plane)


    def run_function(self, function, plane):
        number_plane = deepcopy(plane)
        self.add(number_plane)
        self.dither()
        self.play(ApplyPointwiseFunction(function, number_plane, run_time = 2.0))
        self.dither(3)
        self.remove(number_plane)


############# HORRIBLE! ##########################
class ShowMatrixTransformHack(TransformScene2D):
    args_list = [
        ([[1, 3], [-2, 0]], True, False),
    ]
    @staticmethod
    def args_to_string(matrix, with_background, show_matrix):
        background_string = "WithBackground" if with_background else "WithoutBackground"
        show_string = "ShowingMatrix" if show_matrix else ""
        return matrix_to_string(matrix) + background_string + show_string

    def construct(self, matrix, with_background, show_matrix):
        matrix = np.array(matrix)
        number_plane_config = {
            "density_factor" : self.get_density_factor(matrix)
        }
        if with_background:
            self.add_background()
            number_plane_config["use_faded_lines"] = False
            self.add_number_plane(**number_plane_config)
            self.add_x_y_arrows()
        else:
            self.add_number_plane(**number_plane_config)
        if show_matrix:
            self.add(matrix_mobject(matrix).to_corner(UP+LEFT))
        def func(mobject):
            mobject.points[:, :2] = np.dot(mobject.points[:, :2], np.transpose(matrix))
            return mobject
        dot = Dot((-1, 2, 0), color = "yellow")
        x_arrow_copy = deepcopy(self.x_arrow)
        y_arrow_copy = Arrow(LEFT, LEFT+2*UP, color = "red")

        self.number_plane.add(dot)
        self.play(ApplyMethod(x_arrow_copy.rotate, np.pi))
        self.play(ShowCreation(y_arrow_copy))
        self.dither()
        self.remove(x_arrow_copy, y_arrow_copy)
        kwargs = {
            "run_time" : 2.0,
            "interpolation_function" : self.get_interpolation_function(matrix)
        }
        anims = [ApplyFunction(func, self.number_plane, **kwargs)]
        if hasattr(self, "x_arrow") and hasattr(self, "y_arrow"):
            for arrow, index in (self.x_arrow, 0), (self.y_arrow, 1):
                new_arrow = Arrow(
                    ORIGIN,
                    self.number_plane.num_pair_to_point(matrix[:,index]),
                    color = arrow.get_color()
                )
                arrow.remove_tip()
                new_arrow.remove_tip()
                Mobject.align_data(arrow, new_arrow)
                arrow.add_tip()
                new_arrow.add_tip()
                anims.append(Transform(arrow, new_arrow, **kwargs))
        self.play(*anims)
        self.dither()

        x_arrow_copy = deepcopy(self.x_arrow)
        y_arrow_copy = Arrow(LEFT+2*UP, 5*RIGHT+2*UP, color = "red")
        self.play(ApplyMethod(x_arrow_copy.rotate, np.pi))
        self.play(ShowCreation(y_arrow_copy))
        self.remove(x_arrow_copy, y_arrow_copy)
        self.dither(3)

    def get_density_factor(self, matrix):
        max_norm = max([
            abs(np.linalg.norm(column))
            for column in np.transpose(matrix)
        ])
        return max(max_norm, 1)

    def get_interpolation_function(self, matrix):
        rotational_components = [
            sign*np.arccos(matrix[i,i]/np.linalg.norm(matrix[:,i]))
            for i in [0, 1]
            for sign in [((-1)**i)*np.sign(matrix[1-i, i])]
        ]
        average_rotation = sum(rotational_components)/2
        if abs(average_rotation) < np.pi / 2:
            return straight_path
        elif average_rotation > 0:
            return counterclockwise_path
        else:
            return clockwise_path


class Show90DegreeRotation(TransformScene2D):
    def construct(self):
        self.add_number_plane()
        self.add_background()
        self.add_x_y_arrows()

        self.dither()
        self.play(*[
            RotationAsTransform(mob, run_time = 2.0)
            for mob in self.number_plane, self.x_arrow, self.y_arrow
        ])
        self.dither()





if __name__ == "__main__":
    command_line_create_scene(MOVIE_PREFIX)