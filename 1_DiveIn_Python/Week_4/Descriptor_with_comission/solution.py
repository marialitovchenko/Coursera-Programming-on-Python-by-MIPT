"""
Write a descriptor which would take a commission from value on the account
"""


class Value:
    def __init__(self):
        pass

    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value * (1 - instance.commission)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
