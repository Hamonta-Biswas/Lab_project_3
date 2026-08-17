from abc import ABC, abstractmethod


class Course(ABC):

    def __init__(self, code, name, department):
        self.code = code
        self.name = name
        self.department = department

    @abstractmethod
    def get_details(self):
        pass


class CSECourse(Course):

    def __init__(self):
        super().__init__(
            "CSE3206",
            "Software Engineering",
            "Computer Science and Engineering"
        )

    def get_details(self):
        return f"{self.code} - {self.name} ({self.department})"


class EEECourse(Course):

    def __init__(self):
        super().__init__(
            "EEE3202",
            "Digital Electronics",
            "Electrical and Electronic Engineering"
        )

    def get_details(self):
        return f"{self.code} - {self.name} ({self.department})"