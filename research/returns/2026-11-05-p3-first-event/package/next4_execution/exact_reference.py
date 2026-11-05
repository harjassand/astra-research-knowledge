"""Independent full-state baseline and exact finite Palm checks.

The acquisition executable does not import this module or receive q_G,
the lifetime, terminal probabilities, or reference trajectories.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,time
import mpmath as mp

def rational_model(bits=100):
    d=F(1,2**bits);a=1-3*d
    pi=[2*a/3,a/3,d,2*d]
    cycle=[2,3,1,0]
    q=[[F(0) for _ in range(4)] for _ in range(4)]
    for x in range(4):
        for y in range(4):
            if y!=x:q[x][y]=pi[y]
        q[x][cycle[x]]+=d/pi[x]
        q[x][x]=-sum(q[x])
    p=[[F(x==y)+q[x][y]/4 for y in range(4)] for x in range(4)]
    rev=[[pi[y]*p[y][x]/pi[x] for y in range(4)] for x in range(4)]
    assert all(sum(row)==1 for row in p)
    assert all(sum(pi[x]*q[x][y] for x in range(4))==0 for y in range(4))
    assert p!=rev
    return pi,q,p,rev

def exhaustive_palm():
    pi,q,p,rev=rational_model(4);mass=pi[2]+pi[3]
    path_count=0;worst=F(0);wrong_tv={}
    L=F(7)
    for n in range(5):
        target=[];wrong=[]
        for x in product(range(4),repeat=n+1):
            prob=pi[x[0]]
            for j in range(n):prob*=p[x[j]][x[j+1]]
            nb=sum(z>=2 for z in x)
            first=(pi[x[0]]/mass if x[0]>=2 else 0)
            for j in range(n):first*=p[x[j]][x[j+1]]
            prop=F(first,1)/(1+L)
            wrong_prop=prop
            for mark in range(1,n+1):
                if x[mark]<2:continue
                term=pi[x[mark]]/mass
                bad=term
                for j in range(mark,0,-1):
                    term*=rev[x[j]][x[j-1]]
                    bad*=p[x[j]][x[j-1]]
                for j in range(mark,n):
                    term*=p[x[j]][x[j+1]]
                    bad*=p[x[j]][x[j+1]]
                # (mixture L/(1+L))*(Poisson ratio n/L)*(mark 1/n)
                prop+=term/(1+L);wrong_prop+=bad/(1+L)
            expected=prob*nb/(mass*(1+L))
            assert prop==expected
            worst=max(worst,abs(prop-expected));path_count+=1
            good=x[0]<2 and any(z>=2 for z in x)
            if good:
                target.append(prob)
                wrong.append(wrong_prop/nb)
        if target:
            z=sum(target);zw=sum(wrong)
            wrong_tv[n]=sum(abs(t/z-w/zw) for t,w in zip(target,wrong))/2
    return {"path_count":path_count,"max_exact_identity_residual":str(worst),
            "wrong_reverse_path_TV_by_fixed_event_count":
                {str(n):float(v) for n,v in wrong_tv.items()}}

def m(v):return mp.mpf(v.numerator)/v.denominator
def main():
    begin=time.perf_counter();mp.mp.dps=180
    pi,q,p,rev=rational_model()
    pv=mp.matrix([[m(v) for v in pi[:2]]])
    qa=mp.matrix([[m(q[i][j]/4) for j in range(2)] for i in range(2)])
    one=mp.matrix([1,1]);ident=mp.eye(2)
    pB=m(pi[2]+pi[3]);zeta=m(pi[2]);g=mp.mpf(1)/4
    def safe_survival(t):return (pv*mp.expm(qa*t)*one)[0]
    def qhit(t):return 1-safe_survival(t)
    L,b,H=65536,320,5
    qL,qH,qb=qhit(L),qhit(H),qhit(b);qG=qL-qH
    muG=qG/(pB*(1+L));eta=mp.exp(-g*b)/zeta
    structure=eta/(1-eta)+(1+eta)/(1-eta)*(qH+qb)/qG+(1+eta)*qb
    init=mp.matrix([[1,0]])
    occupation=init*(-qa)**-1
    mean_norm=(occupation*one)[0]
    joint={}
    for x in range(2):
        for y in range(2,4):
            joint[f"{x}->{y}"]=occupation[x]*m(q[x][y]/4)
    # Occupation during [H,L], restricted to no previous hit, stationary start.
    window_occ=pv*(qa**-1)*(mp.expm(qa*L)-mp.expm(qa*H))
    block_joint={}
    for x in range(2):
        for y in range(2,4):
            block_joint[f"{x}->{y}"]=window_occ[x]*m(q[x][y]/4)/qG
    assert abs(sum(joint.values())-1)<mp.mpf("1e-140")
    assert abs(sum(block_joint.values())-1)<mp.mpf("1e-130")
    # Directionally wrong stationary boundary law, for comparison only.
    jflux=sum(m(pi[x])*m(q[x][y]/4) for x in range(2) for y in range(2,4))
    reversed_wrong={f"{x}->{y}":m(pi[y])*m(q[y][x]/4)/jflux
                    for x in range(2) for y in range(2,4)}
    times=[mp.mpf(a) for a in ["0.01","0.03","0.1","0.3","1","2","3","5"]]
    cdf={str(t):1-(init*mp.expm(qa*t*mean_norm)*one)[0] for t in times}
    eps=mp.mpf("0.1");delta=mp.mpf("0.01")
    b_uniform=mp.ceil(mp.ceil(mp.log(128/(eps*zeta),2))/g)
    L_uniform=mp.ceil(1024*(H+b_uniform+2)/(g*eps))
    xi=eps/128;q0=g/8
    N_uniform=mp.ceil(128/(q0*xi**2)*mp.ceil(mp.log(8/delta,2)))
    def decimal(x):return mp.nstr(x,70)
    data={"model":"four states; exact pi-reset plus invariant directed cycle",
          "rare_bits":100,"p":decimal(pB),"zeta":decimal(zeta),
          "q_L":decimal(qL),"q_H":decimal(qH),"q_buffer":decimal(qb),
          "q_G":decimal(qG),"palm_mean":decimal(muG),
          "multiplicative_mixing_eta":decimal(eta),
          "ideal_structural_TV_bound":decimal(structure),
          "mean_normalized":decimal(mean_norm),"mean_physical":decimal(mean_norm/4),
          "first_entry_joint":{k:decimal(v) for k,v in joint.items()},
          "conditional_block_entry_joint":{k:decimal(v) for k,v in block_joint.items()},
          "wrong_forward_as_reverse_joint":{k:decimal(v) for k,v in reversed_wrong.items()},
          "wrong_direction_joint_TV":decimal(sum(abs(joint[k]-reversed_wrong[k]) for k in joint)/2),
          "cdf_at_mean_multiples":{k:decimal(v) for k,v in cdf.items()},
          "uniform_recipe":{"epsilon":str(eps),"delta":str(delta),
                            "b":int(b_uniform),"L":int(L_uniform),
                            "calibration_proposals":int(N_uniform),
                            "leading_proposal_updates":int(N_uniform*L_uniform)},
          "exact_palm_check":exhaustive_palm(),
          "seconds":time.perf_counter()-begin}
    Path("next4_execution/exact_reference.json").write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps({k:data[k] for k in ["p","q_G","palm_mean","ideal_structural_TV_bound",
                     "mean_physical","wrong_direction_joint_TV","seconds"]},indent=2))
if __name__=="__main__":main()
