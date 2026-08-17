from singleton.registration_manager import RegistrationManager

from factory_method.course_creator import (
    CSECourseCreator,
    EEECourseCreator
)

from abstract_factory.registration_factory import (
    RegularRegistrationFactory,
    OnlineRegistrationFactory
)


def process_registration(
    student_name,
    course_type,
    registration_type,
    base_fee
):

    print("\n" + "=" * 55)
    print("        UNIVERSITY COURSE REGISTRATION")
    print("=" * 55)

    print(f"Student: {student_name}")
    print(f"Course Type: {course_type}")
    print(f"Registration Type: {registration_type}")

    # -----------------------------------------
    # Singleton
    # -----------------------------------------

    manager = RegistrationManager()

    print("\n[Singleton]")
    print("Using centralized RegistrationManager")

    # -----------------------------------------
    # Factory Method
    # -----------------------------------------

    course_creators = {
        "CSE": CSECourseCreator(),
        "EEE": EEECourseCreator()
    }

    creator = course_creators[course_type]
    course = creator.create_course()

    print("\n[Factory Method]")
    print(f"Created Course: {course.get_details()}")

    # -----------------------------------------
    # Abstract Factory
    # -----------------------------------------

    registration_factories = {
        "Regular": RegularRegistrationFactory(),
        "Online": OnlineRegistrationFactory()
    }

    factory = registration_factories[registration_type]

    enrollment = factory.create_enrollment()
    fee_calculator = factory.create_fee_calculator()

    enrollment_message = enrollment.enroll(
        student_name,
        course
    )

    final_fee = fee_calculator.calculate_fee(base_fee)

    print("\n[Abstract Factory]")
    print(enrollment_message)
    print(f"Registration Fee: {final_fee:.2f}")

    # -----------------------------------------
    # Register through Singleton
    # -----------------------------------------

    registration_id = manager.register_course(
        student_name,
        course
    )

    print("\n[Registration Manager]")
    print(f"Registration ID: {registration_id}")
    print("Registration completed successfully!")

    print("=" * 55)


def main():

    process_registration(
        "Hamonta",
        "CSE",
        "Regular",
        5000
    )

    process_registration(
        "Rejone",
        "CSE",
        "Online",
        5000
    )

    manager = RegistrationManager()

    print("\nTotal Registrations:")
    print(manager.get_total_registrations())


if __name__ == "__main__":
    main()