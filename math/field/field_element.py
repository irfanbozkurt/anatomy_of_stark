class FieldElement:
	def __init__(self, value, field):
		self.value = value
		self.field = field

	def __eq__(self, other): return self.value == other.value and self.field == other.field
	def __neq__(self, other): return not self.__eq__(other)
	def __str__(self): return str(self.value)
	def __bytes__(self): return bytes(str(self).encode())

	def is_zero(self): return self.value == 0

	def __add__(self, other): return self.field.add(self, other)
	def __neg__(self): return self.field.neg(self)
	def __sub__(self, other): return self.field.sub(self, other)

	def __mul__(self, other): return self.field.mul(self, other)
	def inv(self): return self.field.inv(self)
	def __truediv__(self, other): return self.field.div(self, other)
	def __xor__(self, exp):
		acc = FieldElement(1, self.field)
		if exp == 0: return acc
		if exp == 1: return self

		val = FieldElement(self.value, self.field)
		for i in reversed(range(len(bin(exp)[2:]))):
			acc = acc * acc
			if (1 << i) & exp != 0: acc = acc * val

		return acc

# def test_exp():
# 	elem = FieldElement(1, )
