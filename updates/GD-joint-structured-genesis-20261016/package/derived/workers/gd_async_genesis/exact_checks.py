"""Own exact finite checks. SymPy is preinstalled; no acquired code is used.

These verify concrete algebra and a concrete absorbing-history lift.
The universal assertions are proved in PROOFS.md, not by this script.
"""
import json,platform,time
from pathlib import Path
import sympy as S

ROOT=Path(__file__).resolve().parent
I4=S.eye(4);I16=S.eye(16)
ZA=S.diag(1,1,-1,-1);ZB=S.diag(1,-1,1,-1)
CA=(I4+ZA)/2;CB=(I4+ZB)/2
P0=S.diag(1,0);I2=S.eye(2);X=S.Matrix([[0,1],[1,0]])
PIA=S.kronecker_product(I4,P0,I2);PIB=S.kronecker_product(I4,I2,P0)
ZAP=2*S.kronecker_product(CA,P0,I2)-I16
ZBP=2*S.kronecker_product(CB,I2,P0)-I16
COPYA=S.kronecker_product(CA,I2,I2)+S.kronecker_product(I4-CA,X,I2)
COPYB=S.kronecker_product(CB,I2,I2)+S.kronecker_product(I4-CB,I2,X)

SINE=S.Rational(5,13);COSINE=S.Rational(12,13)
COORDS=[0,1,0,1,0,1]
WEIGHTS=[(1,1),(1,-1),(1,0),(1,1),(1,-1),(0,1)]

def matrices(coord,weights):
    pairs=[(0,2),(1,3)] if coord==0 else [(0,1),(2,3)]
    u=S.eye(4);g=S.zeros(4)
    for w,(a,b) in zip(weights,pairs):
        if w:
            u[a,a]=u[b,b]=COSINE
            u[a,b]=u[b,a]=-S.I*SINE*w
            g[a,b]=g[b,a]=w
    return u,g

def zero(m):return all(x==0 for x in m)
def pinch(rho,z):return (rho+z*rho*z)/2
def trace_event(rho,diagonal):
    return S.simplify(sum(rho[n,n]*diagonal[n] for n in range(rho.rows)))

def main():
    started=time.monotonic(); checks={}
    checks['commuting_new_involutions']=zero(ZAP*ZBP-ZBP*ZAP) and ZAP**2==I16 and ZBP**2==I16
    checks['copies_preserve_all_new_parities']=all(z*u==u*z for z in [ZAP,ZBP] for u in [COPYA,COPYB])
    checks['copy_unitaries']=COPYA.H*COPYA==I16 and COPYB.H*COPYB==I16
    us=[];gs=[]
    for coord,weights in zip(COORDS,WEIGHTS):
        u,g=matrices(coord,weights);us.append(u);gs.append(g)
        pi=PIA if coord==0 else PIB;zi=ZAP if coord==0 else ZBP;zj=ZBP if coord==0 else ZAP
        gg=S.kronecker_product(g,I2,I2);v=pi*gg;h0=(I16-pi)*gg
        assert zero(zi*v+v*zi)
        assert zero(zj*v-v*zj)
        assert zero(zi*h0-h0*zi) and zero(zj*h0-h0*zj)
        assert h0+v==gg
        assert u.H*u==I4
        # G^2 is a projection: its spectrum is contained in {-1,0,1}.
        assert g*g*g*g==g*g
    checks['six_all_input_Hamiltonian_decompositions']=True
    checks['six_original_gate_norm_certificates']=True

    # Original record instrument, with actual internal wrong labels a,b.
    rho0=S.zeros(4);rho0[0,0]=1
    branches=[(rho0,0,0)]
    for k,u in enumerate(us):
        branches=[(u*r*u.H,a,b) for r,a,b in branches]
        if k in [1,3]:
            c=CA if k==1 else CB;new=[]
            for r,a,b in branches:
                for label,p in [(0,c),(1,I4-c)]:
                    new.append((p*r*p,label if k==1 else a,label if k==3 else b))
            branches=new
    bitsA=[0,0,1,1];bitsB=[0,1,0,1]
    original_ever=S.Integer(0);original_terminal=S.Integer(0)
    for r,a,b in branches:
        event=[int((a or aa) and (b or bb)) for aa,bb in zip(bitsA,bitsB)]
        original_ever+=trace_event(r,event)
        original_terminal+=r[3,3]
    original_ever=S.simplify(original_ever);original_terminal=S.simplify(original_terminal)

    # Lifted physical dynamics; at each own node copy then pinch new parity.
    lifted=S.zeros(16);lifted[0,0]=1
    for k,u in enumerate(us):
        ul=S.kronecker_product(u,I2,I2);lifted=ul*lifted*ul.H
        if k in [1,3]:
            copy,z=(COPYA,ZAP) if k==1 else (COPYB,ZBP)
            lifted=pinch(copy*lifted*copy.H,z)
    event=[int(ZAP[n,n]==-1 and ZBP[n,n]==-1) for n in range(16)]
    lift_terminal=trace_event(lifted,event)
    checks['exact_lift_endpoint_equals_original_record_OR']=(lift_terminal==original_ever)
    assert all(checks.values())

    # Exact symbolic norm identity of the independent entire obstruction.
    u,r=S.symbols('u r',real=True)
    norm_poly=(1-(1+u)*r)**2+(1-u*u)*r+(1+u)**2*r*(1-r)
    checks['abstract_norm_polynomial_is_one']=S.expand(norm_poly)==1
    obstruct=S.Rational(81,250)+S.Rational(729,2500)
    target=1-S.Rational(4,5)**4
    checks['abstract_exact_terminal_odd_excess_positive']=(obstruct-target==S.Rational(63,2500))
    assert all(checks.values())

    out={"scope":"exact SymPy matrix identities in dimension 16 and a polynomial identity; not a universal numerical proof",
         "checks":checks,
         "original_ever_probability":str(original_ever),"original_terminal_probability":str(original_terminal),
         "lifted_terminal_probability":str(lift_terminal),
         "original_ever_decimal":float(original_ever),"original_terminal_decimal":float(original_terminal),
         "abstract_bad_probability":str(obstruct),"abstract_Q":str(target),"abstract_excess":str(obstruct-target),
         "python":platform.python_version(),"sympy":S.__version__,"elapsed_seconds":time.monotonic()-started}
    (ROOT/'exact_checks_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
