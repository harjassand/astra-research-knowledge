"""Exact F7/F7* witness search in fundamental binary matrices."""
from pathlib import Path
from itertools import combinations
import json
from bdl_matroid_probe import rank_and_relations

def read_matrix(path):
    a=list(map(int,path.read_text().split()));r,n,nz=a[:3]
    rows=[0]*r;cols=[0]*n
    for t in range(nz):
        i,j,v=a[3+3*t:6+3*t];assert v==1
        rows[i-1]|=1<<(j-1);cols[j-1]|=1<<(i-1)
    return rows,cols

def support(v):
    out=[]
    while v:
        b=v&-v;out.append(b.bit_length()-1);v^=b
    return out

def search(rows,cols):
    seen=set()
    for full,c in enumerate(cols):
        for i,j,k in combinations(support(c),3):
            if (i,j,k) in seen:continue
            seen.add((i,j,k))
            a=rows[i]&rows[j]&~rows[k]
            b=rows[i]&rows[k]&~rows[j]
            d=rows[j]&rows[k]&~rows[i]
            if a and b and d:
                inds=[(v&-v).bit_length()-1 for v in [a,b,d]]+[full]
                small=[[int((rows[u]>>v)&1) for v in inds] for u in [i,j,k]]
                assert small==[[1,1,0,1],[1,0,1,1],[0,1,1,1]]
                return {'rows':[i,j,k],'columns':inds,'matrix':small,'candidates':len(seen)}
    return {'found':False,'candidates':len(seen)}

def main():
    path=Path(__file__).parent/'matroid_certificates/level3_Z_dual_core.sparse'
    rows,cols=read_matrix(path)
    first=search(rows,cols)
    print('Fano',json.dumps(first),flush=True)
    result={'Fano':first}
    if first.get('found') is False:result['Fano_dual']='Not attempted: transpose contains large-degree columns.'
    print(json.dumps(result,indent=2))
    path.with_suffix('.fano.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
