"""Exact independent GF(2) verification of the BDL wheel-minor packing.

This verifies the local wheel directly in the literal BDL ell=3 cellular
construction at level 3, projects the inherited relation columns onto three
independent (s_z, a_q) pairs, and checks that the final local algebra produces
a direct sum of Fano matroids. The all-ell bridge and asymptotic packing are
proved in p1_comparator.md; the script does not simulate an enormous device.
"""
from collections import defaultdict
from pathlib import Path
import json
from bdl_matroid_probe import seed,rx,canonical_edge,rank_and_relations
from rx_relations import rx_Z_relations

EDGES=[('A','B'),('A','C'),('B','C'),('A','D'),('B','E'),('C','D'),('C','E'),('D','E')]
D_EXPECT=[0,1,0,1,0,3,2,2] # w=1,u=2

def main():
    old=rx(rx(seed()).dual()).dual()
    new=rx(old)
    qzs=defaultdict(set)
    for q,z in old.qz:qzs[q].add(z)
    chosen=[];used=set()
    for x,q,z,r in old.faces:
        if len(qzs[q])<2:
            q,r=r,q
        if len(qzs[q])<2:continue
        vertices={('X',x),('Q',q),('Z',z),('Q',r)}
        if used & vertices:continue
        chosen.append((x,q,z,r));used|=vertices
        if len(chosen)==3:break
    assert len(chosen)==3
    names,relations=rx_Z_relations(old)
    param_image=[0]*len(names)
    chosen_q={q:(i,z,sorted(qzs[q]-{z},key=repr)[0]) for i,(x,q,z,r) in enumerate(chosen)}
    chosen_z={z:i for i,(x,q,z,r) in enumerate(chosen)}
    for j,name in enumerate(names):
        if name[0]=='s' and name[1] in chosen_z:
            param_image[j]=2<<(2*chosen_z[name[1]])
        elif name[0]=='a' and name[1] in chosen_q:
            i,z,zref=chosen_q[name[1]]
            if name[2] in (z,zref):param_image[j]=1<<(2*i)
    def project(v):
        ans=0
        while v:
            b=v&-v;ans^=param_image[b.bit_length()-1];v^=b
        return ans
    face_by_vertex=defaultdict(list)
    for f in new.faces:face_by_vertex[f[0]].append(f)
    reports=[]
    for j,(x,q,z,r) in enumerate(chosen):
        u=('XV',x,(('z',z),0))
        qe=lambda a,b: ('XE',x,canonical_edge(a,b))
        qq=lambda a: ('QV',a,(('z',z),0))
        vertices={
          'A':qe((('q',q),0),(('z',z),0)),
          'B':qe((('q',r),0),(('z',z),0)),
          'C':qe((('z',z),0),(('z',z),1)),
          'D':qq(q),'E':qq(r)}
        inv={v:k for k,v in vertices.items()}
        actual={}
        for xx,qa,zz,qb in face_by_vertex[u]:
            edge=tuple(sorted((inv[qa],inv[qb])))
            assert edge not in actual
            actual[edge]=zz
        assert set(actual)==set(EDGES)
        vals=[project(relations[actual[e]])>>(2*j) for e in EDGES]
        assert vals==D_EXPECT
        assert all(project(relations[actual[e]])==v<<(2*j) for e,v in zip(EDGES,vals))
        reports.append({'wheel':j,'source_face':repr((x,q,z,r)),
                        'wheel_vertex':repr(u),'inherited_patterns':vals,
                        'actual_check_labels':{''.join(e):repr(actual[e]) for e in EDGES}})
    # An independent symbolic cycle parametrization of the five-vertex wheel.
    # x=F_AB, y=F_AC, z=F_BC, t=F_DE; F_AD=x+y etc.
    F=[1,2,4,3,5,11,13,8]
    for v in 'ABCDE':
        val=0
        for edge,f in zip(EDGES,F):
            if v in edge:val^=f
        assert val==0
    blocks=[]
    for j in range(3):
        # After contracting u+w, F_AC=y, F_BC=z, leave x,t,w.
        # Retain D_w, F_AB, (F_AD+d_AD), F_CD, (F_CE+d_CE),
        # F_DE, and (F_DE+d_DE).
        block=[4,1,5,3,7,2,6]
        assert set(block)==set(range(1,8))
        blocks.extend(v<<(3*j) for v in block)
    rank,_=rank_and_relations(blocks)
    assert rank==9
    assert all((v.bit_length()-1)//3==j for j in range(3) for v in blocks[7*j:7*j+7])
    out={'literal_coarse_level':2,'literal_coarse_qubits':len(old.Q),
         'checked_RX_qubits':len(new.Q),'independent_wheels':3,
         'wheel_edges':[''.join(e) for e in EDGES],
         'wheel_cycle_coordinates':F,'inherited_patterns':D_EXPECT,
         'final_Fano_columns_per_block':[4,1,5,3,7,2,6],
         'direct_sum_rank':rank,'all_exact_checks_passed':True,'wheels':reports}
    path=Path(__file__).parent/'matroid_certificates/wheel_packing_verification.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='wheels'},indent=2))
if __name__=='__main__':main()
