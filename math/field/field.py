from math.field.field_element import FieldElement
from math.xgcd import xgcd

class Field:
    def __init__(self, p): self.p = p
    def __str__(self): return str(self.p)

    def zero(self): return FieldElement(0, self)
    def one(self): return FieldElement(1, self)

    def add(self, left, right):
        return FieldElement((left.value + right.value) % self.p, self)
    def neg(self, operand):
        return FieldElement((self.p - operand.value) % self.p, self)
    def sub(self, left, right):
        return FieldElement((self.p + left.value - right.value) % self.p, self)
    def mul(self, left, right):
        return FieldElement((left.value * right.value) % self.p, self)
    def inv(self, operand):
        a, _, _ = xgcd(operand.value, self.p)
        return FieldElement(a, self)
    def div(self, left, right):
        assert(not right.is_zero()), "division by zero"
        a, _, _ = xgcd(right.value, self.p)
        return FieldElement(left.value * a % self.p, self)
