"""Exact deletion/contraction of loops, parallel and series classes before CMR."""
from pathlib import Path
import json,subprocess
from bdl_matroid_probe import rank_and_relations,relation_columns
from bdl_cmr_probe import fundamental

def read_fundamental(path):
    a=list(map(int,path.read_text().split()));r,n,nz=a[:3]
    cols=[1<<i for i in range(r)]+[0]*n
    for k in range(nz):
        i,j,v=a[3+3*k:6+3*k]
        assert v==1;cols[r+j-1]|=1<<(i-1)
    return cols

def simplify(cols,labels):
    seen={};keep=[]
    for i,c in enumerate(cols):
        if c and c not in seen:seen[c]=i;keep.append(i)
    kept=set(keep)
    return [cols[i] for i in keep],[labels[i] for i in keep],[labels[i] for i in range(len(cols)) if i not in kept]

def dual(cols):
    r,rels=rank_and_relations(cols)
    return relation_columns(rels,len(cols))

def write_fundamental(cols,path):
    chosen,rest,cs=fundamental(cols)
    nz=[]
    for j,c in enumerate(cs):
        while c:
            bit=c&-c;nz.append((bit.bit_length(),j+1,1));c^=bit
    path.write_text(f'{len(chosen)} {len(rest)} {len(nz)}\n'+'\n'.join(' '.join(map(str,x)) for x in nz)+'\n')
    return chosen,rest

def main():
    folder=Path(__file__).parent/'matroid_certificates'
    cols=read_fundamental(folder/'level3_Z_dual.sparse');labels=list(range(len(cols)))
    operations=[];sizes=[]
    while True:
        before=len(cols)
        cols,labels,deleted=simplify(cols,labels);operations.append({'delete':deleted})
        dc=dual(cols)
        dc,labels,contracted=simplify(dc,labels);operations.append({'contract':contracted})
        cols=dual(dc)
        r,_=rank_and_relations(cols);sizes.append({'elements':len(cols),'rank':r})
        print(sizes[-1],flush=True)
        if len(cols)==before:break
    path=folder/'level3_Z_dual_core.sparse'
    chosen,rest=write_fundamental(cols,path)
    (folder/'level3_Z_dual_core_reduction.json').write_text(json.dumps({'sizes':sizes,'minor_groundset_labels':labels,'operations':operations,'core_basis':chosen,'core_rest':rest},indent=2)+'\n')
    cmr=Path(__file__).parent/'third_party/cmr/build'
    for typ,extra in [('graphic',[]),('cographic',['-t'])]:
        p=subprocess.run([str(cmr/'cmr-graphic'),str(path),'-i','sparse',*extra,'--time-limit','30'],capture_output=True,text=True)
        print(typ,p.stdout+p.stderr,flush=True)
    p=subprocess.run([str(cmr/'cmr-regular'),str(path),'-i','sparse','-D',str(folder/'level3_Z_dual_core.decomposition'),'-N',str(folder/'level3_Z_dual_core.nonregular'),'--time-limit','45'],capture_output=True,text=True)
    print('regular',p.stdout+p.stderr,flush=True)
    (folder/'level3_Z_dual_core.regular.log').write_text(p.stdout+p.stderr)

if __name__=='__main__':main()
