from fractions import Fraction as F
from variance_fptas import Coordinate, solve, exhaustive, objective, trim, State

cases = [
    (Coordinate(F(1), F(1), F(1), F(0), F(1)),),
    (Coordinate(F(0), F(1), F(1), F(0), F(1)),),
    (Coordinate(F(1,2), F(1,2), F(1), F(1,3), F(1)),)*2,
    (Coordinate(F(0), F(1,3), F(2), F(0), F(1)),
     Coordinate(F(1), F(2,3), F(5), F(1,8), F(1,2))),
    (Coordinate(F(1,3), F(2,3), F(1), F(0), F(1)),
     Coordinate(F(2,3), F(1,3), F(2), F(1,1000), F(1))),
]
for c in cases:
    r = solve(c, F(1,4))
    if r['status'] == 'NO_POSITIVE_EVENT_MASS':
        assert all(x.b == 0 for x in c)
    else:
        opt = objective(exhaustive(c))
        assert F(r['lower_bound']) <= opt <= F(r['upper_bound'])
        assert F(r['upper_bound']) <= (1+F(1,4))*F(r['lower_bound'])
        print(len(c), float(opt), float(F(r['lower_bound'])), float(F(r['upper_bound'])))
s = [State(F(0), F(0), 0), State(F(1), F(2), 1),
     State(F(21,20), F(3), 2), State(F(11,10), F(1), 3)]
t = trim(s, F(11,10))
assert len(t) == 3
assert t[1] == s[2] and t[2] == s[3]
for x in s:
    assert any(y.S <= F(11,10)*x.S and y.V >= x.V for y in t)
print('Development checks passed')
