"""Independent exact review diagnostics; never imports or writes peer files."""
import sys,json,hashlib
from pathlib import Path
from itertools import combinations,product
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from representation_compiler import C,Q,matrix,det

def amplitudes(f,holes):
    remaining=sorted(set(range(len(f)))-set(holes))
    if len(remaining)%2:return []
    result=[]
    for ii in combinations(remaining,len(remaining)//2):
        jj=sorted(set(remaining)-set(ii))
        a=det([[f[i][j] for j in jj] for i in ii])
        if a:result.append(a)
    return result

def weights(f,holes):
    aa=amplitudes(f,holes)
    assert all(a.im==0 for a in aa)
    return sum(a.abs2() for a in aa),sum(abs(a.re) for a in aa)

def matching_vertices(vertices):
    if not vertices:
        yield ()
        return
    first,*rest=vertices
    for matching in matching_vertices(rest):yield matching
    for j in rest:
        for matching in matching_vertices([x for x in rest if x!=j]):
            yield ((first,j),)+matching

def aux_l1(f,holes):
    value=Q(0)
    for mm in matching_vertices(sorted(set(range(6))-set(holes))):
        used={i for edge in mm for i in edge}
        value+=Q(1,100)**len(mm)*weights(f,set(holes)|used)[1]
    return value

def main():
    f1=matrix([[0,-1,-1,-1,0,0],[0,0,0,0,0,0],[1,0,0,0,0,0],
               [0,0,0,0,0,0],[0,0,-1,-1,0,0],[0,-1,-1,0,0,0]])
    f2=matrix([[0,0,0,0,0,0],[0,0,1,1,0,0],[-1,0,0,0,-1,0],
               [1,0,0,0,-1,0],[0,0,0,0,0,0],[0,0,-1,1,0,0]])
    s,t,a=set(),{1,3,4,5},1
    assert sorted(abs(x.re) for x in amplitudes(f1,s))==[1,1]
    assert sorted(abs(x.re) for x in amplitudes(f1,t))==[1,1]
    terms=[]
    for j in (3,4,5):
        left=amplitudes(f1,s^{a,j});right=amplitudes(f1,t^{a,j})
        terms.append([sorted(abs(x.re) for x in left),sorted(abs(x.re) for x in right)])
    assert terms==[[[],[]],[[1],[1]],[[1],[1]]]
    s2,t2,a2={0,4},{1,5},0
    assert [sorted(abs(x.re) for x in amplitudes(f2,u)) for u in (s2,t2)]==[[2],[2]]
    terms2=[]
    for j in (1,4,5):
        terms2.append([sorted(abs(x.re) for x in amplitudes(f2,u^{a2,j})) for u in (s2,t2)])
    assert terms2==[[[1,1],[1,1]],[[],[]],[[1,1],[1,1]]]
    assert len(list(matching_vertices(list(range(6)))))==76
    auxleft=aux_l1(f1,s)*aux_l1(f1,t)
    auxright=sum(aux_l1(f1,s^{a,j})*aux_l1(f1,t^{a,j}) for j in (3,4,5))
    assert auxleft==Q(84115083,20000000) and auxright==Q(218697827,100000000)
    same1=matrix([[0,0,-1,1],[-1,1,-1,1],[0,-1,1,0],[-1,0,1,-1]])
    same2=matrix([[-1,0,-1,1],[-1,1,-1,0],[0,1,-1,-1],[-1,1,0,1]])
    for mask in range(16):
        holes={i for i in range(4) if (mask>>i)&1}
        assert weights(same1,holes)[0]==weights(same2,holes)[0]
    assert weights(same1,set())==(6,4) and weights(same2,set())==(6,6)
    weak=[]
    for bits in (2,6,10):
        u=Q(1,1<<bits);c=(1-u*u)/(1+u*u);sine=2*u/(1+u*u)
        f=matrix([[0,-1,0,0],[1,0,0,0],[0,0,c,-sine],[0,0,sine,c]])
        assert all(sum(f[i][k]*f[j][k].conjugate() for k in range(4))==C(i==j) for i in range(4) for j in range(4))
        z=weights(f,set())[0]
        assert z==4*sine*sine
        assert weights(f,{0,1})[0]/z==Q(1,2)
        assert weights(f,{2,3})[0]/z==1/(2*sine*sine)
        v=[[C(i==j) for j in range(4)]+[f[j][i] for j in range(4)] for i in range(4)]
        vals=[]
        for signs in product((-1,1),repeat=4):
            b=[[sum(v[i][col]*v[j][col].conjugate()*signs[col%4] for col in range(8)) for j in range(4)] for i in range(4)]
            x=det(b);assert x.im==0;vals.append(x.re)
        assert sum(vals)/16==z
        assert sum(abs(x) for x in vals)/abs(sum(vals))==(1+c*c)/(sine*sine)
        assert sum(x*x for x in vals)/16==64*(1+c**4)
        weak.append({'L':bits,'norm':str(z),'largest_ratio':str(1/(2*sine*sine))})
    zero=matrix([[0,1,0,0],[0,0,0,1],[0,0,0,1],[0,0,0,0]])
    two=matrix([[0,1,1,0],[0,0,0,0],[0,0,0,0],[0,-1,1,0]])
    evenmasks=(0,3,5,6,9,10,12,15)
    tables=[]
    for f,expected in ((zero,(1,1,1,0,0,0,1,1)),(two,(4,1,1,0,0,1,1,1))):
        got=tuple(weights(f,{i for i in range(4) if mask>>i&1})[0] for mask in evenmasks)
        assert got==expected;tables.append([str(x) for x in got])
    output={'status':'PASS','checks':{'L03_two_Lp_fixtures':2,'L03_positive_auxiliary_L1':1,
        'L03_entropy_all_hole_coefficients':16,'L06_weak_block_sign_enumerations':3,
        'L09_exact_equality_fixtures':2},'weak_blocks':weak,'L09_tables':tables,
        'scope':'finite exact diagnostics; universal proof arguments reviewed separately'}
    target=Path(__file__).with_name('independent_luna_checks.json')
    target.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output))

if __name__=='__main__':main()
