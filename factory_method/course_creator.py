from abc import ABC, abstractmethod

from factory_method.course import (
    Course,
    CSECourse,
    EEECourse
)


class CourseCreator(ABC):

    @abstractmethod
    def create_course(self) -> Course:
        pass


class CSECourseCreator(CourseCreator):

    def create_course(self) -> Course:
        return CSECourse()


class EEECourseCreator(CourseCreator):

    def create_course(self) -> Course:
        return EEECourse()