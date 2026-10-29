"""Independent exact closed-gap/sign checks; no imports from research producer."""
from pathlib import Path
import hashlib,json
import sympy as s

z=s.symbols('z')
def poly(v): return s.Poly(s.cancel(v),z,domain=s.QQ)
def matrix(a,b,sign=None):
    N=len(b);J=s.diag(*b)
    for i in range(N-1):J[i,i+1]=J[i+1,i]=a[i]
    if sign is not None:J[0,N-1]=J[N-1,0]=sign*a[-1]
    return J
def compute(a,b):
    N=len(a);C=s.prod(a);M=s.eye(2)
    for i in range(N):M=s.Matrix([[(z-b[i])/a[i],-a[i-1]/a[i]],[1,0]])*M
    p=poly(C*s.trace(M));Y=poly(C*(M[0,0]-M[1,1]));G=poly(C*M[1,0]/a[-1]);F=p*p-poly(4*C*C)
    assert poly(matrix(a,b,1).charpoly(z).as_expr())==p-poly(2*C)
    assert poly(matrix(a,b,-1).charpoly(z).as_expr())==p+poly(2*C)
    assert poly(matrix(a[:-2],b[:-1]).charpoly(z).as_expr())==G
    K=s.gcd(F,F.diff()).monic();Fred=F.exquo(K*K);rad=F.exquo(K)
    assert s.gcd(Fred,Fred.diff()).degree()==0 and s.gcd(K,Fred).degree()==0
    assert s.gcd(rad,rad.diff()).degree()==0 and s.gcd(G,G.diff()).degree()==0
    assert all(m<=2 for _,m in F.sqf_list()[1]);assert len(F.intervals())==rad.degree()
    Ga=G.exquo(K);Yr=Y.exquo(K)
    Kplus=s.gcd(K,p-poly(2*C)).monic();Kminus=s.gcd(K,p+poly(2*C)).monic()
    assert Kplus*Kminus==K
    # Matrix equality M=±I modulo each closed-root factor.
    for factor,sign in [(Kplus,1),(Kminus,-1)]:
        for i in range(2):
            for j in range(2): assert poly(M[i,j]-(sign if i==j else 0)).rem(factor).is_zero
    # Differentiate the finite characteristic determinant with its actual Toda
    # vector field, not with the asserted Dubrovin equations.
    adot=[a[i]*(b[(i+1)%N]-b[i]) for i in range(N)]
    bdot=[2*(a[i]**2-a[i-1]**2) for i in range(N)]
    t=s.symbols('t');Jt=matrix([a[i]+t*adot[i] for i in range(N-2)],
                             [b[i]+t*bdot[i] for i in range(N-1)])
    Gdot=poly(s.diff(Jt.charpoly(z).as_expr(),t).subs(t,0))
    assert (Gdot-2*Y).rem(G).is_zero
    Gadot=Gdot.exquo(K);assert (Gadot-2*Yr).rem(Ga).is_zero
    # Lagrange/Abel identity computed exactly as leading coefficient of the
    # remainder, rather than approximate algebraic roots.
    g=Ga.degree();abel=[-2*poly(z**j).rem(Ga).nth(g-1) for j in range(g)]
    assert abel==([0]*(g-1)+[-2] if g else [])
    # Decoder sum equals the lambda^(N-2) coefficient of the inverse of kappa
    # modulo G, by polynomial Lagrange interpolation.
    kappa=poly(M[0,0]);kappainv=s.invert(kappa,G)
    recovered_aNsq=-C*kappainv.nth(N-2)
    assert recovered_aNsq==a[-1]**2
    # Full-G finite Stieltjes decoder, evaluated using exact polynomial
    # residues/moments; closed Dirichlet nodes are NOT discarded here.
    moments=[-C/recovered_aNsq*(poly(z**j)*kappainv).rem(G).nth(N-2)
             for j in range(2*(N-1))]
    assert moments[0]==1
    def inner(u,v):
        uv=poly(u*v)
        return sum(uv.nth(j)*moments[j] for j in range(uv.degree()+1))
    previous=s.Integer(0);current=s.Integer(1);h=s.Integer(1);hprevious=s.Integer(1)
    diagonal=[];offsq=[]
    for j in range(N-1):
        bj=s.cancel(inner(z*current,current)/h);diagonal.append(bj)
        nxt=s.expand((z-bj)*current-(h/hprevious)*previous)
        if j<N-2:
            hnext=s.cancel(inner(nxt,nxt));assert hnext>0
            offsq.append(s.cancel(hnext/h));previous,current=current,nxt;hprevious,h=h,hnext
        else:assert poly(nxt)==G
    diagonal.append(-p.nth(N-1)-sum(diagonal))
    offsq.append(C*C/(recovered_aNsq*s.prod(offsq)));offsq.append(recovered_aNsq)
    assert diagonal==b and offsq==[ai**2 for ai in a]
    return {'N':N,'C':str(C),'p':str(p.as_expr()),'F_factorization':str(s.factor(F.as_expr())),
      'closed_factor_K':str(K.as_expr()),'reduced_F':str(s.factor(Fred.as_expr())),
      'full_G':str(s.factor(G.as_expr())),'active_G':str(Ga.as_expr()),
      'Kplus':str(Kplus.as_expr()),'Kminus':str(Kminus.as_expr()),
      'Y_reduced_mod_active_G':str(Yr.rem(Ga).as_expr()),
      'Gdot_div_K':str(Gadot.as_expr()),'reduced_Abel_velocity':list(map(str,abel)),
      'recovered_aN_squared':str(recovered_aNsq),
      'full_state_Stieltjes_decoder_exact':True,'all_exact_checks_passed':True}

def main():
    cases={'subperiod2_N4':([1,2,1,2],[0,1,0,1]),
           'subperiod3_N6':([1,2,3,1,2,3],[0,1,-1,0,1,-1]),
           'all_closed_N4':([1,1,1,1],[0,0,0,0]),
           'generic_N3':([1,2,3],[0,1,-1])}
    result={name:compute(list(map(s.Rational,a)),list(map(s.Rational,b))) for name,(a,b) in cases.items()}
    # Independent nonclosed generic symbolic sign test in dimension three.
    a=s.symbols('a0:3',nonzero=True);b=s.symbols('b0:3');C=s.prod(a);M=s.eye(2)
    for i in range(3):M=s.Matrix([[(z-b[i])/a[i],-a[i-1]/a[i]],[1,0]])*M
    G=s.expand(C*M[1,0]/a[-1]);Y=s.cancel(C*(M[0,0]-M[1,1]))
    Gdot=sum(s.diff(G,a[i])*a[i]*(b[(i+1)%3]-b[i])+s.diff(G,b[i])*2*(a[i]**2-a[i-1]**2) for i in range(3))
    rem=s.rem(s.cancel(Gdot-2*Y),G,z);assert s.simplify(rem)==0
    result['symbolic_N3_Dubrovin_sign_identity']=True
    proof=Path(__file__).resolve().parents[1]/'PERIODIC_TODA_CONDITIONING_BRIDGE.md'
    result['proof_sha256_at_review']=hashlib.sha256(proof.read_bytes()).hexdigest()
    out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
