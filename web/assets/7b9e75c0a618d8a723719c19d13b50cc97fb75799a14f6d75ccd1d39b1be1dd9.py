"""Exact rational replay of the finite-rank CP / no-reversible-frame example.

Reads the frozen certificate at work/sol/hidden_realization/exact_certificate_v1.json.
Only Python's standard library is required; all mathematical comparisons use Fraction.
"""
from fractions import Fraction as F
from pathlib import Path
import json

CERT = Path(__file__).resolve().parents[2] / 'sol' / 'hidden_realization' / 'exact_certificate_v1.json'
d = json.loads(CERT.read_text())
def mat(k): return [[F(x) for x in row] for row in d[k]]
def req(ok, label):
    if not ok: raise RuntimeError(label)
def tr(a): return [list(row) for row in zip(*a)]
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def minus(a,b): return [[x-y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]
def iszero(a): return all(x == 0 for row in a for x in row)
def det(a):
    a = [row[:] for row in a]
    out = F(1)
    for i in range(len(a)):
        q = next((j for j in range(i, len(a)) if a[j][i]), None)
        if q is None: return F(0)
        if q != i: a[i], a[q], out = a[q], a[i], -out
        p = a[i][i]; out *= p
        for j in range(i+1, len(a)):
            r = a[j][i] / p
            for k in range(i, len(a)): a[j][k] -= r*a[i][k]
    return out

def dot(a,b): return sum(x*y for x,y in zip(a,b))

def main():
    v, z, D, M, L, Q, H = (mat(k) for k in ('points','farkas_z','internal_D','M','L','Q','H'))
    C, facets, B = mat('covariance'), mat('facets'), mat('B')
    eta, reset = F(d['marker_eta']), F(d['reset_rate'])
    n, r = 10, 8
    req(len(v)==5 and len(Q)==n and len(H)==n and len(H[0])==r, 'declared dimensions')
    req(all(dot(p,p)==1 for p in v) and len({tuple(p) for p in v})==5, 'distinct rational unit-circle points')
    req(all(x >= 0 for i,row in enumerate(Q) for j,x in enumerate(row) if i!=j), 'nonnegative CTMC off-diagonal')
    req(all(sum(row)==0 for row in Q), 'generator row sums')
    req(all(sum(Q[i][j] for i in range(n))==0 for j in range(n)), 'uniform stationarity')
    req(Q[0][1] != Q[1][0], 'hidden generator is not reversible')
    req(all(Q[i][j] > 0 for i in range(5) for j in range(5) if i!=j), 'strictly positive internal rates')
    req(all(sum(Q[i][5+k] for i in range(5)) > 0 for k in range(5)), 'every marker is connected')
    req(B[0][0] > 0 and det(B) == F(911,40000), 'positive-definite base drift matrix')
    req(C[0][0] > 0 and det(C) > 0, 'positive-definite centered covariance')
    req(iszero(minus(mm(C,tr(D)),mm(D,C))), 'C D^T = D C: internal drift selfadjointness')
    req(det([[sum(D[i][k]*C[k][j] for k in range(2)) for j in range(2)] for i in range(2)]) > 0, 'positive internal dissipation form')
    req(all((Q[i][j]>0)==(Q[j][i]>0) for i in range(n) for j in range(i+1,n)), 'symmetric support')
    req(iszero(minus(mm(Q,H),mm(H,L))), 'QH=HL: observable subspace invariant')
    req(iszero(minus(mm(M,L),mm(tr(L),M))), 'M-selfadjoint restricted generator')
    req(M==[[sum(H[k][i]*H[k][j] for k in range(n))/10 for j in range(r)] for i in range(r)], 'observable Gram matrix')
    req(det(M)>0, 'full observable rank (Gram matrix is positive definite)')
    omega=[F(1),F(0),F(0),F(1),F(1),F(1),F(1),F(1)]
    req(mm(L, [[x] for x in omega]) == [[F(0)] for _ in range(r)], 'stationary observable vector')
    req(dot(omega, [sum(M[i][j]*omega[j] for j in range(r)) for i in range(r)]) == 1, 'unit norm constant')
    req(M[1][1]+M[2][2] == F(1,2), 'internal position second-moment trace')
    req(M[0][0] == F(1,2), 'internal frame mass')
    req(all(M[3+k][3+k] == F(1,10) for k in range(5)), 'marker masses')
    # The five polygon facets are exactly the oriented edges in the recorded CCW order.
    order=d['ccw_order']
    derived=[]
    for k,i in enumerate(order):
        j=order[(k+1)%5]
        ex,ey=v[j][0]-v[i][0],v[j][1]-v[i][1]
        derived.append([ey*v[i][0]-ex*v[i][1], ey, -ex])
        # Certificate uses determinant(edge, point - start): (c,-ey,ex).
        derived[-1]=[ey*v[i][0]-ex*v[i][1], -ey, ex]
    req(derived==facets, 'recorded facet equations')
    req(all(f[0]+f[1]*p[0]+f[2]*p[1] >= 0 for f in facets for p in v), 'vertices satisfy every facet')
    req(all(f[0]+f[1]*p[0]+f[2]*p[1] > 0 for k,f in enumerate(facets) for j,p in enumerate(v) if j not in (order[k],order[(k+1)%5])), 'strictly convex pentagon facets')
    req(any(det([facets[i],facets[j],facets[k]]) != 0 for i in range(5) for j in range(i+1,5) for k in range(j+1,5)), 'facet affine functions span internal affine space')
    req(all(f[0]+f[1]*v[order[k]][0]+f[2]*v[order[k]][1] == 0 and f[0]+f[1]*v[order[(k+1)%5]][0]+f[2]*v[order[(k+1)%5]][1] == 0 for k,f in enumerate(facets)), 'each facet is its ordered edge')
    req(all(sum(f[1] for f in facets)==0 and sum(f[2] for f in facets)==0 for _ in [0]), 'constant total facet slack')
    req(all(Q[i][5+k] == eta*(facets[k][0]+facets[k][1]*v[i][0]+facets[k][2]*v[i][1]) == Q[5+k][i] for i in range(5) for k in range(5)), 'symmetric marker rates equal eta times facet slack')
    req(len({sum(Q[i][5+k] for k in range(5)) for i in range(5)})==1, 'constant total marker exit rate')
    # Exact stationary five-point moment representation and nondegenerate recovery.
    mean=[sum(p[k] for p in v)/5 for k in range(2)]
    u=[[p[k]-mean[k] for k in range(2)] for p in v]
    req(C==[[sum(u[i][a]*u[i][b] for i in range(5))/5 for b in range(2)] for a in range(2)], 'centered covariance')
    feat=[[1,p[0],p[1],p[0]*p[0],p[0]*p[1]] for p in v]
    req(det(tr(feat)) == F(d['five_point_moment_determinant']) != 0, 'unique vertex moment weights')
    req(sum(F(1,10) for p in v)==M[0][0], 'uniform internal mass')
    req(sum(F(1,10)*p[0] for p in v)==M[0][1] and sum(F(1,10)*p[1] for p in v)==M[0][2], 'uniform first moments agree with M')
    req(sum(F(1,10)*p[0]**2 for p in v)==M[1][1] and sum(F(1,10)*p[0]*p[1] for p in v)==M[1][2], 'uniform second moments agree with M')
    # Exact planar monotone-field witness, including all 10 internal pairs.
    pairings=[]
    for i in range(5):
        for j in range(i+1,5):
            q=dot([z[i][k]-z[j][k] for k in range(2)],[v[i][k]-v[j][k] for k in range(2)])
            req(q>0, 'strict monotonicity between distinct vertices')
            pairings.append(q)
    req(pairings==[F(x) for x in d['monotonicity_pairings']], 'exact monotonicity values')
    planar=sum(dot(z[i], [sum(D[a][b]*u[i][b] for b in range(2)) for a in range(2)])/5 for i in range(5))
    req(planar==F(d['farkas_drift_pairing'])<0, 'negative planar drift pairing')
    # Internal generator drift is -D(p_i-mean); marker killing contributes only -kappa*p_i.
    for i in range(5):
        drift=[sum(Q[i][j]*(v[j][a]-v[i][a]) for j in range(5)) for a in range(2)]
        req(drift==[-sum(D[a][b]*u[i][b] for b in range(2)) for a in range(2)], 'exact internal drift')
    # Lift the planar monotone fields to the full 8-coordinate OS space.
    # Test coefficient d_i=(0,z_i,(z_i dot p_i) 1_5); marker test vectors are zero.
    # This makes internal/marker monotonicity exactly zero and cancels marker killing in the Farkas sum.
    full=F(0)
    xis=[]
    for i in range(5):
        xi=H[i]
        xis.append(xi)
        di=[F(0),z[i][0],z[i][1]]+[dot(z[i],v[i])]*5
        full += F(1,10)*dot(di,[-x for x in mm([xi],L)[0]])
    for k in range(5): xis.append(H[5+k])
    req(all(dot([0,z[i][0],z[i][1]]+[dot(z[i],v[i])]*5,[xis[i][a]-xis[5+k][a] for a in range(8)])==0 for i in range(5) for k in range(5)), 'zero internal-marker monotonicity')
    req(full==planar/2<0, 'full eight-dimensional Farkas pairing remains strictly negative')
    # Keep the Farkas test valid with arbitrary duplicate atoms at a forced vertex/marker.
    print(json.dumps({
        'status':'PASS', 'arithmetic':'fractions.Fraction', 'states':10, 'labels':6,
        'observable_rank':8, 'generator_nonreversible_witness':[str(Q[0][1]),str(Q[1][0])],
        'min_internal_monotonicity':str(min(pairings)),
        'planar_pairing':str(planar), 'full_frame_pairing':str(full),
        'five_point_moment_determinant':str(det(tr(feat))),
        'marker_total_exit':str(sum(Q[0][5+k] for k in range(5)))
    },indent=2))

if __name__=='__main__': main()
