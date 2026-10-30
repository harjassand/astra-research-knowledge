"""Noncommuting overlapping own-corner witnesses: exact local congruence drift.
Finite operator regression for the abstract dressing step, not native service.
"""
import numpy as np,json
from scipy.linalg import expm,eigvalsh
from pathlib import Path
I2=np.eye(2);I=np.eye(4);X=np.array([[0,1],[1,0]],complex);Q=np.diag([0,1]);down=np.array([[0,1],[0,0]],complex)
qs=[np.kron(Q,I2),np.kron(I2,Q)]
js=[np.kron(down,I2),np.kron(I2,down)]
zs=[np.kron(Q,.6*I2+.1*X),np.kron(.6*I2+.1*X,Q)]
D=.7*qs[0]+.4*qs[1]+.2*qs[0]@qs[1]
P0=(I-qs[0])@(I-qs[1]);B=I-P0
r=.45

def Lc(O):return sum(J.conj().T@O@J-(J.conj().T@J@O+O@J.conj().T@J)/2 for J in js)
def Lw(O):return Lc(O)-(D@O+O@D)/2
for z,q in zip(zs,qs):assert eigvalsh(-Lc(z)-r*q)[0]>-1e-12
first=Lc(sum(zs));rows=[];maxcorner=0.;maxratio=0.;minmargin=1.
for delta in [1e-4,3e-4,1e-3,3e-3,.01,.03,.05,.1,.2]:
 Y=expm(delta*zs[1]/2)@expm(delta*zs[0]/2);Yi=np.linalg.inv(Y)
 M=Yi.conj().T@Lw(Y.conj().T@Y)@Yi
 R=M+D-delta*first
 corner=np.linalg.norm(R@P0);ratio=np.linalg.norm(R,2)/delta**2
 margin=float(eigvalsh(-D-delta*r/2*sum(qs)-M)[0])
 maxcorner=max(maxcorner,float(corner));maxratio=max(maxratio,float(ratio));minmargin=min(minmargin,margin)
 rows.append({'delta':delta,'relative_remainder_norm_over_delta_squared':float(ratio),'remainder_zero_corner_error':float(corner),'weighted_drift_margin':margin})
assert maxcorner<1e-12 and minmargin>-1e-12
out={'noncommuting_overlapping_witness_commutator':float(np.linalg.norm(zs[0]@zs[1]-zs[1]@zs[0])),'witness_other_Q_commutator':float(np.linalg.norm(zs[0]@qs[1]-qs[1]@zs[0])),'maximum_relative_second_order_remainder':maxratio,'minimum_weighted_drift_margin':minmargin,'maximum_remainder_good_corner_error':maxcorner,'rows':rows,'all_checks_pass':True,'scope':'finite exact operator check of local congruence and bad-corner remainder, not native circuit or useful DATA service'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
