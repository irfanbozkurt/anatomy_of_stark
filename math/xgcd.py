
def xgcd(x, y):
	old_a, a, old_b, b, old_gcd, gcd = 1, 0, 0, 1, x, y
	while gcd != 0:
		quotient = old_gcd // gcd
		old_gcd, gcd = gcd, old_gcd - quotient * gcd
		old_a, a = a, old_a - quotient * a
		old_b, b = b, old_b - quotient * b
	return old_a, old_b, old_gcd

def test_xgcd(): assert xgcd(1398, 324) == (-19,82,6)
