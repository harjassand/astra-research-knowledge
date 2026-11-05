"""Floating feasibility gate only: periodic-score witness resolvent.

No confidence interval or exact-sampling claim is made by this screen.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix

ROOT=Path(__file__).resolve().parent

def model(path,geodesic=True):
    G=json.loads(Path(path).read_text()); edges=G['edges']; nd=G['internal_vertices']
    p=np.array([x['p_float'] for x in G['errors']]); costs=np.array(G['costs'])
    n=max(max(e) for e in edges)+1; adj=[[] for _ in range(n)]
    directed=[]
    for i,(u,v) in enumerate(edges):
        adj[u].append((v,i));adj[v].append((u,i));directed.extend([(u,v,i),(v,u,i)])
    sid={(u,v):i for i,(u,v,e) in enumerate(directed)}
    states=np.array([(u,v,e,b) for u,v,e in directed for b in (0,1)],dtype=np.int64)
    w=np.stack([(1-p)*2.**(-costs),p*2.**costs],axis=1)
    shortcuts={(min(u,v),max(u,v)):costs[e] for e,(u,v) in enumerate(edges)}
    data={int(d):[[],[],[]] for c in set(costs) for d in (-c,c)}
    for i,(u,v,e,b0) in enumerate(states):
        if v>=nd:continue
        for z,f in adj[v]:
            if z==u:continue
            triangle=shortcuts.get((min(u,z),max(u,z)),10**9)<costs[e]+costs[f]
            for b in (0,1):
                if geodesic and b0==b==0 and triangle:continue
                j=2*sid[v,z]+b;d=int(costs[f]*(2*b-1))
                row,col,val=data[d];row.append(i);col.append(j);val.append(w[f,b])
    T={d:csr_matrix((val,(row,col)),shape=(len(states),len(states))) for d,(row,col,val) in data.items()}
    starts=np.array([2*sid[u,adj[u][0][0]]+b for u in G['left'] for b in (0,1)])
    end=np.isin(states[:,1],G['right'])
    return G,states,p,costs,w,T,starts,end

def solve(path,N,geodesic=True,save=False):
    ts=time.perf_counter();G,states,p,costs,w,T,starts,end=model(path,geodesic)
    base=end[:,None]*np.exp2(-np.arange(N,dtype=float))[None,:]
    H=base.copy();residual=None
    for it in range(600):
        new=base.copy()
        for d,A in T.items():new+=A@np.roll(H,-d,axis=1)
        residual=float(np.max(np.abs(new-H)));H=new
        if residual<1e-19:break
    e=states[starts,2];b=states[starts,3];scores=costs[e]*(2*b-1)
    Z=float(np.sum(w[e,b]*H[starts,scores%N]))
    result={'scope':'floating normalizer screen only','input':str(Path(path).name),'geodesic':geodesic,'modulus':N,'directed_bit_states':len(states),'transition_count':sum(A.nnz for A in T.values()),'iterations':it+1,'last_absolute_update':residual,'folded_normalizer':Z,'table_bytes':H.nbytes,'seconds':time.perf_counter()-ts}
    if save:np.savez_compressed(ROOT/f'table_N{N}_geo{int(geodesic)}.npz',H=H,states=states,starts=starts,end=end,modulus=N)
    return result

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--input',default=str(ROOT.parent/'canonical_qec_circuit_gate_20261105/d13_r13_p1_1000_graph.json'));a.add_argument('--moduli',default='16,32,64,128');a.add_argument('--unrestricted',action='store_true');a.add_argument('--save',action='store_true');args=a.parse_args()
    out=[]
    for N in map(int,args.moduli.split(',')):
        r=solve(args.input,N,not args.unrestricted,args.save);out.append(r);print(json.dumps(r),flush=True);(ROOT/'screen_results.json').write_text(json.dumps(out,indent=2)+'\n')
