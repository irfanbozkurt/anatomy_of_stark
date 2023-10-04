from math.field.field_element import FieldElement
from math.field.field import Field

class StarkField(Field):
	def __init__(self): self.p = 1 + 11 * 37 * (1 << 119)
	
	# Generator of multiplicative subgroup of order 2^119
	def generator(self): 
		return FieldElement(85408008396924667383611388730472331217, self)
	
	# As we keep squaring the generator, we'll get the generator 
	# of the next 2^k'th roots of unity:  g_{2^k}^2 = g_{2^(k-1)}
	# "next" subgroup is half the size of the first subgroup
	def primitive_nth_root_of_unity(self, n):
		assert(n & (n-1) == 0), "There are only subgroups of order 2^n"
		assert(n <= (1 << 119)), "There's no subgroup of order > 2^119"

		root = self.generator()
		order = 1 << 119
		while order != n:
			root ^= 2
			order /= 2

		return root
	
	# Samples a random field element based on provided randomness
	def sample(self, byte_array):
		base = 0
		for byte in byte_array: base = ((base << 8) ^ int(byte)) % self.p
		return FieldElement(base, self)
