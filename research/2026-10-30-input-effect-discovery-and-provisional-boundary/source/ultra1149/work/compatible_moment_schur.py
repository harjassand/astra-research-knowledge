"""Exact compatible-gradient Schur operation, with a real witness on failure.

Sine modes represent an actual periodic map. Passing a shape certifies all
its means and amplitudes, never all gradient fields or global QC.
"""
from fractions import Fraction as R
from pathlib import Path
import importlib.util,json,math
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('core',root/'outputs/hopf_structure/receive.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
def add(*ps):
    ans={}
    for p in ps:
        for e,c in p.items():ans[e]=ans.get(e,R(0))+c
    return {e:c for e,c in ans.items() if c}
def scale(p,c):return {e:v*c for e,v in p.items() if v*c}
def mul(p,q):
    ans={}
    for e,c in p.items():
        for f,d in q.items():
            ee=tuple(a+b for a,b in zip(e,f));ans[ee]=ans.get(ee,R(0))+c*d
    return {e:c for e,c in ans.items() if c}
def substitute(poly,values):
    ans={}
    for powers,co in poly.items():
        term={(0,0):co}
        for v,e in zip(values,powers):
            for _ in range(e):term=mul(term,v)
        ans=add(ans,term)
    return ans
def average(poly,G):return substitute(poly,G).get((0,0),R(0))
def gradient(modes):
    G=[{} for _ in range(4)]
    for mode in modes:
        k=tuple(mode['frequency']);v=list(map(R,mode['sine']))
        assert len(k)==2 and all(isinstance(x,int) for x in k) and k!=(0,0)
        for i in range(2):
            for j in range(2):G[2*i+j]=add(G[2*i+j],{k:v[i]*k[j]/2,tuple(-n for n in k):v[i]*k[j]/2})
    assert all(g.get((0,0),0)==0 for g in G)
    return G
def linear_solve(matrix,rhs):
    n=len(matrix);a=[list(row)+[rhs[i]] for i,row in enumerate(matrix)]
    for j in range(n):
        i=next(i for i in range(j,n) if a[i][j]);a[j],a[i]=a[i],a[j];pivot=a[j][j];a[j]=[z/pivot for z in a[j]]
        for i in range(n):
            if i!=j:
                co=a[i][j];a[i]=[x-co*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),R(0))
def support(H):
    selected=[]
    for i in range(len(H)):
        new=selected+[i];mat=[[H[j][k] for k in new] for j in new]
        if core.rank(mat)==len(new):core.pd(mat);selected=new
    return selected
def shape_operation(F,C,Q,modes):
    G=gradient(modes);H=[[average(core.diff(core.diff(F,i),j),G) for j in range(4)] for i in range(4)]
    v=[average(core.diff(F,i),G) for i in range(4)];w=[average(core.diff(C,i),G) for i in range(4)]
    f,c,q=[average(p,G) for p in (F,C,Q)];I=support(H);HII=[[H[i][j] for j in I] for i in I]
    def solve(rhs):
        sol=linear_solve(HII,[rhs[i] for i in I]);ans=[R(0)]*4
        for i,z in zip(I,sol):ans[i]=z
        residual=[rhs[i]-dot(H[i],ans) for i in range(4)]
        return ans,residual
    sv,rv=solve(v);sw,rw=solve(w)
    assert not any(rv),'The acquired leading quartic would fail this compatible field'
    a=2*f-dot(v,sv);bb=2*q-dot(w,sw);r=c-dot(v,sw);assert a>=0
    result={'H_rank':len(I),'a':str(a),'b':str(bb),'r':str(r),
      'correlation_determinant':str(a*bb-r*r),'scope':'This exact compatible field at all means and amplitudes; not global QC.'}
    if any(rw):
        # A residual to the supported solution need not itself be in ker H.
        # Select a coordinate outside I and explicitly construct a null vector.
        for j in range(4):
            if j in I:continue
            coefficients=linear_solve(HII,[H[i][j] for i in I]);k=[R(0)]*4;k[j]=1
            for i,z in zip(I,coefficients):k[i]=-z
            if dot(k,w):break
        assert all(dot(row,k)==0 for row in H) and dot(k,w)
        rho=R(1);s=-(f+c+q+1)/dot(k,w);M=[s*z for z in k]
    elif bb<0:
        rho=R(-1 if r>0 else 1)
        while a*rho*rho+2*r*rho+bb>=0:rho/=2
        M=[-rho*x-y for x,y in zip(sv,sw)]
    elif a*bb-r*r<0:
        rho=-r/a if a else -(bb+1)/(2*r);M=[-rho*x-y for x,y in zip(sv,sw)]
    else:
        result['all_means_and_amplitudes_nonnegative_for_this_shape']=True
        return result
    AG=[add({(0,0):m},scale(g,rho)) for m,g in zip(M,G)]
    P=core.add(F,C,Q);actual=substitute(P,AG).get((0,0),R(0))-core.evaluate(P,M)
    assert actual<0
    result.update({'all_means_and_amplitudes_nonnegative_for_this_shape':False,
      'witness_mean':list(map(str,M)),'witness_amplitude':str(rho),'actual_energy_gap':str(actual),'modes':modes})
    return result
def acquired():
    raw=json.loads((root/'work/actual_boundary.json').read_text());gd=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text())
    F={tuple(row[:4]):R(row[4],row[5]) for row in raw['F']};C={tuple(pw):R(co) for pw,co in zip(gd['cubic_powers'],gd['example_cubic_coefficients']) if R(co)}
    T={tuple(2*int(i==j) for i in range(4)):R(1) for j in range(4)}
    return F,C,T
if __name__=='__main__':
    F,C,T=acquired();modes=[{'frequency':[1,0],'sine':['1','0']},{'frequency':[0,1],'sine':['0','1']},{'frequency':[1,1],'sine':['1','1']}]
    answer=shape_operation(F,C,scale(T,R(1859)),modes)
    print(json.dumps(answer,indent=2))
