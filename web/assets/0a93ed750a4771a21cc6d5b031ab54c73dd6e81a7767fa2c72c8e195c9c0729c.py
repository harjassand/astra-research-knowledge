"""Exact finite transcription checks for the phase-2 higher-spin mixture.

No SDE sampling, no asymptotic theorem or separability certified by fixtures.
"""
from pathlib import Path
from math import comb
import json
import sympy as sp
from collections import Counter
import higher_spin_mixture_coefficients as acquired

x,y,z=sp.symbols("x y z",real=True)
coords=(x,y,z)
I2=sp.eye(2)
X=sp.Matrix([[0,1],[1,0]])
Y=sp.Matrix([[0,-sp.I],[sp.I,0]])
Z=sp.diag(1,-1)
tau=(I2+x*X+y*Y+z*Z)/2

def kron_all(factors):
    out=sp.ones(1,1)
    for m in factors:out=sp.kronecker_product(out,m)
    return out

def projector(q):
    return sp.Matrix(1<<q,1<<q,lambda i,j:
        sp.Rational(1,comb(q,int(i).bit_count())) if int(i).bit_count()==int(j).bit_count() else 0)

def exact_zero(matrix):
    return all(sp.cancel(t)==0 for t in matrix)

def collective(q):
    ans=[]
    for pauli in (X,Y,Z):
        m=sp.zeros(1<<q,1<<q)
        for k in range(q):
            factors=[I2]*q
            factors[k]=pauli/2
            m+=kron_all(factors)
        ans.append(m)
    return ans

def evaluate(matrix,point):
    return matrix.subs(dict(zip(coords,point)))

def main():
    radial=x*x+y*y+z*z
    projector_checks=[]
    for q in range(1,5):
        l=projector(q)*kron_all([tau]*q)*projector(q)
        a=sp.expand(sp.trace(l))
        expected=sum(sp.binomial(q+1,2*j+1)*radial**j
                     for j in range(q//2+1))/2**q
        assert sp.expand(a-expected)==0
        assert a.subs({x:0,y:0,z:0})==sp.Rational(q+1,2**q)
        projector_checks.append({"q":q,"a_q":str(expected)})
    C=sp.Matrix([[2,sp.Rational(1,4),0],
                 [sp.Rational(1,4),sp.Rational(3,2),sp.Rational(1,5)],
                 [0,sp.Rational(1,5),sp.Rational(5,4)]])
    # Source's explicit PSD promises, certified by Sylvester here.
    for m in (C-sp.eye(3),3*sp.eye(3)-C):
        assert all(m[:k,:k].det()>0 for k in (1,2,3))
    b=sp.Matrix([sp.Rational(1,7),-sp.Rational(1,11),sp.Rational(1,13)])
    m=sp.Matrix(coords)
    P=sp.eye(3)-m*m.T
    cross=sp.Matrix([[0,-z,y],[z,0,-x],[-y,x,0]])
    D=P*C*P-cross*C*cross.T
    points=[(0,0,0),(sp.Rational(1,50),-sp.Rational(1,100),sp.Rational(1,200)),
            (sp.Rational(1,12),sp.Rational(1,16),-sp.Rational(1,20))]
    generator_checks=[]
    for spins in ((1,),(2,),(1,2),(2,2)):
        s=sp.Integer(acquired.integer_s(len(spins)))
        population=acquired.Population(tuple(sorted(Counter(spins).items())))
        q=sum(spins)
        pi=kron_all([projector(k) for k in spins])
        l=pi*kron_all([tau]*q)*pi
        l=l.applyfunc(sp.expand)
        dl=[l.diff(c) for c in coords]
        ddl=[[dl[i].diff(coords[j]) for j in range(3)] for i in range(3)]
        a=sp.expand(sp.trace(l))
        closed=sp.prod(sum(sp.binomial(k+1,2*j+1)*radial**j
                       for j in range(k//2+1))/2**k for k in spins)
        assert sp.expand(a-closed)==0
        da=[a.diff(c) for c in coords]
        dda=[[da[i].diff(coords[j]) for j in range(3)] for i in range(3)]
        js=collective(q)
        H=sum((C[i,j]*js[i]*js[j] for i in range(3) for j in range(3)),
              sp.zeros(1<<q,1<<q))/s**2
        H+=sum((b[i]*js[i] for i in range(3)),sp.zeros(1<<q,1<<q))/s
        assert exact_zero(H*pi-pi*H)
        u=(m.T*C*m)[0]
        drift=(q-1)*(C*m-u*m)/(2*s**2)+P*b/(2*s)
        V=q*(q-1)*u/(4*s**2)+q*sp.trace(C)/(4*s**2)+q*(b.T*m)[0]/(2*s)
        for point in points:
            ll=evaluate(l,point); aa=evaluate(sp.Matrix([[a]]),point)[0]
            dlv=[evaluate(v,point) for v in dl]
            ddlv=[[evaluate(ddl[i][j],point) for j in range(3)] for i in range(3)]
            dav=sp.Matrix([evaluate(sp.Matrix([[v]]),point)[0] for v in da])
            ddav=sp.Matrix(3,3,lambda i,j:evaluate(sp.Matrix([[dda[i][j]]]),point)[0])
            DD=evaluate(D,point); dd=evaluate(drift,point)
            VV=evaluate(sp.Matrix([[V]]),point)[0]
            # Derivatives of the normalized physical product kernel.
            kk=ll/aa
            dkv=[dlv[i]/aa-ll*dav[i]/aa**2 for i in range(3)]
            ddkv=[[ddlv[i][j]/aa-(dlv[i]*dav[j]+dlv[j]*dav[i]+ll*ddav[i,j])/aa**2
                   +2*ll*dav[i]*dav[j]/aa**3 for j in range(3)] for i in range(3)]
            dphys=dd+DD*dav/(2*s**2*aa)
            vphys=VV+(dd.T*dav)[0]/aa+sum(DD[i,j]*ddav[i,j]
                       for i in range(3) for j in range(3))/(4*s**2*aa)
            output=vphys*kk+sum((dphys[i]*dkv[i] for i in range(3)),sp.zeros(1<<q,1<<q))
            output+=sum((DD[i,j]*ddkv[i][j] for i in range(3) for j in range(3)),
                        sp.zeros(1<<q,1<<q))/(4*s**2)
            target=(H*kk+kk*H)/2
            assert exact_zero(output-target)
            assert sp.cancel(vphys-sp.trace(H*kk))==0
            exact_input=lambda v:acquired.F(int(sp.numer(v)),int(sp.denom(v)))
            compiled=acquired.coefficients(population,
                [[exact_input(C[i,j]) for j in range(3)] for i in range(3)],
                [exact_input(v) for v in b],1,1,[exact_input(v) for v in point])
            assert compiled["potential"]==exact_input(vphys)
            assert compiled["drift"]==[exact_input(v) for v in dphys]
            assert compiled["diffusion_D"]==[[exact_input(DD[i,j]) for j in range(3)] for i in range(3)]
            # Principal minors check the asserted D>=3/4 for these points.
            margin=DD-sp.Rational(3,4)*sp.eye(3)
            assert all(margin[:k,:k].det()>0 for k in (1,2,3))
            generator_checks.append({"spins_q":list(spins),"point":[str(v) for v in point],
                "full_generator_identity":True,"potential_trace_identity":True,
                "diffusion_margin_fixture":True,"acquired_coefficient_program_matches":True})
    r=sp.symbols("r",real=True)
    character_checks=[]
    for q in range(1,9):
        char=sum(sp.exp(r*(sp.Rational(q,2)-j)) for j in range(q+1))/(q+1)
        coeff=sp.log(char).series(r,0,5).removeO().expand()
        assert coeff.coeff(r,2)==sp.Rational(q*(q+2),24)
        assert coeff.coeff(r,4)==-sp.Rational((q+1)**4-1,2880)
        character_checks.append({"q":q,"variance":str(sp.Rational(q*(q+2),12)),
                                  "quartic_log_coefficient":str(coeff.coeff(r,4))})
    # Exact rational lower bounds from the generic entanglement obstruction.
    denom=1+sp.Rational(3,7)+sp.Rational(5,343)
    assert 1/denom-sp.Rational(1,3)==sp.Rational(178,495)
    assert sp.Rational(178,495)-sp.Rational(1,5)==sp.Rational(79,495)
    result={"status":"PASS_EXACT_FINITE_TRANSCRIPTION",
      "projector_normalization":projector_checks,"generator_checks":generator_checks,
      "character_coefficients":character_checks,
      "entanglement_rational_bounds":{"f0":"178/495","concave_f":"79/495"},
      "scope":"Exact small matrices/coefficients only. No SDE path law, asymptotic separability theorem, finite-bit sampler or quantum state preparation executed."}
    Path(__file__).with_name("higher_spin_mixture_checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"matrix_generator_cases":len(generator_checks),
                      "character_cases":len(character_checks),"scope":result["scope"]},indent=2))

if __name__=="__main__":main()
