from abc import ABC, abstractmethod


class FeeCalculator(ABC):

    @abstractmethod
    def calculate_fee(self, base_fee):
        pass


class RegularFeeCalculator(FeeCalculator):

    def calculate_fee(self, base_fee):
        return base_fee


class OnlineFeeCalculator(FeeCalculator):

    def calculate_fee(self, base_fee):
        return base_fee * 0.90