import sympy as s
import json
R=s.Rational

def channel(etas):
    n=2**len(etas)
    return s.Matrix(n,n,lambda j,k:s.prod(etas[a] if ((j^k)>>a)&1 else 1 for a in range(len(etas))))

def witness(C,z,p,q):
    K=len(z); N=K+2
    L=sum(s.Abs(x) for x in z)
    v=s.zeros(N,1); w=s.zeros(N,1); u=s.eye(N)[:,0]
    if L==0:
        v[1]=1; w[N-1]=1
    else:
        for j,x in enumerate(z):
            v[j+1]=s.sqrt(s.Abs(x)/L)
            w[j+1]=s.sqrt(L*s.Abs(x))*x/s.Abs(x) if x else 0
        w[N-1]=s.sqrt(1-L**2)
    def rot(t,b):
        return s.eye(N)+(s.sqrt(1-t)-1)*(u*u.H+b*b.H)-s.I*s.sqrt(t)*(u*b.H+b*u.H)
    U1=rot(p,v); U2=rot(q,w)
    psi=U1*u; rho=psi*psi.H
    # Put the extra sink into bad sector 1.
    labels=list(range(K+1))+[1]
    after=s.Matrix(N,N,lambda j,k:C[labels[j],labels[k]]*rho[j,k])
    actual=s.simplify(1-(U2*after*U2.H)[0,0])
    c=C[1:,0]; B=C[1:,1:]
    predicted=s.simplify(p+q-p*q+2*s.sqrt(p*q*(1-p)*(1-q))*s.re((c.H*z)[0])-p*q*(z.H*B*z)[0])
    assert s.simplify(actual-predicted)==0
    assert s.simplify((v.H*v)[0]-1)==0 and s.simplify((w.H*w)[0]-1)==0
    return str(actual)

out={}
for name,etas in [('two_nonzero',[R(1,3),R(1,3)]),('same_max_one_zero',[R(1,3),0])]:
    C=channel(etas); B=C[1:,1:]; c=C[1:,0]; z=B.inv()*c
    beta=s.Matrix([(-1)**(j.bit_count()+1)*s.prod(etas[a] for a in range(len(etas)) if (j>>a)&1) for j in range(1,len(c)+1)])
    assert z==beta
    D=s.prod(1-e**2 for e in etas)
    assert s.simplify((c.H*z)[0]-(1-D))==0
    actual=witness(C,z,R(1,2),R(1,2))
    assert s.Rational(actual)==1-D/4
    out[name]={'beta':list(map(str,z)),'l1':str(sum(s.Abs(x) for x in z)),'F':actual,'max_good_bad_coherence':str(max(map(abs,c)))}
d=s.Matrix([1,s.I,1]); C=d*d.H; z=C[1:,0]/2
out['complex_singular_rank_one']={'F':witness(C,z,R(1,4),R(1,4)),'rank_B':C[1:,1:].rank()}
# Arbitrary feasible complex z in a nonsingular correlation matrix.
C=R(1,2)*s.eye(3)+R(1,2)*d*d.H
z=s.Matrix([s.I/5,-R(1,7)])
out['complex_nonoptimizer']={'F':witness(C,z,R(1,4),R(1,3))}
C=channel([R(1,4),R(1,4)]); B=C[1:,1:]; c=C[1:,0]
z=s.Matrix([R(1,2),R(1,2),0]); alpha=R(1,16); h=R(3,16)
g=h*c-alpha*B*z
f=s.simplify(2*h*(c.H*z)[0]-alpha*(z.H*B*z)[0])
upper=s.simplify(alpha*(z.H*B*z)[0]+2*max(map(abs,g)))
assert f==upper==R(31,512)
assert witness(C,z,R(1,4),R(1,4))=='255/512'
out['constrained_boundary_certificate']={'F':'255/512','objective':str(f),'tangent_upper':str(upper),'gradient':list(map(str,g)),'retained_full_pinch_bound':'147/256'}
C=channel([R(1,10),R(1,10)]); z=3*C[1:,1:].inv()*C[1:,0]
actual=witness(C,z,R(1,4),R(1,4)); assert actual=='71791/160000'
out['small_coherence_interior']={'F':actual,'l1':str(sum(map(abs,z)))}
print(json.dumps(out,indent=2))
