"""Finite periodic two-site MPS norm/energy contractions.

For integer A_s,B_s the norm V and the two energy coefficients U0,U1 are
arbitrary-precision integers, and energy per bond=(U0+sqrt(6)*U1)/(2V).
U(1) difference blocks are exhaustive, not a truncation. The exact four-site
computational-basis replay checks the contraction independently.
"""
import pathlib,sys,json,time,argparse,math
from fractions import Fraction
import tebd_trial as tebd
import numpy as np
import mpmath as mp
mp.iv.dps=80
iv=mp.iv
ROOT=pathlib.Path(__file__).resolve().parent

def lower(x):return math.nextafter(float(x.a),-math.inf)
def upper(x):return math.nextafter(float(x.b),math.inf)
def tp(a,b):return np.sum(a*b.T)


def operators(a,b,pa,pb):
    ea=sum(tebd.restricted_kron(a[:,s,:],a[:,s,:],pa,pb)for s in range(5))
    eb=sum(tebd.restricted_kron(b[:,s,:],b[:,s,:],pb,pa)for s in range(5))
    bs={(s,t):a[:,s+2,:]@b[:,t+2,:]for s in range(-2,3)for t in range(-2,3)}
    z=np.zeros((len(pa),len(pa)),dtype=a.dtype);o0=z.copy();o1=z.copy()
    for s in range(-2,3):
        for t in range(-2,3):
            x=bs[s,t];o0+=s*t*tebd.restricted_kron(x,x,pa,pa)
            if s<2 and t>-2:
                y=bs[s+1,t-1];sq=(6-s*(s+1))*(6-t*(t-1))
                term=tebd.restricted_kron(x,y,pa,pa)+tebd.restricted_kron(y,x,pa,pa)
                if sq==24:o1+=term
                else:
                    assert sq in (16,36);o0+=(2 if sq==16 else 3)*term
    return ea,eb,o0,o1


def tensors(path,exact=False,scale=10**8):
    j=json.loads(pathlib.Path(path).read_text());a=np.array(j['A']);b=np.array(j['B']);qa=np.array(j['charges_A_left']);qb=np.array(j['charges_A_right'])
    ai=np.rint(scale*a).astype(np.int64);bi=np.rint(scale*b).astype(np.int64)
    for i,q in enumerate(qa):
        for s in range(-2,3):
            for k,r in enumerate(qb):
                if r!=q+s:assert ai[i,s+2,k]==0
                if q!=r+s:assert bi[k,s+2,i]==0
    if exact:return ai.astype(object),bi.astype(object),qa,qb
    return ai.astype(float)/scale,bi.astype(float)/scale,qa,qb


def contract(a,b,qa,qb,n,verbose=False):
    assert n>=4 and n%2==0
    exact=a.dtype==object;v=0;u0=0;u1=0;dims=[];start=time.monotonic()
    differences=sorted(set(int(x-y)for x in qa for y in qa)|set(int(x-y)for x in qb for y in qb))
    for diff in differences:
        pa=[(i,j)for i,x in enumerate(qa)for j,y in enumerate(qa)if x-y==diff];pb=[(i,j)for i,x in enumerate(qb)for j,y in enumerate(qb)if x-y==diff]
        if not pa or not pb:continue
        ea,eb,oab0,oab1=operators(a,b,pa,pb);_,_,oba0,oba1=operators(b,a,pb,pa)
        t=ea@eb;p=np.linalg.matrix_power(t,n//2-2);pab=p@t;pba=(eb@p)@ea
        vv=tp(pab,t);uv0=tp(pab,oab0)+tp(pba,oba0);uv1=tp(pab,oab1)+tp(pba,oba1)
        v+=vv;u0+=uv0;u1+=uv1;dims.append([diff,len(pa),len(pb)])
        if verbose:print('block',n,diff,len(pa),len(pb),'seconds',time.monotonic()-start,flush=True)
    if exact:
        assert isinstance(v,int) and v>0
        energy=(iv.mpf(int(u0))+iv.sqrt(6)*int(u1))/(2*int(v))
        return {'n':n,'V':str(v),'U0':str(u0),'U1':str(u1),'energy_per_bond_lower':lower(energy),'energy_per_bond_upper':upper(energy),'blocks':dims,'seconds':time.monotonic()-start}
    energy=(u0+np.sqrt(6)*u1)/(2*v)
    return {'n':n,'energy_per_bond':float(energy),'norm':float(v),'blocks':dims,'seconds':time.monotonic()-start}


def direct_four_site(a,b,qa,qb):
    import spin_chain as sc
    h,codes,h0,h1=sc.sector(4,0)
    vec=[]
    for code in codes:
        s=[(int(code)//5**j)%5 for j in range(4)]
        vec.append(int(np.trace(a[:,s[0],:]@b[:,s[1],:]@a[:,s[2],:]@b[:,s[3],:])) )
    v=np.array(vec,dtype=object);norm=sum(x*x for x in vec);u=[]
    for hc in [h0,h1]:
        result=0;co=hc.tocoo()
        for r,c,x in zip(co.row,co.col,co.data):result+=int(x)*vec[r]*vec[c]
        u.append(result)
    replay=contract(a,b,qa,qb,4)
    assert norm==int(replay['V'])
    assert u[0]==2*int(replay['U0']) and u[1]==2*int(replay['U1'])
    return {'status':'EXACT_COMPUTATIONAL_BASIS_MATCH','n':4,'norm':str(norm),'energy_numerator_0':str(u[0]),'energy_numerator_1':str(u[1])}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--n',type=int,default=32);ap.add_argument('--exact',action='store_true');ap.add_argument('--output',required=True);args=ap.parse_args()
    a,b,qa,qb=tensors(args.input,args.exact)
    if args.exact:
        result=contract(a,b,qa,qb,args.n,True);result['status']='EXACT_INTEGER_FINITE_RING_VARIATIONAL_CONTRACTION';result['source_tensor_file']=args.input;result['quantization_scale']=10**8
        # The four-site replay uses the same exact tensors and an independent
        # physical-Hamiltonian implementation.
        result['independent_four_site_check']=direct_four_site(a,b,qa,qb)
    else:result={'status':'FLOATING_FINITE_RING_DIAGNOSTIC','runs':[contract(a,b,qa,qb,n)for n in [16,32,64,128,256]]}
    pathlib.Path(args.output).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items()if k not in ['V','U0','U1','independent_four_site_check']},indent=2))
