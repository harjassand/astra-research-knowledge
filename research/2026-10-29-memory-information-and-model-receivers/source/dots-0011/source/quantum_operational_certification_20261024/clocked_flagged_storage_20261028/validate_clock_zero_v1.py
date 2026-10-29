from pathlib import Path
import numpy as np,json
import clocked_channel_v1 as m
HERE=Path(__file__).parent
basis=[np.ones((1,1),complex)]
for _ in range(5):basis=[np.kron(a,p) for a in basis for p in m.P]
B=np.array([p.reshape(-1) for p in basis]).T
clock={'one':1.,'two':2.,'prep':2.,'measure':4.,'feedback':1.}
F,timing=m.build_ec(.001,0.,clock)
K,_,_=m.old.ec_kraus(.001);Fd=m.old.superop(K)
expected=(B.conj().T@Fd@B/32).real
err=float(np.max(abs(F-expected)));assert err<2e-12
initial,D=m.code_coordinates()
F0,_=m.build_ec(0.,0.,clock);err0=float(np.max(abs(F0-initial@D)));assert err0<2e-12
out={'status':'PASS_AUTHOR_CROSS_REPRESENTATION_FULL_OPERATOR_CHECK','eta_001_zero_background_max_difference':err,'eta_zero_background_zero_full_reset_max_difference':err0,'scope':'Pauli-transfer clock model at zero background versus prior193-Kraus coherent-noise channel on all physical operators; not independent review of clocked nonzero background.'}
(HERE/'validate_clock_zero_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
