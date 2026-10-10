"""Check whether release-conditioning failure is just poor time-window choice."""
import json
import mpmath as mp
from release_condition import basis_value

mp.mp.dps=70
records=[]
for m in (3,4,5,6):
    c=[mp.mpf('0.7')+mp.mpf('0.6')*i/(m-1) for i in range(m)]
    for top in ('0.1','1','10','100','1000'):
        tau=[mp.mpf(top)*mp.mpf(i)/80 for i in range(81)]
        mat=mp.matrix([basis_value(c,t,mp) for t in tau])
        for col in range(mat.cols):
            norm=mp.sqrt(sum(mat[row,col]**2 for row in range(mat.rows)))
            for row in range(mat.rows): mat[row,col]/=norm
        s=mp.svd(mat,compute_uv=False)
        record=dict(hidden_nodes=m,tau_max=top,
                    column_normalized_condition=mp.nstr(s[0]/s[s.rows-1],18))
        records.append(record)
        print(json.dumps(record),flush=True)
with open(__file__.replace('.py','_results.json'),'w') as f:
    json.dump(records,f,indent=2)
