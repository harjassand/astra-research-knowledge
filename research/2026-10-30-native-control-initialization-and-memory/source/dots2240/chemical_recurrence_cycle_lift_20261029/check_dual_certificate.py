"""Exact worked dual certificate for the finite-gate network, not proof by numerics."""
import sympy as s
import json
r=s.Symbol('r'); eps=s.Rational(1,10)
# beta_C=-1,beta_B=0; edge (source mode,target mode,delta,shifted rate)
edges=[(0,0,1,eps),(0,1,1,r+1),(1,1,-1,eps*r),(1,0,-1,s.Integer(1))]
G=s.zeros(2)
for j,k,d,rate in edges:
    G[j,k]+=rate*(s.Integer(8)**d if d>0 else s.Integer(2)**d)
    G[j,j]-=rate
v=(-G.T).inv()*s.ones(2,1)
v=[s.factor(z) for z in v]
adj=[s.Integer(0),s.Integer(0)]
for j,k,d,rate in edges:
    adj[k]+=s.Integer(4)**d*v[j].subs(r,r-d)*rate.subs(r,r-d)
    adj[j]-=v[j]*rate
adj=[s.factor(z) for z in adj]
def positivity_threshold(expr,sign):
    num,den=s.fraction(s.cancel(expr)); pn=s.Poly(num,r);pd=s.Poly(den,r)
    assert s.sign(pn.LC()/pd.LC())==sign
    def bound(p):
        return s.Integer(1)+max([abs(z/p.LC()) for z in p.all_coeffs()[1:]]+[s.Integer(0)])
    return max(bound(pn),bound(pd))
R=max([positivity_threshold(z,1) for z in v]+[positivity_threshold(z,-1) for z in adj])
R=int(s.ceiling(R))+2
for n in [R,R+1,2*R,10*R]:
    assert all(z.subs(r,n)>0 for z in v)
    assert all(z.subs(r,n)<0 for z in adj)
out={'epsilon':str(eps),'beta':[-1,0],'tilted_G':str(G),'positive_rational_v':[str(z) for z in v],'exact_unaveraged_adjoint_over_4_minus_r':[str(z) for z in adj],'all_r_above_cauchy_certificate':R,'scope':'Exact rational sign certificate for one worked family; global finite-phase theorem requires its structural proof.'}
print(json.dumps(out,indent=2))
