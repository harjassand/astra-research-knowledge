"""Exact-rational first-time multiport counterfactual on a grounded star.
No fit to edge functions: only physically measured boundary combinations.
This is an exact source constructed in Q, under inverse slope bands.
"""
from fractions import Fraction as Q

S=Q(12,25) # 0.48
q=Q(3,25)  # 0.12 for four service ports

def trunk(t): return Q(3,25)*t+Q(9,100)*t*abs(t)
def branch0(t):return Q(9,25)*t+Q(7,100)*t*abs(t)

y_reference_inactive=trunk(S)
y_probe_inactive=trunk(q)
y_probe_active=trunk(q)+branch0(q)
y_task_true=trunk(S)+branch0(q)
y_task_stitched=y_reference_inactive+y_probe_active-y_probe_inactive
assert y_task_stitched==y_task_true==Q(7659,62500) # 0.122544

lower_no_history=Q(1,10)*S+Q(3,10)*q
upper_no_history=Q(1,2)*S+Q(4,5)*q
info_floor=(Q(1,2)-Q(1,10))*(S-q)
assert (lower_no_history,upper_no_history)==(Q(21,250),Q(42,125)) # 0.084,.336
assert info_floor==Q(18,125) # .144

print('reference inactive =',y_reference_inactive,'=',float(y_reference_inactive))
print('service probe active =',y_probe_active,'=',float(y_probe_active))
print('service probe inactive =',y_probe_inactive,'=',float(y_probe_inactive))
print('counterfactual target =',y_task_stitched,'=',float(y_task_stitched))
print('source-only prior [',lower_no_history,',',upper_no_history,']')
print('unavoidable without trunk calibration =',info_floor)
