class Polynomial:
	def __init__(self, coefficients): 
		# For a degree-zero polynomial, coefficients = [c0]
		self.coefficients = coefficients

	# Degree of zero polynomial will be -1
	def degree(self):
		if self.coefficients == []: return -1

		zero = self.coefficients[0].field.zero()
		max_index = -1
		for i in range(len(self.coefficients)):
			if self.coefficients[i] != zero: max_index = i

		return max_index

	def textbook_division(num, denom):
		denom_deg, num_deg = denom.degree(), num.degree()
		if denom_deg == -1: return None, None
		if num_deg < denom_deg: return (Polynomial([]), num)

		field = denom.coefficients[0].field
		zero = field.zero()

		max_q_coeff_size = (num_deg - denom_deg + 1)

		r = Polynomial([n for n in num.coefficients])
		q_coeff = [zero] * max_q_coeff_size
		for _ in range(max_q_coeff_size):
			r_deg = r.degree()
			if r_deg < denom_deg: break
			c = r.leading_coeff() / denom.leading_coeff()
			shift = r_deg - denom_deg
			q_coeff[shift] = c
			r -= Polynomial([zero] * shift + [c]) * denom

		return Polynomial(q_coeff), r

	# O(n^2) evaluation
	def evaluate( self, point ):
		xi = point.field.one()
		value = point.field.zero()
		for c in self.coefficients:
			value += c * xi
			xi *= point
		return value

	def evaluate_domain( self, domain ):
		return [self.evaluate(d) for d in domain]

	# O(n^2) Lagrange
	def interpolate_domain( domain, values ):
		assert(len(domain) == len(values)), "number of elements in domain does not match number of values -- cannot interpolate"
		assert(len(domain) > 0), "cannot interpolate between zero points"
		field = domain[0].field
		x = Polynomial([field.zero(), field.one()])
		acc = Polynomial([])
		for i in range(len(domain)):
			prod = Polynomial([values[i]])
			for j in range(len(domain)):
				if j == i: continue
				prod *= (x - Polynomial([domain[j]])) * Polynomial([(domain[i] - domain[j]).inv()])
			acc += prod
		return acc

	# Z_D(x) = (x-d_1)*(x-d_2)*...
	def zerofier(domain):
		field = domain[0].field
		x = Polynomial([field.zero(), field.one()])
		acc = Polynomial([field.one()])
		for d in domain: acc *= x - Polynomial([d])
		return acc

	def scale(self, factor):
		return Polynomial(
			[(factor^i) * self.coefficients[i] for i in range(len(self.coefficients))]
		)

	# Do given points form a perfect line?
	def test_colinearity(points):
		return Polynomial.interpolate_domain(
			[p[0] for p in points],
			[p[1] for p in points]
		).degree() <= 1
	
	def is_zero(self): return self.degree() == -1
	@staticmethod
	def zero(): return Polynomial([])

	def leading_coeff(self): return self.coefficients[self.degree()]
	
	def __str__(self): return ",".join(list(map(lambda x: str(x), self.coefficients)))

	def __eq__(self, other):
		deg = self.degree()
		if deg != other.degree(): return False
		if deg == -1: return True

		for i in range(len(self.coefficients)): 
			if self.coefficients[i] != other.coefficients[i]: return False

		return True
	def __neq__(self, other): return not self == other

	def __add__(self, other):
		if self.is_zero(): return other
		if other.is_zero(): return self

		field1, field2 = self.coefficients[0].field, other.coefficients[0].field
		assert(field1.p == field2.p), "Polynomials to be added must belong to the same field"

		len1, len2 = len(self.coefficients), len(other.coefficients)
		coeffs = [field1.zero()] * max(len1, len2)
		for i in range(len1): coeffs[i] += self.coefficients[i]
		for i in range(len2): coeffs[i] += other.coefficients[i]

		return Polynomial(coeffs)
	def __neg__(self): return Polynomial([-c for c in self.coefficients])
	def __sub__(self, other): return self + (-other)

	# Textbook mul
	def __mul__(self, other):
		if self.is_zero() or other.is_zero(): return Polynomial.zero()
		zero = self.coefficients[0].field.zero()
		len1, len2 = len(self.coefficients), len(other.coefficients)
		coeffs = [zero] * (len1 + len2 - 1)
		for i in range(len1):
			if self.coefficients[i].is_zero(): continue
			for j in range(len2):
				coeffs[i + j] += self.coefficients[i] * other.coefficients[j]
		return Polynomial(coeffs)
	def __truediv__(self, other):
		q, r = Polynomial.textbook_division(self, other)
		assert(r.is_zero()), "Remainder is not zero. Cannot do a full div. Subtract the modulo first"
		return q
	def __mod__(self, other):
		_, r = Polynomial.textbook_division(self, other)
		return r
	
	# Exponentiate via square & multiply
	def __xor__(self, exp):
		if self.is_zero(): return Polynomial([])
		if exp == 0: return Polynomial([self.coefficients[0].field.one()])

		acc = Polynomial([self.coefficients[0].field.one()])
		for i in reversed(range(len(bin(exp)[2:]))):
			acc *= acc
			if (1 << i) & exp != 0: acc *= self
		return acc
