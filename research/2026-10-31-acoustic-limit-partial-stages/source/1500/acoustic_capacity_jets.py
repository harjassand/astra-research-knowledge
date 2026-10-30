"""Derive exact acoustic jet charges and test the entire cubic quotient."""
from pathlib import Path
from fractions import Fraction as R
import sys,json,time
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/shared_mode_gluing'));import receive as r,capacity as ca
start=time.perf_counter();F,_,T=r.m.acquired();qc=json.loads((root/'outputs/quadratic_boundary/certificate.json').read_text());hc=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());basis=[list(map(R,row)) for row in qc['normal_form_basis']];powers=qc['cubic_powers'];polys=[{tuple(pw):co for pw,co in zip(powers,row) if co} for row in basis]
HF=[[r.b.diff(r.b.diff(F,i),j) for j in range(4)] for i in range(4)];av=list(map(R,hc['ray']['A0']));a,b,c,d=av;nulls=[av,[-b,a,d,-c]]
x,y=r.b.var(2,0),r.b.var(2,1);zero={};operator=[];records=[]
def rotate_poly(v):return [r.b.add(r.b.scale(x,v[0]),r.b.scale(y,-v[2])),r.b.add(r.b.scale(x,v[1]),r.b.scale(y,-v[3])),r.b.add(r.b.scale(y,v[0]),r.b.scale(x,v[2])),r.b.add(r.b.scale(y,v[1]),r.b.scale(x,v[3]))]
def covderivative(poly,side):
    co=[R(0)]*3
    for pw,val in poly.items():
        if pw[2] or pw[3]:continue
        co[pw[1-side]]+=val
    return co
for side,K in enumerate(nulls):
    Hco=[[[covderivative(p,side)[k] for p in row] for row in HF] for k in range(3)]
    perp=[[R(int(i==j)) for i in range(4)] for j in range(3)]
    D=[[r.quadratic(Hco[0],v,w) for w in perp] for v in perp];bb=[r.quadratic(Hco[1],K,v) for v in perp];aa=r.quadratic(Hco[2],K);Di_b=r.m.linear_solve(D,bb);sigma=aa-r.dot(bb,Di_b);assert sigma>0;r.b.pd(D)
    rootimages=[x,zero,y,zero] if side==0 else [zero,x,zero,y];derivimages=[zero,x,zero,y] if side==0 else [x,zero,y,zero]
    Kimages=rotate_poly(K);perpimages=[rotate_poly(v) for v in perp];coeffs=[]
    for P in polys:
        grad=[r.compose(r.b.diff(P,i),rootimages,2) for i in range(4)]
        gperp=[r.b.add(*(r.b.mul(v[j],grad[j]) for j in range(4))) for v in perpimages]
        gamma={}
        for i in range(4):
            for j in range(4):gamma=r.b.add(gamma,r.b.mul(Kimages[i],r.b.mul(r.compose(r.b.diff(r.b.diff(P,i),j),rootimages,2),derivimages[j])))
        beta=r.b.add(gamma,*(r.b.scale(g,-co) for g,co in zip(gperp,Di_b)))
        assert all(sum(pw)==3 for pw in beta);coeffs.append([beta.get((3-j,j),R(0)) for j in range(4)])
    rows=list(map(list,zip(*coeffs)));operator+=rows
    assert all(not row[j] for row in rows for j in range(4))
    records.append({'side':side,'sigma':str(sigma),'null':list(map(str,K)),'charge_on_normal_basis':[list(map(str,row)) for row in rows]})
M=[row[4:] for row in operator];rank=r.b.rank(M);print('jet rank',rank,'seconds',time.perf_counter()-start,flush=True)
result={'charge_coefficient_powers':[[3-j,j] for j in range(4)],'jet_operator_on_normal_basis':[list(map(str,row)) for row in operator],'quotient_rank':rank,'acoustic_charts':records,'seconds':time.perf_counter()-start,'scope':'Exact derived jet map; rank determines how much of the eight-dimensional quotient is seen at the singular acoustic limits.'}
if rank==8:
    inverse,_=ca.solve_range(M,[[R(int(i==j)) for j in range(8)] for i in range(8)])
    jetbasis=[[sum(inverse[i][j]*basis[i+4][k] for i in range(8)) for k in range(20)] for j in range(8)]
    result['unit_charge_basis']=[list(map(str,row)) for row in jetbasis];result['charge_matrix_inverse']=[list(map(str,row)) for row in inverse]
(root/'work/acoustic_capacity_jets.json').write_text(json.dumps(result,indent=2)+'\n')
