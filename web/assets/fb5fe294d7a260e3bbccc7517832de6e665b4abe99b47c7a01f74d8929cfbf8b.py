"""Small floating matrix checks of the weighted compressed Euler proof.

Not certified intervals, not a full expanded many-layer circuit, not an FPRAS.
Exact coefficient/compiler evidence is in the companion Fraction diagnostics.
"""
from pathlib import Path
import sys,json
from fractions import Fraction as F
from math import comb,sqrt
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from spin_projection_transfer import edge_gate,field_gate,embed


def ceil_fraction(q):
    q=F(q); return (q.numerator+q.denominator-1)//q.denominator


def matrix(gate):
    return np.array(embed(gate,3),dtype=float)


def dicke_isometry():
    v=np.zeros((8,6))
    for state in range(8):
        r=(state&3).bit_count(); t=(state>>2)&1
        v[state,2*r+t]=1/sqrt(comb(2,r))
    assert np.linalg.norm(v.T@v-np.eye(6),ord=2)<1e-12
    return v


def trial(beta,b0,c0,b1,c1,potential):
    alpha=F(7,5); gamma=F(-3,5)
    terms=[("edge",(i,2),alpha/4,gamma/4) for i in (0,1)]
    terms +=[("field",i,b0/2,c0/2) for i in (0,1)]
    terms +=[("field",2,b1/2,c1/2)]
    potential=tuple(map(F,potential)); shift=max(abs(f) for f in potential)
    c=3*alpha*F(1,2)+(b0+abs(c0))+(b1+abs(c1))/2+shift
    d=2*c; tau=beta*d; epsilon=F(1,2)
    m=ceil_fraction(max(F(1),4*tau,20*tau*tau/epsilon)); s=beta/(2*m)
    eye=np.eye(8); w=eye.copy(); shifted=np.zeros((8,8))
    for kind,qubits,a,g in terms:
        maker=lambda scale:edge_gate(qubits,a,g,scale) if kind=="edge" else field_gate(qubits,a,g,scale)
        w=w@matrix(maker(s))
        shifted+=matrix(maker(F(1)))-eye
    onsite=np.diag([float(shift+potential[(state&3).bit_count()]) for state in range(8)])
    shifted+=onsite
    onsite_euler=eye+float(s)*onsite
    w=onsite_euler@w
    v=dicke_isometry()
    compressed=v.T@(w@w.T)@v
    k=float(beta)*(v.T@shifted@v)
    ev,rotation=np.linalg.eigh(compressed)
    assert ev.min()>=1-1e-12
    log_b=(rotation*np.log(ev))@rotation.T
    generator_error=float(np.linalg.norm(m*log_b-k,ord=2))
    analytic_bound=float(5*tau*tau/m)
    log_zb=float(np.log(np.exp(m*np.log(ev)).sum()))
    log_zk=float(np.log(np.exp(np.linalg.eigvalsh(k)).sum()))
    assert generator_error<=analytic_bound+1e-10
    assert abs(log_zb-log_zk)<=generator_error+1e-9
    return {"beta":str(beta),"longitudinal_fields":[str(c0),str(c1)],"potential":[str(f) for f in potential],
            "m":m,"generator_error":generator_error,"analytic_bound":analytic_bound,
            "log_trace_error":abs(log_zb-log_zk)}


def checks():
    records=[]
    for beta in (F(1,20),F(1,5),F(1),F(3)):
        for potential in ((-2,0,-2),(-3,-1,-2)):
            for fields in ((F(0),F(0)),(F(-1,7),F(2,9))):
                records.append(trial(beta,F(1,3),fields[0],F(2,5),fields[1],potential))
    return {"status":"PASS","scope":"floating 6-dimensional compressed-generator diagnostics; no interval certification, expanded circuit or FPRAS executed",
            "trials":records,"max_ratio":max(r['generator_error']/r['analytic_bound'] for r in records)}


if __name__=="__main__":
    result=checks()
    Path(__file__).with_name('projected_thermal_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='trials'},indent=2))
