"""Exact tests of the new dissipation-weighted theorem, not acquisition.

Includes nonnormal switching primitives with singular source dissipation,
singular dictionaries, and exact Julia input/output energy conservation.
"""
from itertools import product
from pathlib import Path
import json
from rational_linalg import Mat, Q, diag, zeros, norm2, psd, block

I=diag(1,1)
rotation=Mat([[Q(3,5),-Q(4,5)],[Q(4,5),Q(3,5)]])
A=[diag(1,Q(3,5))*rotation.T, rotation*diag(Q(5,13),1)]
Tphysical=[diag(1,Q(1,2))*rotation.T, rotation*diag(Q(1,3),1)]
B=[diag(0,Q(4,5)),rotation*diag(Q(12,13),0)*rotation.T]
C=[rotation*diag(0,Q(4,5))*rotation.T,diag(Q(12,13),0)]
Kphysical=[diag(0,Q(1,8))*rotation.T,rotation*diag(Q(1,18),0)]
Lphysical=[rotation*diag(0,Q(1,8)),diag(Q(1,18),0)*rotation.T]
theta_squared=Q(1,48)
for i in range(2):
    assert B[i]*B[i] == I-A[i]*A[i].T
    assert C[i]*C[i] == I-A[i].T*A[i]
    julia=block(A[i],B[i],C[i],(-1)*A[i].T)
    assert julia.T*julia == diag(1,1,1,1)
assert A[0]*A[1] != A[1]*A[0]

b=Mat([Q(3,5),Q(4,5)])
word_checks=0
largest_ratio_squared=Q(0)
for V in [I,Mat([[Q(3,5),0,Q(4,5)],[0,1,0]])]:
    # Both syntheses are coisometries; the second has a singular Gram matrix.
    assert V*V.T == I
    r=V.cols
    W=diag(*([1]*r))
    G=V.T*V
    c=V.T*b
    T=[V.T*t*V for t in Tphysical]
    S=[t.T for t in T]
    D=[A[i]*V-V*T[i] for i in range(2)]
    J=[A[i].T*V-V*S[i] for i in range(2)]
    K=[k*V for k in Kphysical]
    L=[l*V for l in Lphysical]
    R=[W-t.T*W*t for t in T]
    Rdual=[W-s.T*W*s for s in S]
    for i in range(2):
        assert D[i] == B[i]*K[i] and J[i] == C[i]*L[i]
        assert psd(R[i]) and psd(Rdual[i])
        assert psd(theta_squared*R[i]-K[i].T*K[i])
        assert psd(theta_squared*Rdual[i]-L[i].T*L[i])
    for h in range(8):
        for word in product(range(2),repeat=h):
            alpha=[c]
            for i in word:
                alpha.append(T[i]*alpha[-1])
            beta=[None]*(h+1)
            beta[h]=c
            for t in range(h-1,-1,-1):
                beta[t]=S[word[t]]*beta[t+1]
            prediction=(c.T*G*alpha[h])[0]
            truth_state=b
            e=zeros(2)
            sum_u=sum_v=sum_y=sum_raw=Q(0)
            remainder=Q(0)
            for t,i in enumerate(word):
                u=K[i]*alpha[t]
                v=L[i]*beta[t+1]
                raw=C[i]*e
                y=raw-A[i].T*u
                remainder+=(v.T*raw)[0]
                prediction+=(beta[t+1].T*V.T*D[i]*alpha[t])[0]
                e=A[i]*e+B[i]*u
                truth_state=A[i]*truth_state
                sum_u+=norm2(u); sum_v+=norm2(v)
                sum_y+=norm2(y); sum_raw+=norm2(raw)
            truth=(b.T*truth_state)[0]
            assert e == truth_state-V*alpha[h]
            assert truth-prediction == remainder
            assert norm2(e)+sum_y == sum_u
            assert sum_raw <= 4*sum_u
            assert remainder**2 <= sum_raw*sum_v <= 4*sum_u*sum_v
            loss_f=norm2(c)-norm2(alpha[h])
            loss_b=norm2(c)-norm2(beta[0])
            assert sum_u <= theta_squared*loss_f
            assert sum_v <= theta_squared*loss_b
            full_bound_squared=4*theta_squared**2*loss_f*loss_b
            assert remainder**2 <= full_bound_squared
            if full_bound_squared:
                largest_ratio_squared=max(largest_ratio_squared,
                                          remainder**2/full_bound_squared)
            word_checks+=1

# Lower bound on raw-kernel gain: scalar a, flat input, sufficiently long word.
a=Q(99,100)
warmup,total=1000,100000
gain_lower_squared=(1+a)**2*(1-a**warmup)**2*Q(total-warmup,total)
assert gain_lower_squared > Q(197,100)**2

# Finite-width moments do not bound inverse source dissipation.
rho,delta=Q(1,2),Q(1,10**6)
weighted_values=[]
for eta in [Q(1,10**3),Q(1,10**6),Q(1,10**9)]:
    weighted=delta*(1-eta-rho)**2/(1-(1-eta)**2)
    ordinary=delta*(1-eta-rho)**2
    for h in range(101):
        gap=delta*((1-eta)**h-rho**h)
        assert abs(gap) <= delta
    assert ordinary <= delta
    weighted_values.append({'eta':str(eta),'weighted_form':float(weighted)})

report={
    'arithmetic':'exact standard-library Fraction',
    'word_checks':word_checks,
    'max_word_length':7,
    'source_dimension':2,
    'coefficient_dimensions':[2,3],
    'singular_source_dissipation':True,
    'singular_dictionary_case':True,
    'nonnormal_noncommuting_source_case':True,
    'julia_energy_equalities_verified':True,
    'theta_f_squared':str(theta_squared),
    'theta_b_squared':str(theta_squared),
    'largest_observed_squared_remainder_to_bound_ratio':float(largest_ratio_squared),
    'raw_kernel_l2_gain_proved_greater_than':'1.97',
    'moment_interval_radius':str(delta),
    'inverse_dissipation_ambiguity':weighted_values,
    'actual_source_acquisition_claim':False}
Path(__file__).with_name('dissipation_weighted_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
