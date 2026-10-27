"""Exact metadata certificates plus pathwise nonlinear-query replay.
The full law follows from Gaussian orthogonal decomposition, not moments.
"""
from pathlib import Path
import numpy as np
from fractions import Fraction as R

ROOT = Path(__file__).resolve().parent
def mat(x): return [[R(v) for v in row] for row in x]
def tr(x): return list(map(list,zip(*x)))
def mm(x,y): return [[sum((a*b for a,b in zip(row,col)),R(0)) for col in tr(y)] for row in x]
def add(x,y): return [[a+b for a,b in zip(rx,ry)] for rx,ry in zip(x,y)]
def neg(x): return [[-a for a in row] for row in x]
def sub(x,y): return add(x,neg(y))
def eye(n): return [[R(i==j) for j in range(n)] for i in range(n)]
def zeros(n,m): return [[R(0) for _ in range(m)] for _ in range(n)]
def inv(x):
    n=len(x)
    z=[row[:]+unit for row,unit in zip(x,eye(n))]
    for j in range(n):
        pivot=next(i for i in range(j,n) if z[i][j])
        z[j],z[pivot]=z[pivot],z[j]
        t=z[j][j]
        z[j]=[v/t for v in z[j]]
        for i in range(n):
            if i!=j:
                t=z[i][j]
                z[i]=[a-t*b for a,b in zip(z[i],z[j])]
    return [row[n:] for row in z]
B = mat([[1,0,R(1,5),0,0,0], [R(3,10),1,0,R(1,10),0,0],
         [0,R(1,5),1,0,R(1,5),0], [R(1,10),0,R(1,5),1,0,R(3,10)]])
D = mat([[R(1,10),0,0,0,1,R(1,5)], [0,R(1,10),0,0,R(1,5),1]])
b = mat([[1],[R(4,5)],[R(6,5)],[R(9,10)]])
c = mat([[R(1,5)],[R(-1,10)]])
Bplus = mm(tr(B),inv(mm(B,tr(B))))
P = mm(Bplus,B)
reserve = mm(mm(D,sub(eye(6),P)),tr(D))
reserve_det = reserve[0][0]*reserve[1][1]-reserve[0][1]*reserve[1][0]
v0 = neg(mm(Bplus,b))
affine = sub(c,mm(mm(D,Bplus),b))
W = mm(mm(sub(eye(6),P),tr(D)),inv(reserve))
assert mm(P,P) == P and tr(P) == P
assert mm(B,v0) == neg(b) and mm(B,W) == zeros(4,2)
assert mm(D,W) == eye(2) and mm(tr(W),W) == inv(reserve)
assert mm(tr(v0),W) == zeros(1,2)
assert reserve[0][0] > 0 and reserve_det > 0
assert add(c,mm(D,v0)) == affine

def arr(matrix):
    return np.array(matrix, dtype=float)

def run():
    rng = np.random.default_rng(27102611)
    d = 11
    rot,_ = np.linalg.qr(rng.normal(size=(d,d)))
    offset = rng.normal(size=d)
    phase = rng.normal(size=d)
    calls = 0
    def g(x):
        nonlocal calls
        calls += 1
        return offset + .7*rot@np.tanh(rot.T@x+phase)
    Bn,Dn,bn,cn,Pn,vn,Wn,an = [arr(x) for x in (B,D,b,c,P,v0,W,affine)]
    lower = np.array([[0,0,0,0],[.1,0,0,0],[-.08,.12,0,0],[.07,0,.09,0]])
    fout = np.array([[.2,-.1,.3,.1],[-.15,.2,.05,.25]])
    u = rng.normal(size=(4,d))
    constant = rng.normal(size=(2,d))
    def program(x,z):
        values=[]
        points=[]
        for i in range(4):
            q=u[i]+bn[i,0]*x+Bn[i]@z
            for j in range(i):
                q=q+lower[i,j]*values[j]
            points.append(q)
            values.append(g(q))
        return cn*x+constant+fout@np.array(values)+Dn@z, np.array(points)
    worst = dict(query_gauge=0., affine_response=0., reserve_queries=0.,
                 reserve_decomposition=0., output_response_queries=0., output_response=0.)
    for _ in range(64):
        x=rng.normal(size=d)
        z=rng.normal(size=(6,d))
        delta=rng.normal(size=d)
        h=rng.normal(size=(2,d))
        y,points=program(x,z)
        yg,pg=program(x+delta,z+vn*delta)
        yr,pr=program(x,Pn@z)
        yo,po=program(x,z+Wn@h)
        tests = dict(query_gauge=np.max(np.abs(pg-points)),
            affine_response=np.max(np.abs(yg-y-an*delta)),
            reserve_queries=np.max(np.abs(pr-points)),
            reserve_decomposition=np.max(np.abs(y-yr-Dn@(np.eye(6)-Pn)@z)),
            output_response_queries=np.max(np.abs(po-points)),
            output_response=np.max(np.abs(yo-y-h)))
        for key,value in tests.items():
            worst[key]=max(worst[key],value)
    assert max(worst.values()) < 1e-12
    assert calls==64*4*4
    lines=['AFFINE ORACLE NORMAL-FORM CHECKS',
        'Exact rational projection, reserve positivity, gauge and response identities: PASS',
        'Exact rational gauge/response orthogonality: PASS',
        f'Exact known affine response: {[str(row[0]) for row in affine]}',
        f'Exact reserve determinant: {reserve_det}',
        f'Nonlinear conservative query-replay dimension: {d}',
        f'Total original source calls (including three separate replays): {calls}']
    lines += [f'Max floating residual {key}: {value:.17g}' for key,value in worst.items()]
    lines += ['No source mean is provided or fitted. No empirical moment/TV inference.',
              'Proof is the exact Gaussian orthogonal-decomposition identity.']
    result='\n'.join(lines)+'\n'
    (ROOT/'NORMAL_FORM_CHECK_RESULTS.txt').write_text(result)
    print(result)

if __name__=='__main__':
    run()
