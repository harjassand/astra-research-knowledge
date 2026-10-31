"""Exhaustive discrete check of consecutive-FULL-syndrome recovery.

One faulty complete round is conservatively allowed an arbitrary four-bit
report and any error in the larger one-X/one-Z Bacon-Shor-correctable set.
All later fault-free rounds report its actual stabilizer syndrome. This is
an overapproximation of mixed readings during sequential X/Z gauge sets.
"""
from pathlib import Path
import json

n=9
site=lambda r,c:3*r+c
pauli=lambda x=0,z=0:x|(z<<n)
xpart=lambda p:p&((1<<n)-1)
zpart=lambda p:p>>n
comm=lambda p,q:((xpart(p)&zpart(q)).bit_count()+(zpart(p)&xpart(q)).bit_count())%2==0
XX=[pauli(x=(1<<site(r,c))|(1<<site(r,c+1))) for r in range(3) for c in range(2)]
ZZ=[pauli(z=(1<<site(r,c))|(1<<site(r+1,c))) for r in range(2) for c in range(3)]
G={0}
for q in XX+ZZ:G|={p^q for p in list(G)}
stabs=[]
for c in range(2):
 q=0
 for r in range(3):q^=pauli(x=(1<<site(r,c))|(1<<site(r,c+1)))
 stabs.append(q)
for r in range(2):
 q=0
 for c in range(3):q^=pauli(z=(1<<site(r,c))|(1<<site(r+1,c)))
 stabs.append(q)
syndrome=lambda p:sum(int(not comm(p,q))<<j for j,q in enumerate(stabs))
# Pair bits: 01->row/col0;11->row/col1;10->row/col2.
location={0:None,1:0,3:1,2:2}
def correction(s):
 zcol=location[s&3];xrow=location[(s>>2)&3]
 return pauli(x=0 if xrow is None else 1<<site(xrow,0),
              z=0 if zcol is None else 1<<site(0,zcol))
errors=sorted({pauli(x=0 if i<0 else 1<<i,z=0 if j<0 else 1<<j) for i in range(-1,9) for j in range(-1,9)})

def recover(initial=0,fault_round=None,fault_error=0,fault_report=0):
 current=initial;previous=None;history=[];reached=False
 for r in range(1,5):
  if r==fault_round:
   reached=True;current^=fault_error;report=fault_report
  else:report=syndrome(current)
  history.append(report)
  if previous is not None and report==previous:
   return dict(rounds=r,history=history,accepted=report,residual=current^correction(report),
               fault_reached=reached,flag=False)
  previous=report
 return dict(rounds=4,history=history,accepted=None,residual=current,
             fault_reached=reached,flag=True)

violations=[];reached_cases=0;unreached_cases=0;counts={2:0,3:0,4:0}
examples={}
for f in range(1,5):
 for e in errors:
  for report in range(16):
   r=recover(fault_round=f,fault_error=e,fault_report=report)
   if not r['fault_reached']:
    unreached_cases+=1
    continue
   reached_cases+=1;counts[r['rounds']]+=1
   # At most one correctable X component and one Z component modulo gauge.
   correctable=any((r['residual']^q) in G for q in errors)
   # Sharper result: residual is either original E modulo gauge, or gauge.
   sharp=(r['residual'] in G) or ((r['residual']^e) in G)
   if r['flag'] or not correctable or not sharp:
    violations.append(dict(f=f,e=e,report=report,result=r))
   examples.setdefault(str(r['rounds']),dict(fault_round=f,error=e,fault_report=report,result=r))
input_violations=[]
for e in errors:
 r=recover(initial=e)
 if r['rounds']!=2 or r['residual'] not in G:
  input_violations.append(dict(error=e,result=r))

# Explicitly verify the gauge measurement properties supporting the round
# abstraction: same-axis sets commute, every gauge commutes with all centers.
checks={
 'XX_set_commutes':all(comm(p,q) for p in XX for q in XX),
 'ZZ_set_commutes':all(comm(p,q) for p in ZZ for q in ZZ),
 'all_gauges_commute_with_stabilizers':all(comm(p,q) for p in XX+ZZ for q in stabs),
 'noncommuting_XZ_gauges_present':any(not comm(p,q) for p in XX for q in ZZ),
}

# Bitwise-majority counterexample for one X fault in the middle row. First
# pre-fault syndrome=0, final true syndrome=11 in SZ bits, faulty report=01.
e=pauli(x=1<<site(1,0));bad=1<<2;true=syndrome(e)
majority=(0&bad)|(0&true)|(bad&true)
residual=e^correction(majority)
logical_X=pauli(x=sum(1<<site(r,0) for r in range(3)))
majority_failure=dict(history=[0,bad,true],majority=majority,true_syndrome=true,
                       residual= residual,
                       residual_in_single_X_single_Z_correctable_set=any((residual^q) in G for q in errors),
                       after_next_ideal_recovery_is_logical_X_mod_gauge=(residual^correction(syndrome(residual))^logical_X) in G)

out=dict(reference_model='ideal gauge instruments except at most one localized bad round/location',
         complete_round_gauge_measurements=12,max_complete_rounds=4,
         exhaustive_scheduled_cases=4*len(errors)*16,
         reached_fault_cases=reached_cases,unreached_after_early_stop_cases=unreached_cases,
         termination_round_histogram=counts,
         clean_input_one_fault_violations=violations,
         one_correctable_input_error_no_fault_violations=input_violations,
         gauge_round_checks=checks,examples=examples,bitwise_majority_counterexample=majority_failure,
         important_limit='No two-fault guarantee or threshold. Physical frame/controller reliability and fault containment/reset are explicit assumptions.')
Path(__file__).with_name('bacon_shor_recovery_check.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
