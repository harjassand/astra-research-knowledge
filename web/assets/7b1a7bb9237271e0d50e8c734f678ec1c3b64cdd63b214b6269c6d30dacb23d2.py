"""Exact tests concentrated near locally supported graph-basis shifts."""
import json
from pathlib import Path
import numpy as np
from mixed_graph_search import evaluate

def run(n=8):
    unit=[]
    for i in range(n):
        for a in (1,2):
            z=np.zeros(n,dtype=int);z[i]=a;unit.append(z)
    unit=np.array(unit)
    shifts=np.vstack([np.zeros((1,n),dtype=int),unit])
    delta=[];v=[];w=[]
    for d in shifts:
        for u in unit:
            delta.append(d);v.append(u);w.append(u)
            delta.append(d);v.append(u);w.append(2*u%3)
    delta,v,w=map(np.array,(delta,v,w));records=[];negative=[]
    for typ in ('star','cycle','complete','bipartite'):
        G=np.zeros((n,n),dtype=int)
        for i in range(n):
            for j in range(i+1,n):
                edge=(i==0) if typ=='star' else ((j==i+1) or (i==0 and j==n-1)) if typ=='cycle' else True if typ=='complete' else (i<n//2<=j)
                G[i,j]=G[j,i]=int(edge)
        for changed in (False,True):
            H=G.copy()
            if changed:H[0,1]=H[1,0]=(H[0,1]+1)%3
            a,b,p,q,L=evaluate(G,H,delta,v,w)
            assert np.all(a>=0) and np.all(b>=0)
            gaps=[int(aa)*int(bb)-int(pp)**2+int(pp)*int(qq)-int(qq)**2 for aa,bb,pp,qq in zip(a,b,p,q)]
            for idx,z in enumerate(gaps):
                if z<0:negative.append({'kind':typ,'changed':changed,'index':idx,'delta':delta[idx].tolist(),'v':v[idx].tolist(),'w':w[idx].tolist(),'a':int(a[idx]),'b':int(b[idx]),'p':int(p[idx]),'q':int(q[idx]),'scale':L})
            rec={'sites':n,'kind':typ,'one_edge_changed':changed,'planes':len(gaps),'negative':sum(z<0 for z in gaps),'zero':sum(z==0 for z in gaps),'minimum_scaled_determinant':str(min(gaps)),'scale':L}
            records.append(rec);print(json.dumps(rec),flush=True)
    out={'status':'exact tests on stated restricted planes, not full rank-two positivity','records':records,'negative_certificates':negative}
    Path(__file__).with_name('FOCUSED_GRAPH_n8.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':run()
