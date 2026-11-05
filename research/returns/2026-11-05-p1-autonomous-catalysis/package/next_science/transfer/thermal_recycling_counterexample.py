"""Exact four-state witness: conditional thermal gates can recycle energy.
All chemistry is a synthetic TWO-STAGE lumped cycle, not an ORR fit.
The baseline pathway comparison changes chemical pathways and therefore
changes the thermal-projected generator. It is not the fixed-Kbar bound.
"""
from pathlib import Path
import json
import mpmath as mp
mp.mp.dps=70
M=mp.mpf
KB=M('8.617333262145e-5');T=M(298);beta=1/(KB*T)
E=M('.126');tau=M('4.1e-8');gamma=1/tau
q=mp.exp(-beta*E);A=beta*4*M('.3');z=mp.exp(-A)
a=M(100);c=M(100);d=c*mp.exp(-beta*M('.192'))
# Index00=0,01=1,10=2,11=3; free energies are0,E,-E,0.
energies=[M(0),E,-E,M(0)]


def solve(coupled, bath_gamma=None):
    gam=gamma if bath_gamma is None else M(bath_gamma)
    Q=mp.matrix(4,4);edges=[]
    def edge(i,j,kf,kr,reward,work,delta_mode,label):
        Q[i,j]+=kf;Q[j,i]+=kr;Q[i,i]-=kf;Q[j,j]-=kr
        db=mp.log(kf/kr)-beta*(work-energies[j]+energies[i])
        assert abs(db)<M('1e-60')
        edges.append((i,j,kf,kr,reward,work,delta_mode,label))
    edge(0,1,gam*q,gam,0,0,E,'bath_empty')
    edge(2,3,gam*q,gam,0,0,E,'bath_adsorbed')
    if coupled is True:
        edge(0,3,a,a,0,0,E,'capture')
        edge(3,0,c,c*z,1,A/beta,-E,'consume_product')
    elif coupled=='matched_off':
        edge(0,2,a,a*q,0,0,0,'ordinary_adsorption')
        edge(3,0,c,c*z,1,A/beta,-E,'consume_product')
    else:
        for i,j in ((0,2),(1,3)):
            edge(i,j,a,a*q,0,0,0,'ordinary_adsorption')
            edge(j,i,d,d*z/q,1,A/beta,0,'ordinary_product')
    B=Q.T.copy();rhs=mp.matrix(4,1)
    for j in range(4):B[3,j]=1
    rhs[3]=1
    pi=mp.lu_solve(B,rhs)
    currents={};entropy=power=mode_balance=M(0);J=M(0)
    for i,j,kf,kr,reward,work,de,label in edges:
        f=pi[i]*kf;r=pi[j]*kr;net=f-r
        currents[label]=currents.get(label,M(0))+net
        J+=reward*net;entropy+=net*mp.log(f/r);power+=net*work
        mode_balance+=net*de
    gr=mp.matrix(4,1)
    for i,j,kf,kr,reward,work,de,label in edges:
        gr[i]+=kf*reward;gr[j]-=kr*reward
    AA=Q.copy()
    for i in range(4):
        for j in range(4):AA[i,j]+=pi[j]
    h=mp.lu_solve(AA,mp.matrix([J-gr[i] for i in range(4)]))
    var_rate=sum((pi[i]*kf+pi[j]*kr)*(reward+h[j]-h[i])**2
                 for i,j,kf,kr,reward,work,de,label in edges)
    p0=pi[1]/(pi[0]+pi[1]);p1=pi[3]/(pi[2]+pi[3])
    residual=max(abs(sum(pi[i]*Q[i,j] for i in range(4))) for j in range(4))
    return {'pi':list(map(str,pi)),'J':str(J),'gamma':str(gam),
       'count_variance_rate':str(var_rate),'Fano':str(var_rate/J),
       'asymptotic_time_for_one_percent_relative_SE_s':str(var_rate/(J*J*M('.01')**2)),'conditional_hot_empty':str(p0),
       'conditional_hot_adsorbed':str(p1),'currents':{k:str(v) for k,v in currents.items()},
       'entropy':str(entropy),'affinity_times_current':str(A*J),
       'energy_mode_balance':str(mode_balance),'chemical_power':str(power),
       'stationarity_residual':str(residual),
       'Q':[[str(Q[i,j]) for j in range(4)] for i in range(4)]}


def main():
    coupled=solve(True);base=solve(False)
    J_closed=a*c*(1-z)/((a+c)*(1+q)+(a+c*z)*(1+1/q))
    Jbase_closed=a*d*(1-z)/(a*(1+q)+d*(1+z/q))
    matched=[]
    D0=(1+q)*(1+z/q)/a+(1+q)*(1+1/q)/c
    C=1+q+1/q+z
    for gam in (gamma,M('.01')):
        on=solve(True,gam);off=solve('matched_off',gam)
        p00=M(on['pi'][0]);p10=M(on['pi'][2])
        origin=p00*a/(p00*(a+c*z)+p10*gam*q)
        matched.append({'on':on,'off':off,
          'same_thermal_projection_current':str((1-z)/D0),
          'off_current_closed':str((1-z)/(D0+C/gam)),
          'causal_capture_gain':str(1+C/(gam*D0)),
          'fraction_product_quanta_last_created_by_capture':str(origin),
          'cold_trap_mean_residence_s':str(1/(gam*q))})
    out={'matched_rerouting_same_Kbar':matched,'scope':'Synthetic two-stage full thermodynamic cycle, not measured ORR kinetics.',
      'gate_E_eV':str(E),'thermal_lifetime_s':str(tau),'q':str(q),
      'p_thermal':str(q/(1+q)),'affinity_per_net_cycle':str(A),
      'adsorption_rate_a':str(a),'hot_product_rate_c':str(c),
      'baseline_product_rate_d':str(d),'coupled':coupled,'uncoupled':base,
      'coupled_current_closed_form':str(J_closed),
      'uncoupled_current_closed_form':str(Jbase_closed),
      'paired_pathway_gain':str(J_closed/Jbase_closed),
      'energy_recycled_eV_per_s':str(E*J_closed),
      'coupled_J_minus_thermal_projection_J':str(M(coupled['J'])-J_closed),
      'warning':'The gain compares different Kbar chemical pathways; it is outside the fixed-pathway nonequilibrium-gate excess bound. Gap.126eV and barrier gain.192eV are only conditional illustrative choices. The two-stage product channel lumps a full driven cycle.'}
    Path(__file__).with_name('thermal_recycling_counterexample_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
