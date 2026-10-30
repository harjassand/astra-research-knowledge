# Exact dyadic test of the distinction identified during independent review.
import numpy as np,json
from pathlib import Path
# Consistent terminal history U|0>=|+>; bad workspace history is |->.
P=np.array([[.5,.5],[.5,.5]]);B=np.eye(2)-P
J=[np.array([[1.,0.],[0.,0.]]),np.array([[0.,1.],[0.,0.]])]
loss=[j.T@j for j in J]
# After terminal reset, Q0 clean projector is |0><0|.
Bpost=np.diag([0.,1.])
comm=[a@B-B@a for a in loss]
assert any(np.any(x!=0) for x in comm)
assert np.array_equal(sum(loss),np.eye(2))
assert all(np.array_equal(Bpost@j@P,np.zeros((2,2))) for j in J)
# Whole instrument has exact drift -B on this source block.
drift=sum(j.T@Bpost@j for j in J)-(sum(loss)@B+B@sum(loss))/2
assert np.array_equal(drift,-B)
out={'individual_loss_commutators':[x.tolist() for x in comm], 'summed_loss_commutes':True,'individual_good_range_preserved':True,'bundled_source_drift_minus_B':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
