from abc import ABC, abstractmethod

from abstract_factory.enrollment import (
    Enrollment,
    RegularEnrollment,
    OnlineEnrollment
)

from abstract_factory.fee_calculator import (
    FeeCalculator,
    RegularFeeCalculator,
    OnlineFeeCalculator
)


class RegistrationFactory(ABC):

    @abstractmethod
    def create_enrollment(self) -> Enrollment:
        pass

    @abstractmethod
    def create_fee_calculator(self) -> FeeCalculator:
        pass


class RegularRegistrationFactory(RegistrationFactory):

    def create_enrollment(self) -> Enrollment:
        return RegularEnrollment()

    def create_fee_calculator(self) -> FeeCalculator:
        return RegularFeeCalculator()


class OnlineRegistrationFactory(RegistrationFactory):

    def create_enrollment(self) -> Enrollment:
        return OnlineEnrollment()

    def create_fee_calculator(self) -> FeeCalculator:
        return OnlineFeeCalculator()