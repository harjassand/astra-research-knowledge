"""Independent weighted gap, matching-mixture preparations, and literal seed circuit."""
import numpy as np,json,itertools,math
from scipy.linalg import eigh
from pathlib import Path
rng=np.random.default_rng(991301)
sing=np.array([0,1,-1,0])/np.sqrt(2)
t0=np.array([0,1,1,0])/np.sqrt(2)
omega=(np.kron([1,0,0,0],[0,0,0,1])-np.kron(t0,t0)+np.kron([0,0,0,1],[1,0,0,0]))/np.sqrt(3)
def swap(n,i,j):
    D=2**n; S=np.zeros((D,D))
    for x in range(D):
        y=x^((1<<(n-1-i))|(1<<(n-1-j))) if ((x>>(n-1-i))&1)!=((x>>(n-1-j))&1) else x
        S[y,x]=1
    return S

def matchings(sites):
    if not sites: yield []; return
    i=sites[0]
    for j in sites[1:]:
        for rest in matchings([x for x in sites if x not in (i,j)]): yield [(i,j)]+rest

def product_on_parts(n,parts):
    out=np.ones(2**n)
    for x in range(2**n):
        for sites,vec in parts:
            idx=0
            for s in sites: idx=2*idx+((x>>(n-1-s))&1)
            out[x]*=vec[idx]
    return out

def cptp(D):
    A=rng.normal(size=(3,D,D))+1j*rng.normal(size=(3,D,D))
    w,v=eigh(sum(a.conj().T@a for a in A)); inv=(v/np.sqrt(w))@v.conj().T
    return [a@inv for a in A]

rows=[]
for n in [4,6,8]:
    D=2**n; I=np.eye(D); Ss=[swap(n,i,j) for i in range(n) for j in range(i)]
    J2=sum(Ss)+n*(4-n)/4*I
    w,v=eigh(J2); V=v[:,abs(w)<1e-8]; d0=V.shape[1]; P=V@V.T
    S=swap(n,0,1); pm=(n+2)/(4*(n-1)); pp=1-pm
    minus=[]; plus=[]
    for matching in matchings(list(range(2,n))):
        minus.append(product_on_parts(n,[((0,1),sing)]+[(edge,sing) for edge in matching]))
    for pair in itertools.combinations(range(2,n),2):
        others=[x for x in range(2,n) if x not in pair]
        for matching in matchings(others):
            plus.append(product_on_parts(n,[((0,1,*pair),omega)]+[(edge,sing) for edge in matching]))
    rm=sum(np.outer(x,x) for x in minus)/len(minus)
    rp=sum(np.outer(x,x) for x in plus)/len(plus)
    errm=np.linalg.norm(pm*rm-(I-S)@P/(2*d0)); errp=np.linalg.norm(pp*rp-(I+S)@P/(2*d0))
    assert max(errm,errp)<1e-12
    row={'n':n,'d0':d0,'minus_matching_count':len(minus),'plus_seed_pair_matching_count':len(plus),'weighted_minus_residual':float(errm),'weighted_plus_residual':float(errp)}
    if n<=6:
        # Column vectorization of X in Hom(P,H): R = conjugate(S|P) tensor S.
        Lap=sum(np.eye(D*d0)-np.kron((V.T@s@V).conj(),s) for s in Ss)
        vals=eigh(Lap,eigvals_only=True); gap=min(vals[vals>1e-8]); null=int(sum(abs(vals)<1e-8))
        assert abs(gap-n)<1e-9 and null==1
        row.update(rectangular_gap=float(gap),invariant_dimension=null)
        K=2**int(math.log2(d0)); E=V[:,:K]; Q=E@E.T
        cases=[]
        # Include nonvacuous near-identity CP source and strong arbitrary nonunital source.
        for eta in [1.,.002]:
            A=[np.sqrt(eta)*a for a in cptp(D)]
            if eta<1:A.append(np.sqrt(1-eta)*I)
            ds=[1-sum(np.trace(P@s@a.conj().T@s@a).real for a in A)/d0 for s in Ss]
            comm=sum(np.linalg.norm((s@a-a@s)@V,'fro')**2 for s in Ss for a in A)/d0
            dist=sum(np.linalg.norm((a-(np.trace(V.T@a@V)/d0)*I)@V,'fro')**2 for a in A)/d0
            fe_direct=sum(abs(np.trace(E.T@a@E))**2 for a in A)/K**2
            # TP leakage completion contributes output |0> overlap from leakage of input |0>.
            fe=fe_direct+sum(np.linalg.norm((I-Q)@a@E[:,0])**2 for a in A)/K**2
            bd=d0/K*sum(ds)/n
            outm=sum(a@(pm*rm)@a.conj().T for a in A); outp=sum(a@(pp*rp)@a.conj().T for a in A)
            q=np.trace((I+S)@outm/2+(I-S)@outp/2).real
            target=(1-sum(np.trace(P@S@a.conj().T@S@a).real for a in A)/d0)/2
            assert abs(comm-2*sum(ds))<1e-10 and dist<=sum(ds)/n+1e-10 and 1-fe<=bd+1e-10 and abs(q-target)<1e-12
            cases.append({'eta':eta,'completed_Bell_loss':float(1-fe),'weighted_bound':float(bd),'weighted_poincare_residual':float(dist),'measured_branch_transition':float(q),'target_transition':float(target)})
        row['channels']=cases
    rows.append(row)
# Literal v5 gates, including controlled-on-zero Hadamard, both copying CNOTs.
X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1]); H=np.array([[1,1],[1,-1]])/np.sqrt(2)
c=np.sqrt(2/3);s=np.sqrt(1/3);Ry=np.array([[c,-s],[s,c]])
psi=np.zeros(16);psi[0]=1
psi=np.kron(np.kron(Ry,np.eye(2)),np.eye(4))@psi
CH0=np.block([[H,np.zeros((2,2))],[np.zeros((2,2)),np.eye(2)]])
psi=np.kron(CH0,np.eye(4))@psi
for control,target in [(0,2),(1,3)]:
    out=np.zeros_like(psi)
    for i in range(16): out[i^(1<<(3-target)) if (i>>(3-control))&1 else i]=psi[i]
    psi=out
UA=np.column_stack(([1,0,0,0],-t0,[0,0,0,1],sing));UB=np.kron(X,X)@UA@np.kron(np.eye(2),Z)
psi=np.kron(UA,UB)@psi
assert np.linalg.norm(psi-omega)<1e-12
# Check optional CNOT then odd-plane rotation decomposition of U_A.
C=np.eye(4)[:,[0,1,3,2]]
R=np.column_stack(([1,0,0,0],-t0,sing,[0,0,0,1]))
assert np.linalg.norm(R@C-UA)<1e-12
result={'all_assertions_passed':True,'matching_and_weighted_checks':rows,'literal_seed_circuit_residual':float(np.linalg.norm(psi-omega)),'UA_decomposition_residual':float(np.linalg.norm(R@C-UA))}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
