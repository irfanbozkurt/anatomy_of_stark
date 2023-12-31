from math.field.field_element import FieldElement
from math.polynomial.univariate import Polynomial
from stark import StarkField


stark_field = StarkField()


######################################################################
######## Print generators of all multiplicative subgroups of order 2^k
######################################################################
# print(stark_field.generator())
# for i in reversed(range(119)):
# 	print(stark_field.primitive_nth_root_of_unity(1 << i))

######################################################################
######## Univariate Polynomial tests
######################################################################
assert Polynomial([]).degree() == -1
assert Polynomial([
	stark_field.zero(),
	stark_field.zero(),
	stark_field.zero(),
]).degree() == -1
assert Polynomial([
	stark_field.one(),
	stark_field.zero(),
	stark_field.zero(),
]).degree() == 0
assert Polynomial([
	stark_field.zero(),
	stark_field.one(),
	stark_field.zero(),
]).degree() == 1

p1 = Polynomial([
	FieldElement(1, stark_field),
	FieldElement(2, stark_field),
])
p2 = Polynomial([
	FieldElement(3, stark_field),
	FieldElement(4, stark_field),
])
assert(p1 != p2)
assert(p1 + p2 == Polynomial([
	FieldElement(4, stark_field),
	FieldElement(6, stark_field),
]))
assert(p2 - p1 == Polynomial([
	FieldElement(2, stark_field),
	FieldElement(2, stark_field),
]))
p3 = p2 * p1
assert(p3 == Polynomial([
	FieldElement(3, stark_field),
	FieldElement(10, stark_field),
	FieldElement(8, stark_field),
]))
assert(p3.leading_coeff().value == 8)

q, r = Polynomial.textbook_division(p3, p2)
assert(r.degree() == -1)
assert(q == p1)

q, r = Polynomial.textbook_division(p3, p1)
assert(r.degree() == -1)
assert(q == p2)

p2_cube = (p2^3)
p2_cube_coeffs = [27,108,144,64]
assert(list(map(lambda x: x.value, p2_cube.coefficients)) == p2_cube_coeffs)

p2_cube_zerofier = Polynomial.zerofier(p2_cube.coefficients)

zerofier_evaluated_1 = p2_cube_zerofier.evaluate_domain(p2_cube.coefficients)
for x in zerofier_evaluated_1: assert(x == stark_field.zero())
zerofier_evaluated_2 = (p2_cube_zerofier * p3).evaluate_domain(p2_cube.coefficients)
for x in zerofier_evaluated_2: assert(x == stark_field.zero())

p2_cube_scaled_by_2 = p2_cube.scale(FieldElement(2, stark_field))
assert(list(map(lambda x: x.value, p2_cube_scaled_by_2.coefficients)) == [27,216,576,512])

stark_one = stark_field.one()
stark_two = stark_one + stark_one
stark_four = stark_two + stark_two
stark_eight = stark_four + stark_four
assert(Polynomial.test_colinearity([
	[-stark_one,-stark_two], 
	[stark_one,stark_two], 
	[stark_two,stark_four],
	[stark_four, stark_eight],
]))
