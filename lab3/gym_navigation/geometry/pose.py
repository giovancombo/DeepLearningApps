""" This module contains the Pose class. """
import math
from typing import Any

from gym_navigation.geometry.point import Point


class Pose:
    """The pose of an object in Cartesian plane. """

    position: Point
    _yaw: float  # Imbardata = rotazione dell'aeroplano attorno al suo asse verticale baricentrico

    def __init__(self, position: Point, yaw: float) -> None:
        self.position = position
        self.yaw = yaw

    def move(self, distance: float) -> None:
        if self.yaw == 0:
            self.position.y_coordinate += distance
        elif abs(self.yaw) == math.pi:
            self.position.y_coordinate -= distance
        else:
            slope = math.tan(math.pi / 2 - self.yaw)
            starting_x = self.position.x_coordinate
            if self.yaw < 0:
                self.position.x_coordinate -= math.sqrt(
                    distance ** 2 / (slope ** 2 + 1))
            else:
                self.position.x_coordinate += math.sqrt(
                    distance ** 2 / (slope ** 2 + 1))
            self.position.y_coordinate -= (
                    slope * (starting_x - self.position.x_coordinate))

    def rotate(self, theta: float) -> None:
        self.yaw += theta

    def shift(self, distance: float, theta: float) -> None:
        self.move(distance)
        self.rotate(theta)

    def calculate_angle_difference(self, target: Point) -> float:
        """ Calculate the angle difference from a point.

        This is the angle and the direction (+ or -) that the object
        needs to rotate in order to face the target point.
        """
        vector1 = Point(target.x_coordinate - self.position.x_coordinate,
                        target.y_coordinate - self.position.y_coordinate)

        pose2 = Pose(
            Point(self.position.x_coordinate, self.position.y_coordinate),
            self.yaw)
        pose2.move(1)
        vector2 = Point(
            pose2.position.x_coordinate - self.position.x_coordinate,
            pose2.position.y_coordinate - self.position.y_coordinate)

        angle_difference = math.atan2(
            vector1.x_coordinate * vector2.y_coordinate
            - vector1.y_coordinate * vector2.x_coordinate,
            vector1.x_coordinate * vector2.x_coordinate
            + vector1.y_coordinate * vector2.y_coordinate)
        return angle_difference

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, Pose)
                and self.position == other.position
                and math.isclose(self.yaw, other.yaw))

    def __repr__(self) -> str:
        return f'Position = {self.position}, Yaw = {self._yaw}'

    @property
    def yaw(self) -> float:
        """The rotation (yaw) of the object.

        It is measured from the y axis and E [-pi, pi].
        Positive yaw means clockwise direction while
        negative yaw means counterclockwise direction.
        """
        return self._yaw

    @yaw.setter
    def yaw(self, yaw: float) -> None:
        self._yaw = yaw
        while self._yaw < -math.pi:
            self._yaw += 2 * math.pi
        while self._yaw > math.pi:
            self._yaw -= 2 * math.pi
