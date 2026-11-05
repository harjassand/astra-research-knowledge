"""Connected-SET/Mobius compiler diagnostic; floating arithmetic, not certified."""
import itertools,json,math,time
from collections import Counter
from functools import lru_cache
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm
from scipy.sparse import coo_matrix,eye,kron
from scipy.sparse.linalg import LinearOperator,expm_multiply
AXES="IXYZ"
TABLE={("X","Y"):(1j,"Z"),("Y","X"):(-1j,"Z"),("Y","Z"):(1j,"X"),
       ("Z","Y"):(-1j,"X"),("Z","X"):(1j,"Y"),("X","Z"):(-1j,"Y")}
PM={"I":np.eye(2,dtype=complex),"X":np.array([[0,1],[1,0]],complex),
    "Y":np.array([[0,-1j],[1j,0]],complex),"Z":np.diag([1,-1]).astype(complex)}
def support(s):return frozenset(i for i,a in enumerate(s) if a!="I")
def multiply(left,right):
    phase,out=1+0j,[]
    for a,b in zip(left,right):
        if a=="I":out.append(b)
        elif b=="I":out.append(a)
        elif a==b:out.append("I")
        else:
            factor,c=TABLE[a,b];phase*=factor;out.append(c)
    return phase,"".join(out)
def layout(target):
    i=min(support(target));a=target[i];n=len(target)
    b={"X":"Z","Y":"X","Z":"Y"}[a];q={"X":"Y","Y":"Z","Z":"X"}[a]
    return (tuple("I"*j+(q if j==i else target[j])+"I"*(n-j-1)
                  for j in sorted(support(target))),("I"*i+b+"I"*(n-i-1),))
@lru_cache(None)
def basis(n):
    labels=tuple("".join(t) for t in itertools.product(AXES,repeat=n))
    return labels,{s:i for i,s in enumerate(labels)}
def generator(h,n,r,c):
    labels,index=basis(n);rows,cols,vals=[],[],[]
    for j,a in enumerate(labels):
        if support(a):rows.append(j);cols.append(j);vals.append(-r*len(support(a)))
        for p,theta in h.items():
            c["generator_pauli_product_probes"]+=1;phase,out=multiply(p,a)
            if abs(phase.imag)>.5 and theta:
                rows.append(index[out]);cols.append(j);vals.append(float((-2j*phase*theta).real))
    z=coo_matrix((vals,(rows,cols)),shape=(len(labels),len(labels))).tocsr()
    z.eliminate_zeros();return z
def jordan(label,c):
    labels,index=basis(len(label));rows,cols,vals=[],[],[]
    for j,a in enumerate(labels):
        c["jordan_pauli_product_probes"]+=1;phase,out=multiply(label,a)
        if abs(phase.imag)<.5:
            rows.append(index[out]);cols.append(j);vals.append(float(phase.real))
    return coo_matrix((vals,(rows,cols)),shape=(len(labels),len(labels))).tocsr()
def machine(gen,ops,w):
    blocks=1<<len(ops);z=kron(eye(blocks,format="csr"),w*gen,format="csr")
    for j,a in enumerate(ops):
        rows=[s for s in range(blocks) if s&(1<<j)];cols=[s^(1<<j) for s in rows]
        t=coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(blocks,blocks)).tocsr()
        z+=kron(t,a,format="csr")
    z.eliminate_zeros();return z
def action(a,v,c):
    c["sparse_exponential_actions"]+=1;c["sum_augmented_nonzeros"]+=a.nnz
    c["max_augmented_dimension"]=max(c["max_augmented_dimension"],a.shape[0]);at=a.T.tocsr()
    def run(x,adjoint=False):
        rhs=1 if x.ndim==1 else x.shape[1]
        c["sparse_adjoint_rhs" if adjoint else "sparse_forward_rhs"]+=rhs
        c["nonzero_multiply_add_work_proxy"]+=a.nnz*rhs
        return (at if adjoint else a)@x
    op=LinearOperator(a.shape,dtype=float,matvec=lambda x:run(x),matmat=lambda x:run(x),
                      rmatvec=lambda x:run(x,True),rmatmat=lambda x:run(x,True))
    return expm_multiply(op,v,traceA=float(a.diagonal().sum()))
def sparse_response(h,target,r,w,c):
    sites=sorted(set(support(target)).union(*(support(s) for s in h)))
    target="".join(target[i] for i in sites)
    h={"".join(s[i] for i in sites):v for s,v in h.items()};n=len(sites)
    c["max_local_qubits"]=max(c["max_local_qubits"],n);c["local_response_evaluations"]+=1
    if not h:c["analytic_zero_field_evaluations"]+=1;return 0.
    gen=generator(h,n,r,c);size=gen.shape[0];f,b=layout(target)
    mf=machine(gen,[jordan(s,c) for s in f],w);mb=machine(gen,[jordan(s,c) for s in b],w)
    def window(mat,rho):
        v=np.zeros(mat.shape[0]);v[:size]=rho
        return action(mat,v,c)[-size:]
    v=np.zeros(size);v[0]=1.
    return float((window(mb,window(mf,v))[0]-window(mf,window(mb,v))[0])/2)
def rooted_sets(supports,measured,L):
    n=len(supports);adj=[{j for j in range(n) if j!=i and supports[i]&supports[j]} for i in range(n)]
    roots={i for i,s in enumerate(supports) if s&measured}
    sets=[frozenset()];frontier={frozenset()};c=Counter();sizes={"0":1}
    for size in range(1,L+1):
        new=set()
        for s in frontier:
            candidates=set(roots)
            for i in s:candidates.update(adj[i])
            for i in sorted(candidates-s):
                c["attempted_connected_set_additions"]+=1;new.add(s|{i})
        sets.extend(sorted(new,key=lambda s:tuple(sorted(s))));sizes[str(size)]=len(new);frontier=new
    c["unique_root_connected_sets"]=len(sets);return sets,c,sizes
def odd_tail(z,p,L):
    """Positive-term analytic bound; scalar evaluation is floating point."""
    if not 0<=z<1:return None
    if z==0:return {"upper_bound":0.}
    l=L+1
    if l%2==0:l+=1
    first=l;t=math.exp(math.lgamma(p+l)-math.lgamma(p)-math.lgamma(l+1)+l*math.log(z));total=0.
    while True:
        ratio=z*z*(l+p)*(l+p+1)/((l+1)*(l+2));upper=max(z*z,ratio)
        if upper<1:return {"upper_bound":total+t/(1-upper),"first_omitted_odd_order":first,
                           "final_geometric_ratio_upper":upper}
        total+=t;t*=ratio;l+=2
def budgets(h):
    n=len(next(iter(h)));d=[0]*n;j=[0.]*n;k=0
    for p,t in h.items():
        k=max(k,len(support(p)))
        for i in support(p):d[i]+=1;j[i]+=abs(t)
    return {"n":n,"k":k,"d":max(d),"J":max(j),"per_site_incidence":d,"per_site_strength":j}
def connected_set_response(h,target,r,w,L=3):
    """Arbitrary finite real Pauli dictionary; local-support cache per target."""
    if not h or r<=0 or w<=0 or L<0:raise ValueError("Invalid dictionary, rates or cutoff")
    if not support(target) or any(a not in AXES for a in target):raise ValueError("Invalid target")
    for p,t in h.items():
        if len(p)!=len(target) or not support(p) or any(a not in AXES for a in p) or not math.isfinite(t):
            raise ValueError("Invalid Pauli dictionary")
    labels=tuple(sorted(h));sets,c,sizes=rooted_sets([support(s) for s in labels],support(target),L)
    cache={};terms=[]
    for s in sets:
        ids=tuple(sorted(s));parts=[]
        for mask in range(1<<len(ids)):
            sub=tuple(ids[j] for j in range(len(ids)) if mask&(1<<j));c["mobius_subset_requests"]+=1
            if sub not in cache:
                cache[sub]=sparse_response({labels[j]:h[labels[j]] for j in sub},target,r,w,c)
            else:c["response_cache_hits"]+=1
            parts.append((-1 if (len(ids)-len(sub))%2 else 1)*cache[sub])
        terms.append({"set":[labels[j] for j in ids],"contribution":math.fsum(parts)})
    c["unique_subset_responses"]=len(cache);model=budgets(h);b=len(support(target));a=max(1,model["k"]-1)
    bounds={"damping":odd_tail(2*model["J"]/r,b,L),
            "finite_time":odd_tail(4*a*model["J"]*w,b/a,L)}
    valid=[(name,x) for name,x in bounds.items() if x is not None]
    name,bound=min(valid,key=lambda z:z[1]["upper_bound"]) if valid else (None,{"upper_bound":None})
    if L>=len(labels):name,bound="all_subsets",{"upper_bound":0.}
    return {"target":target,"cutoff":L,"compiled_response":math.fsum(t["contribution"] for t in terms),
            "root_connected_sets_by_size":sizes,"operation_counters":dict(c),
            "analytic_truncation_bound":{**bound,"selected":name,"alternatives":bounds,
                "scope":"Analytic inequality evaluated in float; excludes numerical roundoff."},
            "cluster_contributions":terms}

def pauli_matrix(label):
    a=np.array([[1]],complex)
    for p in label:a=np.kron(a,PM[p])
    return a
def dense_reference_response(h,target,r,w):
    """Full untruncated density-matrix regression: independent representation."""
    n=len(target);dim=1<<n;size=dim*dim;ident=np.eye(dim);c=Counter()
    ham=sum((v*pauli_matrix(p) for p,v in h.items()),np.zeros((dim,dim),complex))
    gen=-1j*(np.kron(ident,ham)-np.kron(ham.T,ident))
    for i in range(n):
        for axis in "XYZ":
            p=pauli_matrix("I"*i+axis+"I"*(n-i-1))
            gen+=r/4*(np.kron(p.conj(),p)-np.eye(size))
    def transfer(labels):
        ops=[]
        for label in labels:
            p=pauli_matrix(label);ops.append((np.kron(ident,p)+np.kron(p.T,ident))/2)
        blocks=1<<len(ops);big=np.kron(np.eye(blocks),w*gen)
        for mask in range(blocks):
            for j,op in enumerate(ops):
                if mask&(1<<j):
                    old=mask^(1<<j);big[mask*size:(mask+1)*size,old*size:(old+1)*size]+=op
        c["dense_matrix_exponentials"]+=1
        c["max_dense_exponential_dimension"]=max(c["max_dense_exponential_dimension"],big.shape[0])
        c["sum_dense_dimension_cubes_cost_proxy"]+=big.shape[0]**3
        return expm(big)[-size:,:size]
    f,b=layout(target);fm,bm=transfer(f),transfer(b);rho=(ident/dim).reshape(-1,order="F")
    forward=np.trace((bm@fm@rho).reshape((dim,dim),order="F")).real
    reverse=np.trace((fm@bm@rho).reshape((dim,dim),order="F")).real
    return {"response":float((forward-reverse)/2),"forward":float(forward),"reverse":float(reverse),
            "operation_counters":dict(c),
            "scope":"Dense untruncated floating-point reference, not certified exact arithmetic."}
def main():
    # One three-qubit, five-term, bounded-degree case and one fixed cutoff.
    np.random.seed(20261105)
    h={"XII":.23,"YXI":-.19,"IYI":.17,"ZZI":.21,"IZX":.18}
    r,w,L=4.,.25,3;start=time.perf_counter();rows=[]
    for target in ["ZZI","XII"]:
        row=connected_set_response(h,target,r,w,L)
        ref=dense_reference_response(h,target,r,w)
        error=abs(row["compiled_response"]-ref["response"])
        row.update(dense_full_system_reference=ref,absolute_difference_from_dense=error,
            numerical_difference_below_analytic_bound=error<=row["analytic_truncation_bound"]["upper_bound"])
        rows.append(row)
    result={"status":"Executed connected-set/Mobius compiler structure diagnostic.",
        "arithmetic_scope":"Floating scipy expm_multiply and expm, not certified arithmetic; analytic tail excludes roundoff.",
        "operation_counter_scope":"Sparse RHS counts intercept actual matrix applications. nnz-times-RHS and dense dimension-cubed are work proxies, not complete flop or bit-operation counts.",
        "versions":{"numpy":np.__version__,"scipy":scipy.__version__},
        "seed":20261105,
        "experiment_scope":"No physical, detector, photon-trajectory or sampled-data simulation.",
        "hamiltonian":h,"budgets":budgets(h),"settings":{"r":r,"w":w,"rw":r*w,"cutoff":L},
        "results":rows,"runtime_seconds":time.perf_counter()-start}
    out=Path(__file__).with_name("connected_set_demo.json");out.write_text(json.dumps(result,indent=2)+"\n")
    print(out)
    for row in rows:
        print(json.dumps({"target":row["target"],"compiled":row["compiled_response"],
            "dense":row["dense_full_system_reference"]["response"],"absolute_difference":row["absolute_difference_from_dense"],
            "analytic_truncation_bound":row["analytic_truncation_bound"]["upper_bound"],
            "operation_counters":row["operation_counters"]}))
    print(json.dumps({"runtime_seconds":result["runtime_seconds"]}))
if __name__=="__main__":main()
