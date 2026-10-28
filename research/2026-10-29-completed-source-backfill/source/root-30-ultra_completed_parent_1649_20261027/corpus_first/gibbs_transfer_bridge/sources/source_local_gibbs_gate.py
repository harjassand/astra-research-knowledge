"""Actual reflection-positive spin-two quadratic Gibbs gate and CP norm map.

The construction is local and exact algebraically, not a finite-rank surrogate
for the unknown long-ring transfer. Numerical files are diagnostic only;
closed-form interval inequalities separately certify the non-EB boundary.
"""
import pathlib,json,math
import numpy as np
import sympy as sp
import mpmath as mp
mp.iv.dps=70
ROOT=pathlib.Path(__file__).resolve().parent


def exact_spin2():
    rt=sp.sqrt
    basis=[sp.diag(1,-1,0)/rt(2),sp.diag(1,1,-2)/rt(6)]
    for i,j in [(0,1),(0,2),(1,2)]:
        x=sp.zeros(3);x[i,j]=x[j,i]=1/rt(2);basis.append(x)
    rotations=[sp.Matrix([[0,0,0],[0,0,-1],[0,1,0]]),sp.Matrix([[0,0,1],[0,0,0],[-1,0,0]]),sp.Matrix([[0,-1,0],[1,0,0],[0,0,0]])]
    g=[sp.Matrix(5,5,lambda i,j:sp.simplify(sp.trace(basis[i].T*(l*basis[j]-basis[j]*l))))for l in rotations]
    assert all(x.T==-x for x in g)
    assert sum((x*x for x in g),sp.zeros(5))==-6*sp.eye(5)
    q=[[sp.simplify((g[i]*g[j]+g[j]*g[i])/2+2*(i==j)*sp.eye(5))for j in range(3)]for i in range(3)]
    t=[sum((e[i,j]*q[i][j]for i in range(3)for j in range(3)),sp.zeros(5))for e in basis]
    assert all(sp.trace(x.T*y)==21*(i==j)for i,x in enumerate(t)for j,y in enumerate(t))
    h=-sum((sp.kronecker_product(x,x)for x in g),sp.zeros(25))
    # Exact degree-two identity in delta, checked coefficient by coefficient.
    gg=sum((sp.kronecker_product(x,x)for x in g),sp.zeros(25))
    tt=sum((sp.kronecker_product(x,x)for x in t),sp.zeros(25))
    assert sp.simplify(h*h/2-6*sp.eye(25)-gg/4-tt/2)==sp.zeros(25)
    return g,t,h


def gate(delta,exact=None):
    g,t,h=exact or exact_spin2()
    fs=[sp.eye(5),*g,*t]
    fs=np.array([np.array(x,dtype=float)for x in fs]);h=np.array(h,dtype=float)
    w=np.array([1+6*delta**2]+[delta+delta**2/4]*3+[delta**2/2]*5)
    a=fs*np.sqrt(w)[:,None,None]
    physical=np.eye(25)-delta*h+delta**2*(h@h)/2
    reconstructed=sum(np.kron(x,x)for x in a)
    assert np.max(np.abs(physical-reconstructed))<2e-13
    c=1+6*delta+18*delta**2
    assert np.max(np.abs(sum(x@x.T for x in a)-c*np.eye(5)))<2e-13
    # K_{x,y} local matrix is A_y A_x. Multiplication K K^T gives
    # B_{x,y}=G2(A_x tensor A_y), of order25 with81 Kraus indices.
    b=np.array([physical@np.kron(x,y)for x in a for y in a])
    witness=.5*sum(x[0,1]**2+x[1,0]**2-2*x[0,0]*x[1,1]for x in b)
    return a,b,physical,h,{'delta':delta,'rank_realignment':9,'K_bond_dimension':5,'Q_bond_dimension':25,'local_CP_kraus_count':81,'local_CP_matrix_order':25,'CP_PT_antisymmetric_expectation_numeric':float(witness),'gate_reconstruction_max_error':float(np.max(np.abs(physical-reconstructed))),'c':c}


def finite_kernel(a,time_slices):
    r=len(a);words=list(np.ndindex(*(r,)*time_slices));k=np.zeros((len(words),len(words)))
    for i,x in enumerate(words):
        for j,y in enumerate(words):
            product=np.eye(5)
            for xx,yy in zip(x,y):product=product@a[yy]@a[xx]
            k[i,j]=np.trace(product)
    return k


def apply_pair(vector,gate,i,j,n):
    # Independent physical tensor application, including the closing bond.
    x=np.asarray(vector).reshape((5,)*n);perm=[i,j]+[q for q in range(n)if q not in [i,j]];inv=np.argsort(perm)
    x=np.transpose(x,perm).reshape(25,-1);x=gate@x
    return np.transpose(x.reshape((5,)*n),inv).reshape(-1)


def physical_trace(gate,n,time_slices):
    assert n%2==0
    product=np.eye(5**n)
    for _ in range(time_slices):
        for parity in [0,1]:
            for i in range(parity,n,2):product=np.column_stack([apply_pair(product[:,j],gate,i,(i+1)%n,n)for j in range(5**n)])
    return float(np.trace(product))


def run():
    (ROOT/'data').mkdir(exist_ok=True);ex=exact_spin2();records=[]
    for delta in [.0001,.001,.01,.05]:
        a,b,g,h,row=gate(delta,ex)
        if delta in [.001,.05]:
            for nt in [1,2]:
                k=finite_kernel(a,nt);q=k@k.T
                rotated=float(np.trace(q@q));physical=physical_trace(g,4,nt)
                assert abs(rotated-physical)<1e-9*max(1,abs(physical))
                row[f'rotation_check_N{nt}']={'four_site_physical_trace':physical,'rotated_trace_Q2':rotated,'absolute_difference':abs(rotated-physical)}
        iv=mp.iv;d=iv.mpf(str(delta));c=1+6*d+18*d*d
        # E=Ad_G2 o (Phi tensor Phi). Diamond distance to identity is <=c^4-1.
        # Choi PT tested on a Schmidt-rank2 antisymmetric vector has change
        # <=25/2*(c^4-1); its identity-channel value is -1.
        bound=-1+iv.mpf(25)/2*(c**4-1)
        row['CP_PT_expectation_upper_directed']=math.nextafter(float(bound.b),math.inf)
        row['non_EB_certified']=row['CP_PT_expectation_upper_directed']<0
        records.append(row)
        if delta==.001:
            # Known scalar normalization makes the Kraus family trace-decreasing;
            # no reset or depolarization is added. The scalar mass is retained.
            scaled=b/(row['c']**2)
            row['instrument_scalar_kappa_upper']=row['c']**4
            row['instrument_sum_BdagB_norm_numeric']=float(np.linalg.eigvalsh(sum(x.T@x for x in b))[-1])
            normmap=sum(np.kron(x,x)for x in b)
            ev=np.linalg.eigvals(normmap);rho=float(np.max(ev.real))
            beta=50.;nt=50000
            # Bell-return probability of the trace-decreasing instrument is
            # Tr(E^nt)/(25^2*kappa^nt). Dominant-mode expression is only a
            # numerical asymptotic diagnostic; the all-N identity is exact.
            row['CP_normmap_spectral_radius_numeric']=rho
            row['beta50_log10_Bell_return_dominant_mode_diagnostic']=(nt*(math.log(rho)-4*math.log(row['c']))-2*math.log(25))/math.log(10)
            np.savez(ROOT/'data/actual_cp_instrument_delta001.npz',A=a,B=b,B_trace_decreasing=scaled,G2=g,Hbond=h,scalar_kappa_upper=row['c']**4)
    # The local source compiler is exact in delta. These finite checks only
    # test index/orientation implementation; the all-size proof is separate.
    (ROOT/'data/local_gate.json').write_text(json.dumps({'status':'EXACT_LOCAL_ALGEBRA_PLUS_NUMERICAL_ROTATION_DIAGNOSTICS_AND_DIRECTED_NON_EB_BOUND','records':records},indent=2));print(json.dumps(records,indent=2))


if __name__=='__main__':run()
