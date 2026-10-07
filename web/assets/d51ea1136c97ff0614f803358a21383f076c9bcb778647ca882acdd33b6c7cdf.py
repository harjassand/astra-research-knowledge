#!/usr/bin/env python3
"""Small exact algebra checks and admitted-boundary interval compiler replays."""
import contextlib
from fractions import Fraction as F
import importlib.util
import io
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('compiler',HERE/'certified_two_spin.py')
compiler=importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)

def c(r=0,i=0): return (F(r),F(i))
def ca(x,y): return (x[0]+y[0],x[1]+y[1])
def cm(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def cs(x,t): return (x[0]*t,x[1]*t)
def ma(A,B): return [[ca(a,b) for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def scale(A,t): return [[cs(x,F(t)) for x in row] for row in A]
def mm(A,B):
    n=len(A)
    return [[sumc(cm(A[i][k],B[k][j]) for k in range(n)) for j in range(n)] for i in range(n)]
def sumc(xs):
    out=c()
    for x in xs: out=ca(out,x)
    return out
def tensor(A,B):
    return [[cm(A[i//len(B)][j//len(B)],B[i%len(B)][j%len(B)])
             for j in range(len(A)*len(B))] for i in range(len(A)*len(B))]

I=[[c(1),c()],[c(),c(1)]]
X=[[c(),c(1)],[c(1),c()]]
Y=[[c(),c(0,-1)],[c(0,1),c()]]
Z=[[c(1),c()],[c(),c(-1)]]
II=tensor(I,I)
XX,YY,ZZ=[tensor(P,P) for P in [X,Y,Z]]
J=[scale(ma(tensor(P,I),tensor(I,P)),F(1,2)) for P in [X,Y,Z]]
J2=ma(ma(mm(J[0],J[0]),mm(J[1],J[1])),mm(J[2],J[2]))
assert J2==ma(scale(II,F(3,2)),scale(ma(ma(XX,YY),ZZ),F(1,2)))
assert ma(mm(J[0],J[0]),scale(mm(J[1],J[1]),-1))==scale(ma(XX,scale(YY,-1)),F(1,2))
assert J[2]==scale(ma(tensor(Z,I),tensor(I,Z)),F(1,2))
commutator=ma(mm(ma(mm(J[0],J[0]),scale(mm(J[1],J[1]),-1)),J[2]),
              scale(mm(J[2],ma(mm(J[0],J[0]),scale(mm(J[1],J[1]),-1))),-1))
assert any(x!=c() for row in commutator for x in row)

cases=[(a,b,32) for a in ['-1','0','1'] for b in ['-1/2','0','1/2']]
cases += [('1/4','1/8',64),('1/4','1/8',128),
          ('1/1099511627776','-1/1099511627776',64)]
summaries=[]
start=time.perf_counter()
for index,(a,b,k) in enumerate(cases):
    out=HERE/'evidence'/'boundary'/f'case_{index:02d}.json'
    compiler.ledger=compiler.Ledger()
    old=sys.argv
    sys.argv=['certified_two_spin.py','--a='+a,'--b='+b,'--error-bits',str(k),
              '--uniform-integer',str((1<<(k+8))-1),'--out',str(out)]
    try:
        with contextlib.redirect_stdout(io.StringIO()): compiler.main()
    finally:
        sys.argv=old
    data=json.loads(out.read_text())
    assert data['sample_local_preparation']['branch_label']=='mixed'
    assert data['sample_local_preparation']['mixed_emission_independent_bits']==[0,1]
    qs=[F(x) for x in data['dyadic_rational_weights']]
    tau=[]
    for P in [X,scale(X,-1),Y,scale(Y,-1),Z,scale(Z,-1),[[c(),c()],[c(),c()]]]:
        tau.append(scale(ma(I,P),F(1,2)))
    density=[[c() for _ in range(4)] for _ in range(4)]
    for q,t in zip(qs,tau): density=ma(density,scale(tensor(t,t),q))
    expected=[[c(F(x)) for x in row] for row in data['compiled_density_matrix']]
    assert density==expected
    ns=data['dyadic_integer_weights']
    W=data['precision']['weight_denominator_bits']
    cumul=0
    for j,n in enumerate(ns):
        assert n>0
        draw=compiler.emit(ns,W,cumul,[0,1])
        assert draw['branch_index']==j
        cumul+=n
    assert cumul==(1<<W)
    summaries.append({'a':a,'b':b,'error_bits':k,'output':str(out.relative_to(HERE)),
                      'mixture_error_upper':data['mixture_trace_distance_upper'],
                      'matrix_error_upper':data['independent_direct_matrix_certificate']['direct_trace_distance_upper'],
                      'max_observed_integer_bits':data['costs']['audit_including_cumulative_arithmetic']['max_observed_integer_bits']})
report={'status':'EXACT_IDENTITIES_AND_12_INTERVAL_REPLAYS_PASS',
        'exact_pauli_identity_checks':3,'exact_noncommutator_witness':True,
        'rational_complex_mixture_reconstructions':len(cases),
        'exact_dyadic_boundary_selection_cases':7*len(cases),
        'cases':summaries,'wall_seconds':time.perf_counter()-start,
        'scope':'Implementation checks for this admitted N=2 family; not a theorem or hardware validation.'}
(HERE/'evidence'/'boundary_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'cases':len(cases),'wall_seconds':report['wall_seconds']}))
