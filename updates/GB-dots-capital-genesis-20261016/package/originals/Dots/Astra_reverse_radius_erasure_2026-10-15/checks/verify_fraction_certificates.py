"""Verify rational primal/dual examples without a numerical optimizer."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
T=[[F(x) for x in row] for row in json.loads((ROOT/'examples/cyclic_channel.json').read_text())]
record=json.loads((ROOT/'examples/cyclic_certificate.json').read_text())
p=list(map(F,record['p']));u=list(map(F,record['u']))
def bounds(T,p,u):
    n,m=len(T),len(T[0])
    assert all(x>=0 for row in T for x in row)
    assert all(sum(T[y][i] for y in range(n))==1 for i in range(m))
    assert min(p)>=0 and sum(p)==1
    J=[y for y in range(n) if all(T[y][i]>0 for i in range(m))]
    assert all(u[y]==0 for y in range(n) if y not in J)
    low=1-sum(1/sum(p[i]/T[y][i] for i in range(m)) for y in J)
    high=max(1-2*sum(u)+sum(u[y]**2/T[y][i] for y in J) for i in range(m))
    return low,high
assert bounds(T,p,u)==(F(record['lower']),F(record['upper']))==(F(2,11),F(2,11))
Z=[[F(0),F(1,2),F(1,2)],[F(1,2),F(0),F(1,2)],[F(1,2),F(1,2),F(0)]]
assert bounds(Z,[F(1,3)]*3,[F(0)]*3)==(F(1),F(1))
print('PASS: exact cyclic 2/11 and zero-common-support exclusion 1 certificates')
