"""Literal sparse p/F/h verification, independent of proposed closed words.

The all-level proof is in RETRACTION_PROOF.md. This checks every linear map
identity on all columns of the two actual finite replacement inputs already
compiled, not a sampling test or an extra recursive level.
"""
from pathlib import Path
from collections import deque
import json,time
from compile_complex import *


def xor(xs):
    a=0
    for x in xs:a^=x
    return a


def compose(A,B):return [xor(B[j] for j in bits(a)) for a in A]


def add(*matrices):return [xor(x) for x in zip(*matrices)]


def unit(n):return [1<<i for i in range(n)]


def combo_basis(pairs):
    out={}
    for x,c in pairs:
        while x:
            p=x.bit_length()-1
            if p in out:x^=out[p][0];c^=out[p][1]
            else:out[p]=(x,c);break
    return out


def solve(x,b):
    c=0
    while x:
        p=x.bit_length()-1
        assert p in b, 'local face/edge filling failed'
        row,comb=b[p];x^=row;c^=comb
    return c


def build(old,ell):
    fine,d=rx(old,ell,True);t=d['t'];retractions=[]
    F0=[1<<x for x,v in d['xv']]
    F1=[0]*len(d['xe'])+[1<<q for q,v in d['qv']]
    F2=[0]*(len(d['xf'])+len(d['qe']))+[1<<z for z,s in d['zp']]
    do0=transpose(old.xs,old.n);df0=transpose(fine.xs,fine.n)
    assert compose(df0,F0)==compose(F1,do0)
    assert compose(fine.zs,F1)==compose(F2,old.zs)
    idq=d['id_qv'];idxe=d['id_xe'];idxv=d['id_xv']
    for layer in (0,1):
        p0=[];h1=[0]*len(d['xv'])
        for x,(vs,es,fs) in enumerate(d['localx']):
            root=(layer,('v',('x',x)))
            p0.append(1<<idxv[x,root]);paths={root:0}
            # Prescribed disjoint x--q rays form a tree, so can be extended.
            for q in d['xq'][x]:
                ray=edge_subdivision(('x',x),('q',q),t)
                if ray[0]!=('v',('x',x)):ray.reverse()
                ray=[(layer,v) for v in ray]
                for a,b in zip(ray,ray[1:]):
                    assert a in paths
                    value=paths[a]^(1<<idxe[x,ordered(a,b)])
                    if b in paths:assert paths[b]==value
                    else:paths[b]=value
            adj={v:[] for v in vs}
            for a,b in es:adj[a].append(b);adj[b].append(a)
            todo=deque(paths)
            while todo:
                a=todo.popleft()
                for b in adj[a]:
                    if b not in paths:
                        paths[b]=paths[a]^(1<<idxe[x,ordered(a,b)]);todo.append(b)
            assert len(paths)==len(vs)
            for v,path in paths.items():h1[idxv[x,v]]=path
        p1=[]
        for q in range(old.n):
            v=(layer,('v',('q',q)))
            p1.append((1<<idq[q,v])^xor(h1[idxv[x,v]] for x in range(len(old.xs)) if (old.xs[x]>>q)&1))
        p2=[]
        for z in range(len(old.zs)):
            row=1<<d['id_zp'][z,layer]
            for q in bits(old.zs[z]):
                ray=edge_subdivision(('q',q),('z',z),t)
                for a,b in zip(ray,ray[1:]):
                    row^=1<<d['id_qe'][q,ordered((layer,a),(layer,b))]
            for fi,face in enumerate(old.faces):
                if face[2]!=z:continue
                x=face[0]
                grid={(i,j):subdivided_vertex(face,i,j,t,fi) for i in range(t+1) for j in range(t+1)}
                for i in range(t):
                    for j in range(t):
                        f=tuple((layer,v) for v in (grid[i,j],grid[i+1,j],grid[i+1,j+1],grid[i,j+1]))
                        row^=1<<d['id_xf'][x,f]
            p2.append(row)
        assert compose(p0,F0)==unit(len(old.xs))
        assert compose(p1,F1)==unit(old.n)
        assert compose(p2,F2)==unit(len(old.zs))
        assert compose(p1,df0)==compose(do0,p0)
        assert compose(p2,fine.zs)==compose(old.zs,p1)
        E=add(unit(fine.n),compose(F1,p1),compose(df0,h1))
        # Local fillings use only faces of the affected X block, or Q edges
        # and the X faces of the at most D neighbouring X blocks.
        bx={}
        for x in range(len(old.xs)):
            ids=[zi for (xx,f),zi in d['id_xf'].items() if xx==x]
            bx[x]=combo_basis((fine.zs[zi],1<<zi) for zi in ids)
        bq={}
        for q in range(old.n):
            xs={x for x in range(len(old.xs)) if (old.xs[x]>>q)&1}
            ids=[zi for (x,f),zi in d['id_xf'].items() if x in xs]
            ids += [zi for (qq,e),zi in d['id_qe'].items() if qq==q]
            bq[q]=combo_basis((fine.zs[zi],1<<zi) for zi in ids)
        h2=[]
        for j,(x,e) in enumerate(d['xe']):h2.append(solve(E[j],bx[x]))
        for j,(q,v) in enumerate(d['qv'],start=len(d['xe'])):h2.append(solve(E[j],bq[q]))
        assert compose(h2,fine.zs)==E
        # The all-vector degree-one homotopy, with no cocycle assumption.
        assert add(compose(F1,p1),compose(df0,h1),compose(h2,fine.zs))==unit(fine.n)
        retractions.append(dict(p0=p0,p1=p1,p2=p2,h1=h1,h2=h2))
    used=0
    for pp in retractions:
        for r in pp['p1']:
            assert not used&r,'p rows/layers are not coordinate-disjoint'
            used|=r
    D=7;F=28;V=2*F*(t+1)**2;Fx=2*F*t*(t+1);Eq=D*(2*t+1)
    A=max(V,1+D*t+F*t*t,Eq+D*Fx)
    stats=[]
    for layer,r in enumerate(retractions):
        hcol=transpose(r['h1'],fine.n)
        stat={'layer':layer,'p1_selected_coordinates':sum(x.bit_count() for x in r['p1']),
              'p1_max_column_weight':max(map(int.bit_count,transpose(r['p1'],fine.n))),
              'F0_max_column_weight':max(map(int.bit_count,transpose(F0,len(old.xs)))),
              'h1_max_column_weight':max(map(int.bit_count,hcol)),
              'p2_max_row_weight':max(map(int.bit_count,r['p2'])),
              'h2_max_row_weight':max(map(int.bit_count,r['h2']))}
        assert max(stat[x] for x in ('F0_max_column_weight','h1_max_column_weight','p2_max_row_weight','h2_max_row_weight'))<=A
        stats.append(stat)
    return {'input_n':old.n,'output_n':fine.n,'ell':ell,'literal_all_vector_identities':'PASS',
            'disjoint_projection_coordinates':'PASS','uniform_analytic_A':A,
            'uniform_parameters':{'D':D,'F_star':F,'V_star':V,'F_x_star':Fx,'E_q_star':Eq},
            'layer_costs':stats,'dimensions':fine.qualify()}


def main():
    p=Path(__file__).parent;t0=time.perf_counter()
    first=seed();second=load(p/'complexes'/'level_1.json').dual()
    reports=[build(first,3),build(second,3)]
    result={'reports':reports,'wall_seconds':time.perf_counter()-t0,
            'scope':'Exact all-vector GF(2) p/F/h identities for the already acquired RX and dual-RX inputs. All-level theorem and primary geometric/stability imports are separate.'}
    (p/'RETRACTION_EXECUTION.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
