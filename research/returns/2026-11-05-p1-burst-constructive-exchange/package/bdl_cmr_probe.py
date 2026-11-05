"""Use standard CMR, then independently verify any returned graph certificate."""
from pathlib import Path
import json,subprocess
from bdl_matroid_probe import seed,rx,rank_and_relations,relation_columns

def fundamental(columns):
    basis={};chosen=[]
    for index,col in enumerate(columns):
        v=col;c=0
        while v:
            p=v.bit_length()-1
            if p not in basis:
                c^=1<<len(chosen);basis[p]=(v,c);chosen.append(index);break
            b,d=basis[p];v^=b;c^=d
    def coordinates(col):
        v=col;c=0
        while v:
            p=v.bit_length()-1;b,d=basis[p];v^=b;c^=d
        return c
    coords=[coordinates(x) for x in columns]
    assert all(coords[index]==1<<j for j,index in enumerate(chosen))
    rest=[i for i in range(len(columns)) if i not in set(chosen)]
    return chosen,rest,[coords[i] for i in rest]

def probe(rows,labels,prefix):
    rank,rels=rank_and_relations(rows)
    dualcols=relation_columns(rels,len(rows))
    selected,rest,coords=fundamental(dualcols)
    matfile=prefix.with_suffix('.sparse')
    nz=[(i+1,j+1,1) for j,c in enumerate(coords) for i in range(len(selected)) if (c>>i)&1]
    matfile.write_text(f'{len(selected)} {len(rest)} {len(nz)}\n'+'\n'.join(' '.join(map(str,a)) for a in nz)+'\n')
    graphfile=prefix.with_suffix('.graph')
    cmr=Path(__file__).parent/'third_party/cmr/build'
    proc=subprocess.run([str(cmr/'cmr-graphic'),str(matfile),'-i','sparse','-G',str(graphfile),'--time-limit','30'],capture_output=True,text=True)
    prefix.with_suffix('.log').write_text(proc.stdout+proc.stderr)
    result={'physical_rows':len(rows),'physical_rank':rank,'dual_rank':len(rels),'CMR_stdout':proc.stdout,'CMR_stderr':proc.stderr,'CMR_exit':proc.returncode}
    if 'Matrix IS graphic.' in proc.stderr:
        edges=[];vertex_rows={}
        for line in graphfile.read_text().splitlines():
            u,v,label=line.split();index=(selected if label[0]=='r' else rest)[int(label[1:])-1]
            edges.append((u,v,index))
            vertex_rows[u]=vertex_rows.get(u,0)^(1<<index)
            vertex_rows[v]=vertex_rows.get(v,0)^(1<<index)
        grank,_=rank_and_relations(list(vertex_rows.values()))
        joint_rank,_=rank_and_relations(list(vertex_rows.values())+rels)
        assert len(edges)==len(rows) and len({e[2] for e in edges})==len(rows)
        assert grank==joint_rank==len(rels)
        result['exact_graph_certificate']={'verified':True,'rank':grank,'vertices':len(vertex_rows),'edges':len(edges)}
        prefix.with_suffix('.certificate.json').write_text(json.dumps({'vertices':list(vertex_rows),'edges':edges,'physical_check_labels':[repr(x) for x in labels]},indent=2)+'\n')
    else:
        proc2=subprocess.run([str(cmr/'cmr-regular'),str(matfile),'-i','sparse','-D',str(prefix.with_suffix('.decomposition')),'-N',str(prefix.with_suffix('.nonregular')),'--time-limit','30'],capture_output=True,text=True)
        result['CMR_regular']=proc2.stdout+proc2.stderr
    return result

def main():
    t=seed();out=[];folder=Path(__file__).parent/'matroid_certificates';folder.mkdir(exist_ok=True)
    for i in range(3):
        t=rx(t) if i%2==0 else rx(t.dual()).dual()
        hx,hz=t.matrices()
        for tag,rows,labels in [('X',hx,t.X),('Z',hz,t.Z)]:
            result={'level':i+1,'sector':tag,**probe(rows,labels,folder/f'level{i+1}_{tag}_dual')}
            print(json.dumps(result),flush=True);out.append(result)
    (folder/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
