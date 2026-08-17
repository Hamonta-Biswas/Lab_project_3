class RegistrationManager:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.registration_count = 0
            cls._instance.registrations = []

        return cls._instance

    def register_course(self, student_name, course):
        self.registration_count += 1

        registration_id = f"REG-{self.registration_count:03d}"

        registration = {
            "id": registration_id,
            "student": student_name,
            "course": course.code
        }

        self.registrations.append(registration)

        return registration_id

    def get_total_registrations(self):
        return self.registration_count