"""Training-only detector count partition for paired differential inference.

All detector/probe categories remain recorded. The software partition greedily
retains Bhattacharyya information from the ten training endpoint patterns.
Held-out truths are not accessed while choosing the partition.
"""
from pathlib import Path
import json,time,heapq
import numpy as np
from paired_screen import load
ROOT=Path(__file__).resolve().parents[1]
CLASSES=[0,10,11,15,16]

def main():
    start=time.monotonic();sr,r,d=load('rigid256');st,t,_=load('phonon4_sigma01')
    q=np.concatenate([[r[sr.index(h)] for h in CLASSES],[t[st.index(h)] for h in CLASSES]]).reshape(10,-1)
    root_sum=q.sum(1);s=np.sqrt(q)
    full=.5*np.maximum(root_sum[:,None]+root_sum[None,:]-2*s@s.T,0)
    norms=np.where(np.eye(10,dtype=bool),np.inf,np.maximum(full,1e-16))
    leaves={};heap=[];uid=0
    def leaf(idx):
        nonlocal uid
        qq=q[:,idx];tot=qq.sum(1);sq=np.sqrt(qq)
        exact=.5*np.maximum(tot[:,None]+tot[None,:]-2*sq@sq.T,0)
        coarse=.5*(np.sqrt(tot[:,None])-np.sqrt(tot[None,:]))**2
        losses=np.maximum(exact-coarse,0)/norms
        a,b=np.unravel_index(np.argmax(losses),losses.shape);score=float(losses[a,b])
        k=uid;uid+=1;leaves[k]=(idx,a,b,score);heapq.heappush(heap,(-score,k))
    leaf(np.arange(q.shape[1]));checkpoints=[]
    for target in [32,64,128,256]:
        while len(leaves)<target:
            _,key=heapq.heappop(heap)
            if key not in leaves:continue
            idx,a,b,score=leaves.pop(key)
            if len(idx)<2 or score<=1e-16:leaves[key]=(idx,a,b,score);break
            x=np.log(np.maximum(q[a,idx],1e-300))-np.log(np.maximum(q[b,idx],1e-300))
            order=np.argsort(x);idx=idx[order]
            ca=np.cumsum(q[a,idx]);cb=np.cumsum(q[b,idx]);ta=ca[-1];tb=cb[-1]
            # Maximize recovered two-bin information for the selected pair.
            gain=(np.sqrt(ca[:-1])-np.sqrt(cb[:-1]))**2+(np.sqrt(np.maximum(ta-ca[:-1],0))-np.sqrt(np.maximum(tb-cb[:-1],0)))**2
            cut=int(np.argmax(gain))+1
            leaf(idx[:cut]);leaf(idx[cut:])
        codes=np.empty(q.shape[1],np.int32)
        for k,(idx,_,_,_) in enumerate(leaves.values()):codes[idx]=k
        grouped=np.stack([np.bincount(codes,weights=row,minlength=len(leaves)) for row in q])
        ss=np.sqrt(grouped);gg=grouped.sum(1)
        B=.5*np.maximum(gg[:,None]+gg[None,:]-2*ss@ss.T,0)
        off=~np.eye(10,dtype=bool)
        retention=float(np.min(B[off]/full[off]))
        item={'bins':len(leaves),'minimum_endpoint_pair_information_retained':retention,
              'elapsed_seconds':time.monotonic()-start};checkpoints.append(item);print(json.dumps(item),flush=True)
        np.savez_compressed(ROOT/f'outputs/count_partition_{target}.npz',codes=codes,training_patterns=grouped,
                            class_labels=CLASSES,scan_cell_area=float(d['scan_cell_area']),positions=d['positions'])
    (ROOT/'outputs/compression.json').write_text(json.dumps({'scope':__doc__,'checkpoints':checkpoints,
         'endpoint_order':'rigid five classes then thermal five classes','heldout_used_for_partition':False,
         'elapsed_seconds':time.monotonic()-start},indent=2))
if __name__=='__main__':main()
