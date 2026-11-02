import sys,json,numpy as np
sys.path.insert(0,'producer-workspace/consequential_alternative_20261102')
from rectangle_repetition import quant
from analog_quantization import bins
out=[]
for v in [.38,.4]:
 for K in [2,3]:
  r=3;small=quant(v/r,K);w=np.array(small['w']);pq=np.array(small['p']);pp=bins(v*r,[])[3][0]
  P=np.column_stack([(1-pq)*(1-pp),pq*(1-pp),pq*pp,(1-pq)*pp]);Ic=1-small['H']-float(-(pp*np.log2(pp)+(1-pp)*np.log2(1-pp)))
  out.append(dict(v=v,r=r,K=K,w=w.tolist(),pauli=P.tolist(),thresholds_normalized=small['thresholds'],thresholds_physical_q=(np.array(small['thresholds'])*np.sqrt(r)).tolist(),unflagged_p_error=float(pp),Ic1=Ic,partition='Bins of |q syndrome| only; discard p reliability but not the quantum output. All flags retained.',probabilities='Gaussian CDF differences; float64, no interval certificate'))
json.dump(out,open('producer-workspace/highnoise_scalarflags_r3.json','w'),indent=2)
print([(x['v'],x['K'],x['Ic1']) for x in out])
