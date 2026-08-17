from abc import ABC, abstractmethod


class Enrollment(ABC):

    @abstractmethod
    def enroll(self, student_name, course):
        pass


class RegularEnrollment(Enrollment):

    def enroll(self, student_name, course):
        return (
            f"{student_name} enrolled in {course.code} "
            f"through regular enrollment."
        )


class OnlineEnrollment(Enrollment):

    def enroll(self, student_name, course):
        return (
            f"{student_name} enrolled in {course.code} "
            f"through online enrollment."
        )