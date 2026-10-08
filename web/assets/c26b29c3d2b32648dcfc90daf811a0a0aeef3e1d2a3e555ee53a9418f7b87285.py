"""Literal generic 27x27 block identity and exact equality-channel audit."""
from pathlib import Path
from itertools import permutations
import json,time
import sympy as s
from triaxial_symbolic import symblock,oddblock

OUT=Path(__file__).resolve().parent

def ev(a,b,c):
    v=s.zeros(27,1);v[9*a+3*b+c]=1;return v

def eps(i,j,k):
    i,j,k=int(i),int(j),int(k)
    if len({i,j,k})<3:return 0
    inv=sum(u>v for p,u in enumerate((i,j,k)) for v in (i,j,k)[p+1:])
    return (-1)**inv

def zero(M):return all(s.expand(v)==0 for v in M)

def partial(R,reg):
    M=s.zeros(3)
    for a in range(3):
        for d in range(3):
            for b in range(3):
                for c in range(3):
                    row=[None]*3;col=[None]*3
                    other=[r for r in range(3) if r!=reg]
                    row[reg]=a;col[reg]=d
                    row[other[0]]=col[other[0]]=b;row[other[1]]=col[other[1]]=c
                    M[a,d]+=R[9*row[0]+3*row[1]+row[2],9*col[0]+3*col[1]+col[2]]
    return M

def run():
    started=time.perf_counter()
    w=list(s.symbols('w1 w2 w3'));K=list(s.symbols('K1 K2 K3'))
    J=[s.Matrix(3,3,lambda a,b:-s.I*eps(i,a,b)) for i in range(3)]
    I=s.eye(3)
    W=sum((w[i]*(s.kronecker_product(J[i].T,J[i],I)+s.kronecker_product(J[i].T,I,J[i])) for i in range(3)),s.zeros(27))
    D=s.diag(*[3*K[a]+K[b]+K[c] for a in range(3) for b in range(3) for c in range(3)])-5*W
    cols=[];expected=[];names=[]
    for i in range(3):
        j,k=[x for x in range(3) if x!=i]
        cols.extend([ev(i,i,i),-ev(i,j,j),-ev(i,k,k),(ev(j,i,j)+ev(j,j,i))/s.sqrt(2),(ev(k,i,k)+ev(k,k,i))/s.sqrt(2)])
        expected.append(symblock(w,K,i));names.append(f'parity{i+1}_symmetric')
        cols.extend([(ev(j,i,j)-ev(j,j,i))/s.sqrt(2),(ev(k,i,k)-ev(k,k,i))/s.sqrt(2)])
        expected.append(s.Matrix([[K[i]+4*K[j],-5*w[i]],[-5*w[i],K[i]+4*K[k]]]));names.append(f'parity{i+1}_antisymmetric')
    for sign in [1,-1]:
        cols.extend([(ev(i,(i+1)%3,(i+2)%3)+sign*ev(i,(i+2)%3,(i+1)%3))/s.sqrt(2) for i in range(3)])
        N=oddblock(w,K)
        if sign==1:
            N=s.Matrix(3,3,lambda i,j:N[i,j] if i==j else -N[i,j])
        expected.append(N);names.append('odd_symmetric' if sign==1 else 'odd_antisymmetric')
    U=s.Matrix.hstack(*cols)
    assert zero(U.T*U-s.eye(27))
    assert zero(U.T*D*U-s.diag(*expected))
    # The odd symmetric determinant excess is exact, including the sign.
    assert s.expand(expected[-2].det()-expected[-1].det()-500*w[0]*w[1]*w[2])==0
    permchecks=[]
    for perm in permutations(range(3)):
        P=s.zeros(3)
        for i in range(3):P[perm[i],i]=1
        T=s.kronecker_product(P,P,P)
        inv=[perm.index(i) for i in range(3)]
        substitutions={w[i]:w[inv[i]] for i in range(3)}|{K[i]:K[inv[i]] for i in range(3)}
        assert zero(T*D*T.T-D.subs(substitutions,simultaneous=True))
        permchecks.append(list(perm))
    # Explicit rational isotropic Choi state, PSD as a sum of outer products.
    vs=[]
    for i in range(3):
        j,k=[u for u in range(3) if u!=i]
        v=4*ev(i,i,i)-2*ev(i,j,j)-2*ev(i,k,k)+3*(ev(j,i,j)+ev(j,j,i)+ev(k,i,k)+ev(k,k,i))
        assert (v.T*v)[0]==60
        vs.append(v)
    R=sum((v*v.T/s.Integer(180) for v in vs),s.zeros(27))
    assert s.trace(R)==1
    assert all(zero(partial(R,i)-s.eye(3)/3) for i in range(3))
    BC=s.zeros(27);ABswap=s.zeros(9)
    for a in range(3):
        for b in range(3):
            ABswap[3*b+a,3*a+b]=1
            for c in range(3):BC[9*a+3*c+b,9*a+3*b+c]=1
    assert zero(BC*R*BC.T-R)
    AB=s.Matrix(9,9,lambda u,v:sum(R[9*(u//3)+3*(u%3)+c,9*(v//3)+3*(v%3)+c] for c in range(3)))
    assert zero(ABswap*AB*ABswap.T-AB)
    score=s.trace(R*W.subs({x:1 for x in w}));assert score==3
    # Exact failed reverse allocation along the middle axial regime.
    t=s.symbols('t',real=True)
    Ga=[(2-t)**2,t*t,t*t];La=[2,t*t+1,t*t+1]
    Drev=s.diag(*[La[a]+(Ga[b]+Ga[c])/2 for a in range(3) for b in range(3) for c in range(3)])-W.subs({w[0]:t*t,w[1]:1,w[2]:1})
    rev=s.factor((vs[0].T*Drev*vs[0])[0]/60)
    assert s.expand(rev-(t-1)*(t-s.Rational(19,15)))==0
    a,b,c=s.symbols('a b c',nonnegative=True)
    zA=s.Matrix([b+c-a,a+c-b,a+b-c]);zB=s.Matrix([2*(2*b-a)/3,2*(2*a-b)/3,2*(a+b)/3]);zC=s.Matrix([0,a,a])
    assert zero((zA-zB).subs(c,(a+b)/3))
    assert zero((zB-zC).subs(a,2*b))
    report={'status':'PASS','generic_full_block_identity':True,'orthonormality':True,'block_names':names,'block_dimensions':[M.rows for M in expected],'odd_symmetric_determinant_excess':'500*w1*w2*w3','all_permutation_covariance_checks':permchecks,'support_boundary_agreement':True,'isotropic_exact_broadcaster':{'normalization':'R=sum_i v_i v_i^T/180, with v_i coefficients 4,-2,-2,3,3,3,3','rank':3,'PSD_by_outer_products':True,'trace':str(s.trace(R)),'all_single_marginals':'I3/3','BC_swap':True,'AB_selfadjoint':True,'score_2s':str(score),'V':'2','k':'1','deficit_ratio':'2'},'reverse_allocation_failed_expectation':str(rev),'reverse_allocation_at_5_4':str(rev.subs(t,s.Rational(5,4))),'seconds':time.perf_counter()-started}
    (OUT/'exact_block_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':run()
