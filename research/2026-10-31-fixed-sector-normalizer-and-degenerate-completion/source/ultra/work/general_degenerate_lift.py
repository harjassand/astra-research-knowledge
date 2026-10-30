"""Exact diagnostic: finite-codimension boundary heat lifts on other planes.

Every reported dimension is exact algebra. A family-wide theorem is not
inferred from finitely many ray pairs; no global heat bound is claimed here.
"""
from pathlib import Path
from fractions import Fraction as R
import json,sys,time
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'))
import heat_model as h
b,r,ca=h.b,h.r,h.ca
source=(root/'work/graded_heat_lift.py').read_text();ns={'__file__':str(root/'work/graded_heat_lift.py'),'__name__':'root_rows'};exec(source[:source.index('c0=[R(q)')],ns)
E0,RHS0,CB,powers=ns['E'],ns['RHS'],ns['CB'],ns['powers']
sys.path.insert(0,str(root/'outputs/acoustic_capacity'));import kernel as ks
ss=(root/'work/degenerate_quadratic_lift.py').read_text();nns={'__name__':'nullspace_only','R':R};exec(ss[ss.index('def nullbasis(A):'):ss.index('zz=nullbasis(J)')],nns);nullbasis=nns['nullbasis']
def test(pairs):
    E=[row[:] for row in E0];rhs=[row[:] for row in RHS0];J=[]
    for u,xi in pairs:
        ray=[R(a*c) for a in u for c in xi];J+=ks.feature_factor(ray,'closed')[1]
        kh=[R(u[0]*xi[0]**2),R(u[0]*xi[0]*xi[1]),R(u[0]*xi[1]**2),R(u[1]*xi[0]**2),R(u[1]*xi[0]*xi[1]),R(u[1]*xi[1]**2)]
        for a in range(4):
            A=[R(int(i==a)) for i in range(4)]
            for i in range(6):
                E.append([sum(R(float(h.XB[a,i,j,l]))*kh[j] for j in range(6)) for l in range(80)])
                row=[]
                for pw in powers:
                    P={tuple(pw):R(1)};HC=[[b.evaluate(b.diff(b.diff(P,j),k),A) for k in range(4)] for j in range(4)];V=[[R(0)]*6 for _ in range(6)]
                    for ids in ((0,1,3,4),(1,2,4,5)):
                        for j in range(4):
                            for k in range(4):V[ids[j]][ids[k]]+=HC[j][k]/2
                    row.append(-sum(V[i][j]*kh[j] for j in range(6)))
                rhs.append(row)
    rk=b.rank(E);aug=b.rank([a+c for a,c in zip(E,rhs)]);ZZ=nullbasis(J);CC=[[sum(z[k]*CB[k][i] for k in range(12)) for i in range(20)] for z in ZZ]
    try:
        ca.solve_range(E,[[sum(a*c for a,c in zip(row,C)) for C in CC] for row in rhs]);ok=True
    except ca.RangeObstruction:ok=False
    return {'pairs':pairs,'algebraically_liftable_cubic_dimension':20-(aug-rk),'necessary_completed_cost_kernel_dimension':len(CC),'all_necessary_cubics_have_lift':ok}
start=time.perf_counter();cases=[ [((1,2),(1,1))], [((1,0),(1,1))], [((1,2),(1,0))], [((1,2),(1,1)),((3,1),(1,2))], [((1,0),(1,0)),((1,2),(1,1))], [((1,2),(1,0)),((3,1),(0,1))], [((1,0),(1,0)),((1,1),(0,1))], [((1,0),(1,0)),((1,0),(0,1))], [((1,0),(1,0)),((0,1),(1,0))] ]
rows=[]
for case in cases:
    row=test(case);rows.append(row);print(json.dumps(row),flush=True)
(root/'work/general_degenerate_lift.json').write_text(json.dumps({'cases':rows,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
