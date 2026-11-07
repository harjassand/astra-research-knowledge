"""Data-only modular certificate and a later 64-state nonlinear ring task.

No private component law is imported. The later coupling is an explicit
rational piecewise affine input with a proved block-row Lipschitz bound.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt,lcm
import hashlib
import json
import time
import numpy as np
from exact_core import (GridResidual,matmul,determinant,eye,matpow,matrix_minus,
                        affine_periodic_base,cyclic_green,dyadic_round,mod1,matvec,
                        cat_entropy_interval)

ROOT=Path(__file__).resolve().parent


def principal(nums,Q):
    return (nums+Q//2)%Q-Q//2


def triangle(x):
    x=mod1(x)
    return min(x,1-x)-F(1,4)


def main():
    start=time.perf_counter()
    cfg=json.loads((ROOT/"network_contract.json").read_text())
    N,q,steps,Q=(cfg[k] for k in ("modules","grid_side","loop_steps","output_denominator"))
    B,M2,M3,eta=(F(cfg[k]) for k in ("B","M2","M3","effective_euclidean_error"))
    assert B/q+2*eta<F(1,2) and B/steps+2*eta<F(1,2)
    data=np.load(ROOT/"network_observations.npz")
    grids=data["grids"].astype(np.int64)
    loops=data["loops"].astype(np.int64)
    components=[]
    all_residual=[]
    records=[]
    root2=F(3,2)  # rigorously above sqrt(2)
    C,J=F(9,4),F(21,8)
    for module in range(N):
        grid=grids[module]
        cols=[]
        for j in range(2):
            ys=loops[module,j]
            winding=principal(np.roll(ys,-1,axis=0)-ys,Q).sum(axis=0)
            assert np.all(winding%Q==0)
            cols.append(winding//Q)
            for k in range(steps):
                if k*q%steps==0:
                    idx=[0,0]
                    idx[j]=k*q//steps
                    assert np.array_equal(ys[k],grid[tuple(idx)])
        A=np.stack(cols,axis=1)
        a=A.tolist()
        assert np.array_equal(A,A.T) and determinant(a)==1
        assert matmul(a,a)==[[3*a[i][j]-int(i==j) for j in range(2)] for i in range(2)]
        assert a[0][0]+a[1][1]==3
        b=[F(int(v),Q) for v in grid[0,0]]
        res=np.zeros_like(grid)
        for idx in np.ndindex(q,q):
            if idx==(0,0):
                continue
            j=next(j for j,v in enumerate(idx) if v)
            prev=list(idx)
            prev[j]-=1
            prev=tuple(prev)
            res[idx]=res[prev]+principal(grid[idx]-grid[prev],Q)-A[:,j]*(Q//q)
        square=np.zeros((q,q),dtype=np.int64)
        for j in range(2):
            inc=principal(np.roll(grid,-1,axis=j)-grid,Q)-A[:,j]*(Q//q)
            assert np.array_equal(inc,np.roll(res,-1,axis=j)-res)
            dif=np.roll(res,-1,axis=j)-np.roll(res,1,axis=j)
            assert 4*int(np.abs(dif).max())**2<2**63
            square+=(dif*dif).sum(axis=-1)
        maxsq=int(square.max())
        sq=isqrt(maxsq)
        if sq*sq<maxsq:
            sq+=1
        beta=F(sq*q,2*Q)
        ell=beta+root2*(M3/F(6*q*q)+eta*q)+M2*root2/F(2*q)
        lhat=ell+M2*F(2,q)+2*root2*eta*q
        delta=eta+M2/F(q*q)
        components.append((a,b,GridResidual(res,Q)))
        all_residual.append(res)
        records.append({"module":module,"A":a,"b":[str(z) for z in b],
                        "ell":str(ell),"ell_hat":str(lhat),"delta":str(delta)})
    ell=max(F(x["ell"]) for x in records)
    lhat=max(F(x["ell_hat"]) for x in records)
    delta=max(F(x["delta"]) for x in records)
    nu=F(cfg["known_coupling_block_row_Lipschitz"])
    assert C*(max(ell,lhat)+nu)<1
    assert J*(max(ell,lhat)+nu)<1
    tau=C*(lhat+nu)
    D=C*delta/(1-C*(ell+nu))
    # A later network task: one address of least period 7 in 64 dimensions.
    m=7
    labels=[[i%11,(3*i+1)%13] for i in range(N)]
    bases=[]
    least=1
    for (a,b,res),label in zip(components,labels):
        base,p=affine_periodic_base(a,b,m,label)
        bases.append(base)
        least=lcm(least,p)
    def nonlinear_at(xs):
        out=[]
        for i,(_,_,res) in enumerate(components):
            val=res(xs[i])
            out.append([val[0]+triangle(xs[(i-1)%N][0])/16,
                        val[1]+triangle(xs[(i+1)%N][1])/16])
        return out
    u=[[[F(0),F(0)] for _ in range(m)] for _ in range(N)]
    iterations=0
    peak_num=peak_den=0
    epsilon=F(1,10**12)
    while True:
        rhs=[[] for _ in range(N)]
        for t in range(m):
            xs=[[bases[i][t][j]+u[i][t][j] for j in range(2)] for i in range(N)]
            values=nonlinear_at(xs)
            for i in range(N):
                rhs[i].append(values[i])
        new=[cyclic_green(components[i][0],rhs[i]) for i in range(N)]
        dif=F(0)
        for i in range(N):
            for t in range(m):
                for j in range(2):
                    z=new[i][t][j]
                    dif=max(dif,abs(z-u[i][t][j]))
                    peak_num=max(peak_num,abs(z.numerator).bit_length())
                    peak_den=max(peak_den,z.denominator.bit_length())
        error=root2*dif/(1-tau)
        if error<=epsilon:
            break
        u=[[[dyadic_round(z,60) for z in row] for row in node] for node in new]
        iterations+=1
        assert iterations<1000
    points=[[[mod1(bases[i][t][j]+u[i][t][j]) for j in range(2)] for i in range(N)] for t in range(m)]
    defect=F(0)
    for t,xs in enumerate(points):
        vals=nonlinear_at(xs)
        for i,(a,b,_) in enumerate(components):
            fx=[z+w+v for z,w,v in zip(matvec(a,xs[i]),b,vals[i])]
            nxt=points[(t+1)%m][i]
            for expected,actual in zip(fx,nxt):
                z=actual-expected
                nearest=(z+F(1,2)).numerator//(z+F(1,2)).denominator
                defect=max(defect,abs(z-nearest))
    independent_error=C*root2*defect/(1-tau)
    assert independent_error<F(1,10**10)
    counts={}
    for period in [1,2,3,7,10,31,100]:
        counts[str(period)]=int(np.prod(np.array([
            abs(determinant(matrix_minus(matpow(a,period),eye(2)))) for a,_,_ in components],dtype=object)))
    # This function returns 2 log(lambda), so scale by N/2 for the network.
    elo,ehi=cat_entropy_interval()
    elo,ehi=elo*F(N,2),ehi*F(N,2)
    output={"module_count":N,"state_dimension":2*N,"acquisition_queries":cfg["unique_one_step_queries"],
        "scalar_reports":cfg["returned_scalar_count"],"joint_state_queries":0,
        "component_certificates":records,"norm":"maximum of Euclidean component norms",
        "C":str(C),"J":str(J),"ell_max":str(ell),"ell_hat_max":str(lhat),"delta_max":str(delta),
        "later_coupling_Lipschitz":str(nu),"network_contraction_factor":str(tau),
        "per_component_all_time_error_bound":str(D),"per_component_all_time_error_decimal":float(D),
        "entropy":{"exact":"32 log((3+sqrt(5))/2)","lower":str(elo),"upper":str(ehi),"decimal":float((elo+ehi)/2)},
        "fixed_point_counts":{key:str(value) for key,value in counts.items()},
        "fixed_point_count_bits":{key:value.bit_length() for key,value in counts.items()},
        "compiled_address":{"period":m,"least_period":least,"labels":labels,"iterations":iterations,
            "algorithm_error":str(error),"algorithm_error_decimal":float(error),
            "direct_defect_error":str(independent_error),"direct_defect_error_decimal":float(independent_error),
            "peak_rational_numerator_bits":peak_num,"peak_rational_denominator_bits":peak_den,
            "points_by_time":[[[str(z) for z in x] for x in xs] for xs in points]},
        "wall_seconds":time.perf_counter()-start,
        "observation_sha256":hashlib.sha256((ROOT/"network_observations.npz").read_bytes()).hexdigest(),
        "scope":"32 synthetic separately acquired components. The network is a specified later mathematical coupling; no joint-source experiment or physical implementation is claimed."}
    (ROOT/"NETWORK_CERTIFICATE.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({"modules":N,"dimension":2*N,"queries":cfg["unique_one_step_queries"],
        "joint_queries":0,"D":float(D),"entropy":float((elo+ehi)/2),"period":m,"least_period":least,
        "iterations":iterations,"algorithm_error":float(error),"direct_defect_error":float(independent_error),
        "count_period_31_bits":counts["31"].bit_length(),"seconds":output["wall_seconds"]}))


if __name__=="__main__":
    main()
