"""Independent exact-size one-block checks; numpy floating point, not formal proof."""
import numpy as np
import json
from pathlib import Path
I=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1])
def pauli(p):
    a=np.array([[1.]])
    for c in p: a=np.kron(a, {'I':I,'X':X,'Z':Z}[c])
    return a
D=32; eye=np.eye(D)
def controlled(control,target,kind):
    a=np.zeros((D,D))
    for k in range(D):
        bits=[(k>>(4-i))&1 for i in range(5)]
        j=k; phase=1
        if bits[control]:
            if kind=='X':j=k^(1<<(4-target))
            else:phase=(-1)**bits[target]
        a[j,k]=phase
    return a
# Order: data, X copy 0, X copy 1, Z copy 0, Z copy 1.
U=controlled(3,0,'Z')@controlled(1,0,'X')
checks={}
def test(name,a,b):
    err=float(np.max(np.abs(a-b))); checks[name]=err; assert err<1e-12,(name,err)
test('unitary',U.T@U,eye)
test('Z_check_frame',U.T@pauli('ZIIII')@U,pauli('ZZIII'))
test('X_check_frame',U.T@pauli('XIIII')@U,pauli('XIIZI'))
for p in ['IZIII','IIZII','IIIZI','IIIIZ']:
    test('witness_phase_gauge_'+p,U.T@pauli(p)@U,pauli(p))
for p in ['IZZII','IIIZZ']:
    test('copy_parity_'+p,U.T@pauli(p)@U,pauli(p))
test('witness_flip_not_harmless',U.T@pauli('IXIII')@U,pauli('XXIII'))
Paux=(eye+pauli('IZZII'))@(eye+pauli('IIIZZ'))/4
for typ,physical,framed in [('Z','ZIIII','ZZIII'),('X','XIIII','XIIZI')]:
    P0=(eye+pauli(physical))@Paux/2
    Pg=(eye+pauli(framed))@Paux/2
    test('ground_projector_'+typ,U@P0@U.T,Pg)
    checks['ground_rank_'+typ]=int(round(np.trace(Pg)))
Path(__file__).with_name('clifford_results.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
