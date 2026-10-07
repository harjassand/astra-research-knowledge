"""Exact rational fixtures for the derived three-gain proof.

The general proof is in three_gain_regularization.txt. These fixtures only
check the recurrence, signs and profile-derivative cancellation; rank on
fixtures is not used to infer almost-everywhere rank.
"""
import itertools
import json
import random
import sympy as s


def fixture(r, z, a, at, az, h):
    e2, e3 = s.Matrix([0, 1, 0]), s.Matrix([0, 0, 1])
    t = [s.Integer(4), s.Integer(3), s.Integer(3), s.Integer(3)-h]
    v = [s.Matrix([r, 0, z])]
    x = [s.zeros(3, 1)]
    ls = []
    for i in range(3):
        x.append(x[-1] - (t[i]-t[i+1])*v[-1])
        n = v[-1] - a[i]*e3
        k = e2 if i == 1 else s.zeros(3, 1)
        li = -n.cross(k)/(n.dot(n)) if i == 1 else s.zeros(3, 1)
        assert n.cross(li) == k
        ls.append(li)
        v.append(v[-1] + k)
    jac = s.zeros(7, 12)
    jac[0, 2] = 1
    for col in range(12):
        dx, dv, dt_prev = s.zeros(3, 1), s.zeros(3, 1), s.Integer(0)
        for i in range(3):
            dt = s.Integer(col == i)
            dli = s.Matrix([s.Integer(col == 3+3*i+j) for j in range(3)])
            dx = dx - (dt_prev-dt)*v[i] - (t[i]-t[i+1])*dv
            dp = (at[i]*dt + az[i]*dx[2])*e3
            n = v[i] - a[i]*e3
            dv = dv + (dv-dp).cross(ls[i]) + n.cross(dli)
            dt_prev = dt
        jac[1:4, col] = dx
        jac[4:7, col] = dv
    _, pivots = jac.rref()
    assert len(pivots) == 7, (r, z, a, at, az, h, jac)
    det = s.factor(jac[:, list(pivots)].det())
    assert det != 0
    n3 = v[2]-a[2]*e3
    da = s.Matrix([1, -r, 0])
    db = s.Matrix([0, -n3[2], 1])
    assert n3.dot(da) == n3.dot(db) == 0
    spatial_det = s.Matrix.hstack(-h*da, -h*db, -e2).det()
    assert spatial_det == h*h
    return {"minor_columns":list(pivots), "minor_det":str(det),
            "spatial_det":str(spatial_det)}


random.seed(3107)
records = []
for _ in range(24):
    r = s.Rational(random.randint(1, 7), random.randint(1, 5))
    z = s.Rational(random.randint(-6, 6), random.randint(1, 5))
    a = [s.Rational(random.randint(-8, 8), random.randint(1, 5)) for _ in range(3)]
    at = [s.Rational(random.randint(-8, 8), random.randint(1, 5)) for _ in range(3)]
    az = [s.Rational(random.randint(-8, 8), random.randint(1, 5)) for _ in range(3)]
    h = s.Rational(random.randint(1, 4), 5)
    records.append(fixture(r, z, a, at, az, h))
print(json.dumps({"scope":"exact rational fixtures, not the general proof",
                  "fixtures":len(records), "all_rank_seven":True,
                  "first_three":records[:3]}, indent=2))
