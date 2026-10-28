#!/usr/bin/env python3
"""Independent exact code/coset, full-ancilla and noncommuting-control fixtures."""
import itertools,json
from pathlib import Path
import sympy as s

I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
def kron(*xs):
    out=s.ones(1,1)
    for a in xs:out=s.kronecker_product(out,a)
    return out
def clean(A):return A.applyfunc(s.expand)
def codebook(n,cols,reps):
    k=len(cols);d=1<<n
    def cw(l):
        v=0
        for i,c in enumerate(cols):
            if l&(1<<i):v^=c
        return v
    dec={}
    for l,g in itertools.product(range(1<<k),range(len(reps))):
        x=cw(l)^reps[g];assert x not in dec;dec[x]=(l,g)
    assert len(dec)==d and reps[0]==0
    return cw,dec
cases=[('nonlinear_3_1',3,[7],[0,4,2,1]),
       ('nonlinear_4_2',4,[12,3],[0,8,2,6])]
augmented_basis_checks=0;moment_entries=0;records=[]
for name,n,cols,reps in cases:
    k=len(cols);d=1<<n;cw,dec=codebook(n,cols,reps)
    nonlinear=any(dec[x^y][0]!=(dec[x][0]^dec[y][0]) for x,y in itertools.product(range(d),repeat=2))
    assert nonlinear
    for x,a in itertools.product(range(d),repeat=2):
        l,g=dec[x^a]
        assert cw(l)^reps[g]^a==x
        for i,c in enumerate(cols):
            lp,gp=dec[(x^c)^a]
            assert lp==l^(1<<i) and gp==g
            for j in range(k):
                zi=(-1)**((l>>j)&1);zip=(-1)**((lp>>j)&1)
                assert zip==zi*(-1 if i==j else 1)
            augmented_basis_checks+=1
        # All diagonal Z phases commute on every coordinate-ancilla basis state;
        # logical X translations commute and their full relations hold above.
    enc=s.zeros(d,1<<k)
    for l in range(1<<k):enc[cw(l),l]=1
    translations=[]
    for f in range(d):
        T=s.zeros(d)
        for x in range(d):T[x^f,x]=1
        translations.append(T)
    coords=[s.diag(*[(-1 if x&(1<<(n-1-j)) else 1) for x in range(d)]) for j in range(n)]
    P=kron(*([X,Z]+[I]*(n-2)))
    V=(3*s.eye(d)-4*s.I*P)/5
    assert clean(V.H*V)==s.eye(d)
    # Direct physical preparation-label averages, before using any code formula.
    means=[s.zeros(d) for _ in range(n+k)]
    unsigned=[]
    rho0=s.zeros(d)
    for l,g in itertools.product(range(1<<k),range(len(reps))):
        x=cw(l)^reps[g];E=s.zeros(d);E[x,x]=1
        rho0+=E/d
        for j in range(n):means[j]+=(-1 if x&(1<<(n-1-j)) else 1)*E/d
    unsigned.append(rho0)
    for i,c in enumerate(cols):
        avg=s.zeros(d);signed=s.zeros(d)
        for l in range(1<<k):
            if l&(1<<i):continue
            for sign,g in itertools.product([-1,1],range(len(reps))):
                x=cw(l)^reps[g];y=x^c
                E=s.zeros(d);E[x,x]=E[y,y]=s.Rational(1,2);E[x,y]=E[y,x]=sign*s.Rational(1,2)
                avg+=E/d;signed+=sign*E/d
        unsigned.append(avg);means[n+i]=signed
    assert all(A==s.eye(d)/d for A in unsigned)
    assert all(means[j]==coords[j]/d for j in range(n))
    assert all(means[n+i]==translations[c]/d for i,c in enumerate(cols))
    # Correlated physical pattern instrument with coherent retained memory.
    K=[s.diag(1,s.Rational(3,5)),s.Matrix([[0,s.Rational(4,5)],[0,0]])]
    assert sum((A.H*A for A in K),s.zeros(2))==I
    q0=[s.Rational(0)]*d;q0[0]=s.Rational(3,5);q0[cols[0]]=s.Rational(1,5);q0[(d-1)^cols[0]]=s.Rational(1,5)
    # For repetition c_0=all-ones the two positions collide with identity.
    if cols[0]==d-1:
        q0=[s.Rational(0)]*d;q0[0]=s.Rational(3,5);q0[4]=q0[2]=s.Rational(1,5)
    q1=[s.Rational(0)]*d;q1[0]=s.Rational(3,4);q1[d-1]=s.Rational(1,8);q1[1<<(n-1)]=s.Rational(1,8)
    qs=[q0,q1];assert all(sum(q)==1 for q in qs)
    biases=[[sum(((-1 if f&(1<<(n-1-j)) else 1)*q[f] for f in range(d)),s.Rational(0)) for j in range(n)] for q in qs]
    assert min(v for row in biases for v in row)>=0
    for a,b in itertools.product(range(2),repeat=2):
        M=s.zeros(2);M[a,b]=1
        km=[A*M*A.H for A in K];total=sum(km,s.zeros(2))
        fs=[sum((qs[z][f]*km[z] for z in range(2)),s.zeros(2)) for f in range(d)]
        for v,A in enumerate(means):
            actual=sum((kron(clean(V*translations[f]*A*translations[f].H*V.H),fs[f]) for f in range(d)),s.zeros(2*d))
            if v<n:
                hm=sum(((-1 if f&(1<<(n-1-v)) else 1)*fs[f] for f in range(d)),s.zeros(2))
                target=kron(clean(V*coords[v]*V.H)/d,hm)
            else:target=kron(clean(V*translations[cols[v-n]]*V.H)/d,total)
            assert clean(actual)==clean(target);moment_entries+=(2*d)**2
    records.append({'name':name,'n':n,'k':k,'columns':cols,'transversal':reps,'nonlinear_logical_decoder':nonlinear})

# A multi-logical actual receiver with deliberately NONCOMMUTING coordinate fits.
n=3;k=2;d=8;D=d*d;cols=[6,3];reps=[0,1];cw,dec=codebook(n,cols,reps)
coords=[kron(*[Z if i==j else I for i in range(n)]) for j in range(n)]
r=s.Rational(1,10000);co=(1-r*r)/(1+r*r);si=2*r/(1+r*r)
S=[co*coords[0]+si*kron(X,X,I),coords[1],coords[2]]
delta=s.Rational(1,256);assert 2*(1-co)<=delta**2
assert S[0]*S[1]!=S[1]*S[0] and all(A*A==s.eye(d) for A in S)
XA=[]
for j in range(n):
    flip=1<<(n-1-j);A=s.zeros(d)
    for a in range(d):A[a^flip,a]=1
    XA.append(A)
W=s.eye(D);Ws=s.eye(D)
for j in range(n):
    Q=kron((s.eye(d)+S[j])/2,s.eye(d))+kron((s.eye(d)-S[j])/2,XA[j])
    Qs=kron((s.eye(d)+coords[j])/2,s.eye(d))+kron((s.eye(d)-coords[j])/2,XA[j])
    assert Q*Q==s.eye(D)
    W=Q*W;Ws=Qs*Ws
assert W.H*W==s.eye(D)
Zhat=[];Ztrue=[];Xtrue=[]
for i,c in enumerate(cols):
    Pi=s.diag(*[(-1 if dec[a][0]&(1<<i) else 1) for a in range(d)])
    Zhat.append(W.H*kron(s.eye(d),Pi)*W)
    Ztrue.append(Ws.H*kron(s.eye(d),Pi)*Ws)
    Tx=s.zeros(d)
    for x in range(d):Tx[x^c,x]=1
    Xtrue.append(kron(Tx,s.eye(d)))
assert all(A*A==s.eye(D) for A in Zhat)
assert Zhat[0]*Zhat[1]==Zhat[1]*Zhat[0]
Ut=s.zeros(D)
gdim=(1<<(n-k))*d
for l,g,a in itertools.product(range(1<<k),range(len(reps)),range(d)):
    Ut[(cw(l)^reps[g]^a)*d+a,l*gdim+g*d+a]=1
assert Ut.H*Ut==s.eye(D)
for i in range(k):
    zi=s.diag(*[(-1 if l&(1<<i) else 1) for l in range(1<<k)])
    xi=s.zeros(1<<k)
    for l in range(1<<k):xi[l^(1<<i),l]=1
    assert Ut*kron(zi,s.eye(gdim))*Ut.H==Ztrue[i]
    assert Ut*kron(xi,s.eye(gdim))*Ut.H==Xtrue[i]

# Keep every P,A and receiver wire through the entire 3k-gate network.
Rdim=1<<k
def network(zlist):
    net=s.SparseMatrix.eye(D*Rdim)
    for i in range(k):
        xr=s.zeros(Rdim);p0=s.zeros(Rdim);p1=s.zeros(Rdim)
        for v in range(Rdim):
            xr[v^(1<<i),v]=1
            (p1 if v&(1<<i) else p0)[v,v]=1
        cz=s.SparseMatrix(kron((s.eye(D)+zlist[i])/2,s.eye(Rdim))+kron((s.eye(D)-zlist[i])/2,xr))
        cx=s.SparseMatrix(kron(s.eye(D),p0)+kron(Xtrue[i],p1))
        net=cz*cx*cz*net
    return net
net=network(Zhat);ideal=network(Ztrue)
swap=s.zeros(D*Rdim)
for l,g,r0 in itertools.product(range(Rdim),range(gdim),range(Rdim)):
    swap[(r0*gdim+g)*Rdim+l,(l*gdim+g)*Rdim+r0]=1
assert ideal==kron(Ut,s.eye(Rdim))*swap*kron(Ut.H,s.eye(Rdim))
eta=k*(4*n+1)*delta
diff=net-ideal;frob2=sum(s.re(v)**2+s.im(v)**2 for v in diff.values())
assert frob2<=eta**2
bell_results=[]
for ancillas in [(0,0),(0,5)]:
    # Gauge is coherently entangled with a retained two-state memory; receiver
    # mixed states are purified by the untouched r0 register. Initial amplitudes
    # have common normalization 1/sqrt(2*Rdim^2).
    amps={}
    for l,r0,h in itertools.product(range(Rdim),range(Rdim),range(2)):
        a=ancillas[h];g=h;pa=(cw(l)^reps[g]^a)*d+a;col=pa*Rdim+r0
        phase=1 if h==0 else s.I
        for row in range(D*Rdim):
            v=net[row,col]
            if v:amps[row//Rdim,row%Rdim,l,h,r0]=phase*v
    norm=sum(s.re(v)**2+s.im(v)**2 for v in amps.values())
    normalization=2*Rdim**2;assert norm==normalization
    good=s.Rational(0)
    for pa,h,r0 in itertools.product(range(D),range(2),range(Rdim)):
        v=sum((amps.get((pa,l,l,h,r0),0) for l in range(Rdim)),s.Rational(0))
        good+=s.re(v)**2+s.im(v)**2
    loss=1-good/(Rdim*normalization)
    assert 0<=loss<=eta**2
    bell_results.append({'coordinate_ancilla_branches':list(ancillas),'complete_reference_Bell_loss':str(loss)})

budget_cases=0
for n,k in [(1,1),(3,1),(3,2),(4,2)]:
    d=1<<n;m=k+1
    for delta in [s.Rational(1,64),s.Rational(1,256)]:
        for gamma in [s.Rational(1,d),s.Rational(1,10*d)]:
            a=s.Rational(1,16*d);stage=0
            while a>delta*gamma/5:a/=2;stage+=1
            assert a>delta*gamma/10
            N=8*m*3**n/a**2
            assert N<800*m*3**n/(delta**2*gamma**2)
            assert 2*(m*3**n+2*m*d*a/3)<=3*m*3**n
            e=s.Rational(5,4)*a;h=gamma-e
            assert h>e and 2*e<=delta*(2*h-e)
            budget_cases+=1
out={'status':'PASS_NONLINEAR_COSET_FULL_ANCILLA_LIFT_NONCOMMUTING_MULTI_LOGICAL_RECEIVER',
     'source_outcomes':0,'rng_draws':0,'nonlinear_code_fixtures':records,
     'full_augmented_basis_Pauli_cases':augmented_basis_checks,
     'complete_memory_preparation_moment_entries':moment_entries,
     'noncommuting_coordinate_fits':True,'learned_Z_reflections_commute_exactly':True,
     'augmented_physical_dimension':D,'multi_logical_unitary_dimension':D*Rdim,
     'full_retained_ancilla_unitary_Frobenius_error_squared':str(frob2),
     'advertised_unitary_error_bound_squared':str(eta**2),
     'complete_reference_fixtures':bell_results,'finite_budget_guard_cases':budget_cases,
     'sampled_acquisition_or_general_compiler_executed':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
