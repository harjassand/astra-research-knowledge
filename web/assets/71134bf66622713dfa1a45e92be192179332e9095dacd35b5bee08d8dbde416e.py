"""Independent Frechet/tensor SU(d) audit; no peer script imports."""
import json
import time
from pathlib import Path
import sympy as s

start=time.perf_counter()
checks={}
def zero(M): return all(s.simplify(x)==0 for x in M)
def basis(d):
    result=[]
    for i in range(d):
        for j in range(i+1,d):
            E=s.zeros(d);E[i,j]=1;E[j,i]=1;result.append(E/s.sqrt(2))
            E=s.zeros(d);E[i,j]=-s.I;E[j,i]=s.I;result.append(E/s.sqrt(2))
    for k in range(1,d):
        E=s.zeros(d)
        for i in range(k):E[i,i]=1
        E[k,k]=-k
        result.append(E/s.sqrt(k*(k+1)))
    return result
def kron(xs):
    value=s.Matrix([[1]])
    for x in xs:value=s.kronecker_product(value,x)
    return value
def dkernel(rho,Z,N):
    return sum((kron([Z if j==i else rho for j in range(N)]) for i in range(N)),s.zeros(rho.rows**N))
def d2kernel(rho,Z,W,N):
    return sum((kron([Z if k==i else W if k==j else rho for k in range(N)])
                for i in range(N) for j in range(N) if i!=j),s.zeros(rho.rows**N))

for d in [2,3]:
    Ts=basis(d);p=len(Ts)
    checks[f'basis_HS1_d{d}']=all(s.simplify(s.trace(Ts[i]*Ts[j])-int(i==j))==0 for i in range(p) for j in range(p))
    checks[f'local_Casimir_d{d}']=zero(sum((T*T for T in Ts),s.zeros(d))-(s.Rational(d*d-1,d))*s.eye(d))
    swap=s.zeros(d*d)
    for i in range(d):
        for j in range(d):swap[j*d+i,i*d+j]=1
    checks[f'completeness_swap_d{d}']=zero(sum((s.kronecker_product(T,T) for T in Ts),s.zeros(d*d))-swap+s.eye(d*d)/d)
    # Strictly positive rational Hermitian density with noncommuting real
    # and imaginary coherences; diagonal dominance gives full rank.
    rho=s.eye(d)/d
    rho[0,0]+=s.Rational(1,20);rho[1,1]-=s.Rational(1,20)
    rho[0,1]=s.Rational(1,50)+s.I/100;rho[1,0]=s.conjugate(rho[0,1])
    rhoinv=rho.inv()
    C=s.eye(p)
    C[0,0]+=s.Rational(1,100);C[0,1]=C[1,0]=s.Rational(1,1000)
    B=s.diag(*[s.Rational(i,d) for i in range(d)])
    B-=s.trace(B)*s.eye(d)/d
    B[0,1]=B[1,0]=s.Rational(1,10)
    t=s.Matrix([s.trace(rho*T) for T in Ts])
    V=[(T*rho+rho*T)/2-t[i]*rho for i,T in enumerate(Ts)]
    R=[-s.I*(T*rho-rho*T) for T in Ts]
    zc=sum((C[i,j]*(Ts[i]*Ts[j]+Ts[j]*Ts[i])/2 for i in range(p) for j in range(p) if C[i,j]),s.zeros(d))
    tc=(t.T*C*t)[0]
    sc=s.trace(rho*zc)
    vb=(B*rho+rho*B)/2-s.trace(rho*B)*rho
    def dv(i,Z):return (Ts[i]*Z+Z*Ts[i])/2-s.trace(Z*Ts[i])*rho-t[i]*Z
    def dr(i,Z):return -s.I*(Ts[i]*Z-Z*Ts[i])
    checks[f'filter_logdet_d{d}']=all(s.simplify(s.trace(rhoinv*V[i])+d*t[i])==0 for i in range(p))
    checks[f'rotation_logdet_d{d}']=all(s.simplify(s.trace(rhoinv*R[i]))==0 for i in range(p))
    # Check the complete principal matrix, including off-diagonal test terms.
    principal=s.Matrix(p,p,lambda i,j:sum(s.trace(Ts[i]*V[a])*s.trace(Ts[j]*V[a])-s.trace(Ts[i]*R[a])*s.trace(Ts[j]*R[a])/4 for a in range(p)))
    expected=s.Matrix(p,p,lambda i,j:s.trace(rho*(Ts[i]-t[i]*s.eye(d))*rho*(Ts[j]-t[j]*s.eye(d))))
    checks[f'isotropic_full_principal_matrix_d{d}']=zero(principal-expected)

    for N in [1,2]:
        dim=d**N
        a=2*sum((C[i,j]*t[i]*V[j] for i in range(p) for j in range(p) if C[i,j]),s.zeros(d))+vb
        a+=sum((C[i,j]*(dv(j,V[i])-dr(j,R[i])/4)/N for i in range(p) for j in range(p) if C[i,j]),s.zeros(d))
        U=(N-1)*tc+sc+N*s.trace(rho*B)
        ker=kron([rho]*N)
        Fs=[sum((kron([T if j==i else s.eye(d) for j in range(N)]) for i in range(N)),s.zeros(dim)) for T in Ts]
        Fb=sum((kron([B if j==i else s.eye(d) for j in range(N)]) for i in range(N)),s.zeros(dim))
        K=sum((C[i,j]*(Fs[i]*Fs[j]+Fs[j]*Fs[i])/(2*N) for i in range(p) for j in range(p) if C[i,j]),s.zeros(dim))+Fb
        differential=U*ker+dkernel(rho,a,N)
        differential+=sum((C[i,j]*(d2kernel(rho,V[i],V[j],N)-d2kernel(rho,R[i],R[j],N)/4)/N for i in range(p) for j in range(p) if C[i,j]),s.zeros(dim))
        checks[f'full_tensor_generator_d{d}_N{N}']=zero(differential-(K*ker+ker*K)/2)
        checks[f'exact_trace_potential_d{d}_N{N}']=s.simplify(U-s.trace(K*ker))==0
        drift=s.trace(rhoinv*a)
        drift+=sum((C[i,j]*(-s.trace(rhoinv*V[i]*rhoinv*V[j])+s.trace(rhoinv*R[i]*rhoinv*R[j])/4)/N for i in range(p) for j in range(p) if C[i,j]),s.S.Zero)
        checks[f'logdet_drift_cancellation_d{d}_N{N}']=s.simplify(drift+d*(2-s.Rational(1,N))*tc+d*sc/N+d*s.trace(rho*B))==0
        qv=2*sum((C[i,j]*(s.trace(rhoinv*V[i])*s.trace(rhoinv*V[j])-s.trace(rhoinv*R[i])*s.trace(rhoinv*R[j])/4)/N for i in range(p) for j in range(p) if C[i,j]),s.S.Zero)
        checks[f'logdet_qv_cancellation_d{d}_N{N}']=s.simplify(qv-2*d*d*tc/N)==0
        checks[f'normalized_trace_for_Jensen_d{d}_N{N}']=s.simplify(s.trace(K)/dim-s.trace(C)/d)==0

# Purely scalar positivity and exponent margins used by the fixed-radius
# theorem: delta<=alpha eta²/10 yields margin alpha eta²/2 at eta,
# and alpha eta²/16 at 3eta/4. eta/2 is NOT a valid neighborhood at this radius.
alpha,eta=s.symbols('alpha eta',positive=True)
radius=alpha*eta**2/10
checks['fixed_domain_margin']=s.simplify(alpha*eta**2-5*radius-alpha*eta**2/2)==0
checks['explicit_3_over4_neighborhood_margin']=s.simplify(alpha*(3*eta/4)**2-5*radius-alpha*eta**2/16)==0
checks['half_neighborhood_not_certified']=s.simplify(alpha*(eta/2)**2-5*radius)==-alpha*eta**2/4
dd,BB,rate=s.symbols('dd BB rate',positive=True)
H0=4*alpha*(dd-1)/dd+BB
L2=8*alpha*dd*(dd-1)*(H0+rate)
checks['fixed_radius_exit_loss_absorption']=s.simplify(H0-L2/(8*alpha*dd*(dd-1))+rate)==0
out={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'num_checks':len(checks),
     'runtime_seconds':time.perf_counter()-start,'sympy_version':s.__version__,
     'scope':'Independent exact full tensor identities at d2,d3 and N1,N2; complete isotropic principal matrix; logdet drift/QV and fixed-radius scalar margins. These fixtures are transcription evidence, not all-N proof, an executed diffusion, normalization sampler or novelty clearance.'}
Path(__file__).with_name('fixed_qudit_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert all(checks.values())
