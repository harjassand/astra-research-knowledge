#!/usr/bin/env python3
"""Exact no-go family for single scalar-envelope loading when a bare positive
controller penalty selects a proper subcode. Analytic amplitudes and independent
high-precision matrix checks; no time-discretized Schr propagation is needed.
"""
import json
import mpmath as mp
mp.mp.dps=65
B=mp.mpf(1); Q=mp.mpf(2); a=mp.mpf(1)
rows=[]
for lv in [10,100,1000,10000,100000,1000000]:
    L=mp.mpf(lv); w1=mp.sqrt(L);w2=L
    W=mp.matrix([[w1,w2]])
    D=Q*(W.T*W)
    A=mp.diag([0,a])
    phi=mp.matrix([mp.sqrt(L/(1+L)),-1/mp.sqrt(1+L),0]);
    code=mp.matrix([1,0,0]);target=mp.matrix([1/mp.sqrt(1+L),0,-mp.sqrt(L)/mp.sqrt(1+L)])
    max_res=mp.mpf('0')
    for eta in [mp.mpf('0'),mp.mpf('.02'),mp.mpf('.4'),mp.mpf('1')]:
        AA=mp.matrix([[eta*eta*D[0,0],eta*eta*D[0,1],eta*Q*w1],
                      [eta*eta*D[1,0],eta*eta*D[1,1]+a,eta*Q*w2],
                      [eta*Q*w1,eta*Q*w2,Q]])
        resid=AA*phi-mp.matrix([0,-a/mp.sqrt(1+L),0])
        resid_target=AA*target if eta==1 else mp.matrix([0,0,0])
        max_res=max(max_res,mp.sqrt(sum(z*z for z in resid)))
        if eta==1:target_res=mp.sqrt(sum(z*z for z in resid_target))
    eps0=mp.sqrt(2-2*mp.sqrt(L/(1+L)))
    overlap=mp.sqrt(L)/(1+L)
    T=mp.mpf(10)
    bound=min(mp.mpf(1),overlap+eps0+a*T/mp.sqrt(1+L))
    min_time_for_probability_90=max(mp.mpf(0),(mp.sqrt(mp.mpf('.9'))-overlap-eps0)*mp.sqrt(1+L)/a)
    rows.append({'lambda':lv,'eta_independent_trapping_residual':mp.nstr(max_res,8),
      'final_code_eigenstate_residual':mp.nstr(target_res,8),
      'initial_state_distance_from_trap':float(eps0),
      'trap_target_overlap':float(overlap),
      'upper_bound_success_amplitude_at_T_10':float(bound),
      'upper_bound_success_probability_at_T_10':float(bound**2),
      'necessary_T_for_at_least_0p9_success_probability':float(min_time_for_probability_90),
      'commutator_norm_squared':float(2*a*a*L**3)})
res={'model':'H_eta+B=R_eta^* Q R_eta+diag(A,0) with R_eta=(eta sqrt(lambda),eta lambda,1), Q=2, A=diag(0,1)',
     'scope':'arbitrary time-dependent scalar eta(t), optional abrupt switching, no extra controls; exact noncommuting bare-controller obstruction',
     'data':rows}
with open('/mnt/data/astra_restricted_controller_no_go.json','w') as f:json.dump(res,f,indent=2)
print(json.dumps(res,indent=2))
