# University Course Registration System

A single, unified Python project demonstrating three **Creational Design Patterns** working together in one end-to-end workflow.

## 📖 Project Overview

This project implements a **University Course Registration System** that integrates three fundamental Creational Design Patterns into one cohesive workflow:

| Pattern              | Class                 | Purpose                                                                                                                             |
| -------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Singleton**        | `RegistrationManager` | Keeps registration records and IDs synchronized through a single centralized manager                                                |
| **Factory Method**   | `CourseCreator`       | Dynamically instantiates different course types (`CSECourse` vs. `EEECourse`)                                                       |
| **Abstract Factory** | `RegistrationFactory` | Generates matching enrollment and fee-calculation component families (`RegularRegistrationFactory` vs. `OnlineRegistrationFactory`) |

---

## 1. Singleton Pattern — `RegistrationManager`

**Category:** Creational Design Pattern

**Intent:** Ensure a class has only one instance throughout the application lifecycle and provide a global point of access to that instance.

### When to Use

- When a centralized registration manager must be shared across the entire application.
- When registration records and registration IDs must remain synchronized.
- When duplicate manager instances could result in inconsistent registration data.
- When a single object should coordinate registration activities.

### Problem Scenario

Without the Singleton pattern, different parts of the application could create separate `RegistrationManager` objects:

```python
manager_a = RegistrationManager()
manager_b = RegistrationManager()
```

If these were independent objects, each manager could maintain its own registration count, resulting in inconsistent registration IDs and incomplete records. The Singleton pattern guarantees every part of the application accesses the **same** `RegistrationManager` instance.

### Participants

- **Singleton (`RegistrationManager`)** — stores the single instance in `_instance` and controls object creation through `__new__`.
- **Client (`process_registration`)** — accesses the registration manager to register students and retrieve registration information.

### UML Structure (Conceptual)

```text
Student A --------\
                    \
                     +------> [ RegistrationManager ]
                    /          (Single Global Manager)
Student B --------/                    |
                                        |
                                        v
                               Registration Records
```

### Example Code

```python
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

        registration_id = (
            f"REG-{self.registration_count:03d}"
        )

        self.registrations.append({
            "id": registration_id,
            "student": student_name,
            "course": course
        })

        return registration_id

    def get_total_registrations(self):
        return self.registration_count
```

### Advantages

- Guarantees a single centralized registration manager.
- Keeps registration records synchronized.
- Prevents duplicate registration manager instances.
- Provides a common access point for registration management.

### Limitations

- Introduces global/shared state.
- Can make unit testing more difficult.
- Excessive use of Singleton can create unnecessary dependencies.
- Concurrent access would require additional synchronization in a multithreaded environment.

---

## 2. Factory Method Pattern — `CourseCreator`

**Category:** Creational Design Pattern

**Intent:** Define an interface for creating an object, but let subclasses decide which class to instantiate.

### When to Use

- When the system needs to create different types of courses.
- When the main registration logic should not directly instantiate concrete course classes.
- When new course types may be introduced in the future.
- When object creation should be separated from the main application logic.

### Problem Scenario

Without Factory Method, the main application could directly create courses using hardcoded conditional logic:

```python
if course_type == "CSE":
    course = CSECourse()
elif course_type == "EEE":
    course = EEECourse()
```

This creates direct dependencies between the main application and every concrete course class — adding a new course type would require modifying the core registration logic. Factory Method solves this by delegating course creation to dedicated creator classes.

### Participants

- **Product (`Course`)** — abstract interface representing a university course.
- **Concrete Products (`CSECourse`, `EEECourse`)** — specific course implementations.
- **Creator (`CourseCreator`)** — declares the Factory Method `create_course()`.
- **Concrete Creators (`CSECourseCreator`, `EEECourseCreator`)** — override `create_course()` to return specific course objects.

### UML Structure (Conceptual)

```text
                    Course
                      ^
                      |
             +--------+--------+
             |                 |
             v                 v
        CSECourse          EEECourse


                 CourseCreator
                      ^
                      |
             +--------+--------+
             |                 |
             v                 v
     CSECourseCreator   EEECourseCreator
             |                 |
          creates            creates
             |                 |
             v                 v
        CSECourse          EEECourse
```

### Example Code

```python
from abc import ABC, abstractmethod


# Product
class Course(ABC):

    def __init__(self, code, name, department):
        self.code = code
        self.name = name
        self.department = department

    @abstractmethod
    def get_details(self):
        pass


# Concrete Products
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


# Creator
class CourseCreator(ABC):

    @abstractmethod
    def create_course(self) -> Course:
        pass


# Concrete Creators
class CSECourseCreator(CourseCreator):

    def create_course(self) -> Course:
        return CSECourse()


class EEECourseCreator(CourseCreator):

    def create_course(self) -> Course:
        return EEECourse()
```

### Advantages

- Separates course creation from the main registration workflow.
- Reduces direct dependency on concrete course classes.
- Makes adding new course types easier.
- Supports better adherence to the Open/Closed Principle.
- Makes the course creation process more organized.

### Limitations

- Increases the number of classes.
- Adding many course types can result in many creator classes.
- The class hierarchy can become larger as the system grows.

---

## 3. Abstract Factory Pattern — `RegistrationFactory`

**Category:** Creational Design Pattern

**Intent:** Provide an interface for creating **families of related or dependent objects** without specifying their concrete classes.

### When to Use

- When a registration type requires a matching set of related components.
- When different registration modes should have their own compatible enrollment and fee-calculation objects.
- When incompatible combinations of registration components should be avoided.
- When the system may support additional registration families in the future.

### Registration Families

```text
RegularRegistrationFactory              OnlineRegistrationFactory
├── RegularEnrollment                   ├── OnlineEnrollment
└── RegularFeeCalculator                └── OnlineFeeCalculator
```

### Problem Scenario

Without Abstract Factory, the main application could independently create mismatched components:

```python
enrollment = RegularEnrollment()
fee_calculator = OnlineFeeCalculator()
```

This creates an incompatible combination — the enrollment is Regular while the fee calculator is Online. Abstract Factory prevents this by ensuring each concrete factory creates a matching family of objects.

### Participants

- **Abstract Product (`Enrollment`)** — defines the interface for student enrollment.
- **Concrete Products (`RegularEnrollment`, `OnlineEnrollment`)** — implement specific enrollment behavior.
- **Abstract Product (`FeeCalculator`)** — defines the interface for calculating registration fees.
- **Concrete Products (`RegularFeeCalculator`, `OnlineFeeCalculator`)** — implement specific fee calculation behavior.
- **Abstract Factory (`RegistrationFactory`)** — declares `create_enrollment()` and `create_fee_calculator()`.
- **Concrete Factories (`RegularRegistrationFactory`, `OnlineRegistrationFactory`)** — create matching product families.

### UML Structure (Conceptual)

```text
                    RegistrationFactory
                           ^
                           |
              +------------+------------+
              |                         |
              v                         v
 RegularRegistrationFactory    OnlineRegistrationFactory
              |                         |
       +------+-------+          +------+-------+
       |              |          |              |
       v              v          v              v
RegularEnrollment  RegularFee  OnlineEnrollment OnlineFee
                   Calculator                   Calculator
```

### Example Code

```python
from abc import ABC, abstractmethod


# Abstract Product
class Enrollment(ABC):

    @abstractmethod
    def enroll(self, student_name, course):
        pass


# Concrete Products
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


# Abstract Product
class FeeCalculator(ABC):

    @abstractmethod
    def calculate_fee(self, base_fee):
        pass


# Concrete Products
class RegularFeeCalculator(FeeCalculator):

    def calculate_fee(self, base_fee):
        return base_fee


class OnlineFeeCalculator(FeeCalculator):

    def calculate_fee(self, base_fee):
        return base_fee * 0.90


# Abstract Factory
class RegistrationFactory(ABC):

    @abstractmethod
    def create_enrollment(self) -> Enrollment:
        pass

    @abstractmethod
    def create_fee_calculator(self) -> FeeCalculator:
        pass


# Concrete Factory
class RegularRegistrationFactory(RegistrationFactory):

    def create_enrollment(self) -> Enrollment:
        return RegularEnrollment()

    def create_fee_calculator(self) -> FeeCalculator:
        return RegularFeeCalculator()


# Concrete Factory
class OnlineRegistrationFactory(RegistrationFactory):

    def create_enrollment(self) -> Enrollment:
        return OnlineEnrollment()

    def create_fee_calculator(self) -> FeeCalculator:
        return OnlineFeeCalculator()
```

### Advantages

- Guarantees compatibility between related registration components.
- Prevents mixing Regular and Online registration components.
- Separates object creation from the client.
- Makes adding a new registration family easier.
- Improves organization and maintainability.

### Limitations

- Adding a new product type may require changes to every concrete factory.
- The number of classes increases as more product families are introduced.
- May be unnecessarily complex for a very small registration system.

---

## 4. Integrated System Demonstration

All three patterns are combined into a single registration workflow:

```python
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

    # 1. Singleton: Get the centralized registration manager
    manager = RegistrationManager()

    print("\n[Singleton]")
    print("Using centralized RegistrationManager")

    # 2. Factory Method: Create the required course
    course_creators = {
        "CSE": CSECourseCreator(),
        "EEE": EEECourseCreator()
    }

    creator = course_creators[course_type]
    course = creator.create_course()

    print("\n[Factory Method]")
    print(f"Created Course: {course.get_details()}")

    # 3. Abstract Factory: Create matching registration components
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

    # 4. Register through Singleton
    registration_id = manager.register_course(
        student_name,
        course
    )

    print("\n[Registration Manager]")
    print(f"Registration ID: {registration_id}")
    print("Registration completed successfully!")

    print("=" * 55)
```

### Sample Output

```text
=======================================================
        UNIVERSITY COURSE REGISTRATION
=======================================================
Student: Hamonta
Course Type: CSE
Registration Type: Regular

[Singleton]
Using centralized RegistrationManager

[Factory Method]
Created Course: CSE3206 - Software Engineering (Computer Science and Engineering)

[Abstract Factory]
Hamonta enrolled in CSE3206 through regular enrollment.
Registration Fee: 5000.00

[Registration Manager]
Registration ID: REG-001
Registration completed successfully!
=======================================================

=======================================================
        UNIVERSITY COURSE REGISTRATION
=======================================================
Student: Rejone
Course Type: CSE
Registration Type: Online

[Singleton]
Using centralized RegistrationManager

[Factory Method]
Created Course: CSE3206 - Software Engineering (Computer Science and Engineering)

[Abstract Factory]
Rejone enrolled in CSE3206 through online enrollment.
Registration Fee: 4500.00

[Registration Manager]
Registration ID: REG-002
Registration completed successfully!
=======================================================

Total Registrations: 2
```

---

## 5. Technologies Used

- Python 3
- Object-Oriented Programming
- Abstract Base Classes (`ABC`)
- Singleton Design Pattern
- Factory Method Design Pattern
- Abstract Factory Design Pattern
- PlantUML
- Git
- GitHub

---

## 6. How to Run

### Requirements

- Python 3.x
- VS Code or another Python-compatible IDE

No external Python packages are required.

### Run the Application

Open the project directory in VS Code, open a terminal, and run:

```bash
python main.py
```

On Windows, if necessary:

```bash
py main.py
```

---

## 7. Conclusion

By combining all three patterns into a single **University Course Registration System**:

- **Singleton (`RegistrationManager`)** ensures centralized registration management and synchronized registration IDs.
- **Factory Method (`CourseCreator`)** provides flexible creation of different university courses.
- **Abstract Factory (`RegistrationFactory`)** ensures consistent and compatible registration families for Regular and Online registration.

The resulting architecture is modular, extensible, loosely coupled, and demonstrates standard Object-Oriented Design principles.

### Future Extensions

- Additional courses and departments
- Additional registration types
- Database integration
- Student authentication
- Course capacity management
- A web-based frontend
