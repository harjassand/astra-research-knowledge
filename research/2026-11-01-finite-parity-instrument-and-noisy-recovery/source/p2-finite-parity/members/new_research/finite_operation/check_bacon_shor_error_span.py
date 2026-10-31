"""Exact binary-Pauli check: 3x3 Bacon-Shor subsystem error containment.

Conventions: XX horizontal gauge, ZZ vertical gauge. Phases are irrelevant
for gauge membership / Knill-Laflamme support conditions.
"""
from pathlib import Path
import json

n=9
site=lambda r,c:3*r+c
p=lambda x=0,z=0:x|(z<<n)
xpart=lambda a:a&((1<<n)-1)
zpart=lambda a:a>>n
commutes=lambda a,b:((xpart(a)&zpart(b)).bit_count()+(zpart(a)&xpart(b)).bit_count())%2==0
xx=[];zz=[]
for r in range(3):
 for c in range(2):xx.append(p(x=(1<<site(r,c))|(1<<site(r,c+1))))
for r in range(2):
 for c in range(3):zz.append(p(z=(1<<site(r,c))|(1<<site(r+1,c))))
gauges=xx+zz
G={0}
for g in gauges:G|={v^g for v in list(G)}
stabilizers=[]
for c in range(2):
 a=0
 for r in range(3):a^=p(x=(1<<site(r,c))|(1<<site(r,c+1)))
 stabilizers.append(a)
for r in range(2):
 a=0
 for c in range(3):a^=p(z=(1<<site(r,c))|(1<<site(r+1,c)))
 stabilizers.append(a)
syndrome=lambda a:tuple(int(not commutes(a,s)) for s in stabilizers)

# All products with <=one X component and <=one Z component, including Y.
errors=sorted({p(x=(0 if i<0 else 1<<i),z=(0 if j<0 else 1<<j)) for i in range(-1,n) for j in range(-1,n)})
violations=[]
for a in errors:
 for b in errors:
  q=a^b
  if all(commutes(q,s) for s in stabilizers) and q not in G:
   violations.append([a,b,q])

# Each vertical ZZ gauge: diagonal pair algebra, and arbitrary one-qubit
# fault on either participant, reduce to a single-site Pauli times gauge.
local_cases=[]
for r in range(2):
 for c in range(3):
  i,j=site(r,c),site(r+1,c)
  S=p(z=(1<<i)|(1<<j))
  D=[0,p(z=1<<i),p(z=1<<j),S]
  for target in (i,j):
   local=[0,p(x=1<<target),p(z=1<<target),p(x=1<<target,z=1<<target)]
   actual={d^q for d in D for q in local}
   ok=all(any((a^e) in (0,S) for e in local) for a in actual)
   local_cases.append(dict(pair=[i,j],fault_site=target,all_supported_errors_reduce=ok))

# Explicit standard syndrome recovery to row-X/column-Z representatives.
recoveries=[]
for e in errors:
 xr=[sum((xpart(e)>>site(r,c))&1 for c in range(3))%2 for r in range(3)]
 zc=[sum((zpart(e)>>site(r,c))&1 for r in range(3))%2 for c in range(3)]
 recovery=0
 for r,v in enumerate(xr):
  if v:recovery^=p(x=1<<site(r,0))
 for c,v in enumerate(zc):
  if v:recovery^=p(z=1<<site(0,c))
 recoveries.append((e^recovery) in G)

out=dict(qubits=n,gauge_group_size_ignoring_phases=len(G),gauge_generator_count=len(gauges),
         stabilizer_generator_count=len(stabilizers),error_span_Pauli_count=len(errors),
         ordered_error_pairs_checked=len(errors)**2,subsystem_KL_violations=violations,
         all_row_column_recoveries_gauge_equivalent=all(recoveries),
         local_fault_cases=local_cases,
         all_local_fault_cases_pass=all(q['all_supported_errors_reduce'] for q in local_cases))
Path(__file__).with_name('bacon_shor_error_span_check.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
