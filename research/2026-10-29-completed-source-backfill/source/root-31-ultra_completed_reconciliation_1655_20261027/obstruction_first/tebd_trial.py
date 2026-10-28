"""Ordinary U(1)-resolved infinite TEBD acquires a two-site MPS trial.

Vidal's infinite-TEBD algorithm is an established variational-search baseline.
No truncation error is used to claim a gap, a spectral tail, or finite-ring
energy. Exact finite contractions must check the final quantized tensors.
"""
from __future__ import annotations
import pathlib,sys,time,json,math,argparse
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'sol6_openings_20261027/positive_current_operation/vendor'))
import numpy as np
from scipy.linalg import eigh,svd,eig
ROOT=pathlib.Path(__file__).resolve().parent
weights=np.arange(-2,3)


def gate(dt):
    sz=np.diag(weights);sp=np.diag(np.sqrt([4,6,6,4]),-1);sm=sp.T
    h=np.kron(sz,sz)+.5*(np.kron(sp,sm)+np.kron(sm,sp));e,u=eigh(h)
    return ((u*np.exp(-dt*e))@u.T).reshape(5,5,5,5)


def update(a,b,middle,outer,qouter,chi,g):
    theta=np.einsum('i,isc,c,ctj,j->istj',outer,a,middle,b,outer,optimize=True)
    theta=np.einsum('stuv,iuvj->istj',g,theta,optimize=True)
    mat=theta.reshape(len(outer)*5,5*len(outer))
    qr=(qouter[:,None]+weights[None,:]).reshape(-1)
    qc=(qouter[None,:]-weights[:,None]).reshape(-1)
    pieces=[]
    for charge in sorted(set(qr)&set(qc)):
        ir=np.flatnonzero(qr==charge);ic=np.flatnonzero(qc==charge)
        u,s,v=svd(mat[np.ix_(ir,ic)],full_matrices=False,check_finite=False)
        for j,x in enumerate(s):
            if x>1e-15:pieces.append((float(x),int(charge),ir,ic,u[:,j],v[j,:]))
    pieces=sorted(pieces,key=lambda z:-z[0])[:chi];pieces.sort(key=lambda z:(z[1],-z[0]))
    new=np.array([x[0]for x in pieces]);new/=np.linalg.norm(new)
    qnew=np.array([x[1]for x in pieces],int);u=np.zeros((len(outer)*5,len(pieces)));v=np.zeros((len(pieces),5*len(outer)))
    for j,x in enumerate(pieces):u[x[2],j]=x[4];v[j,x[3]]=x[5]
    anew=u.reshape(len(outer),5,len(pieces))/outer[:,None,None]
    bnew=v.reshape(len(pieces),5,len(outer))/outer[None,None,:]
    return anew,bnew,new,qnew


def restricted_kron(b,c,left,right):
    i,j=np.array(left).T;k,l=np.array(right).T
    return b[i[:,None],k[None,:]]*c[j[:,None],l[None,:]]


def local_energy(a,b,qa,qb):
    # A has left qA, right qB; B reverses these bond labels.
    pa=[(i,j)for i,x in enumerate(qa)for j,y in enumerate(qa)if x==y]
    pb=[(i,j)for i,x in enumerate(qb)for j,y in enumerate(qb)if x==y]
    ea=sum(restricted_kron(a[:,s,:],a[:,s,:],pa,pb)for s in range(5))
    eb=sum(restricted_kron(b[:,s,:],b[:,s,:],pb,pa)for s in range(5))
    transfer=ea@eb
    ev,left,right=eig(transfer,left=True,right=True);i=int(np.argmax(ev.real));lam=float(ev[i].real);lv=left[:,i].real;rv=right[:,i].real
    norm=float(lv@rv)
    blocks={(s,t):a[:,s+2,:]@b[:,t+2,:]for s in range(-2,3)for t in range(-2,3)}
    op=np.zeros_like(transfer)
    for s in range(-2,3):
        for t in range(-2,3):
            x=blocks[s,t];op+=s*t*restricted_kron(x,x,pa,pa)
            if s<2 and t>-2:
                y=blocks[s+1,t-1];hop=.5*math.sqrt((6-s*(s+1))*(6-t*(t-1)))
                op+=hop*(restricted_kron(x,y,pa,pa)+restricted_kron(y,x,pa,pa))
    return float(lv@op@rv/(lam*norm)),lam,len(pa)


def run(chi,output):
    a=np.zeros((1,5,1));b=np.zeros_like(a);a[0,4,0]=1;b[0,0,0]=1
    la=np.ones(1);lb=np.ones(1);qa=np.array([2]);qb=np.array([0])
    history=[];start=time.monotonic()
    schedule=[(.2,300),(.1,300),(.05,300),(.02,400),(.01,500),(.005,500),(.002,600),(.001,600)]
    for dt,steps in schedule:
        g=gate(dt)
        for _ in range(steps):
            a,b,la,qa=update(a,b,la,lb,qb,chi,g)
            b,a,lb,qb=update(b,a,lb,la,qa,chi,g)
        aa=a*la[None,None,:];bb=b*lb[None,None,:]
        eab,lam,block=local_energy(aa,bb,qb,qa);eba,_,_=local_energy(bb,aa,qa,qb)
        row={'dt':dt,'steps':steps,'energy_AB':eab,'energy_BA':eba,'energy_average':(eab+eba)/2,'norm_transfer':lam,'difference_zero_block':block,'seconds':time.monotonic()-start}
        history.append(row);print(row,flush=True)
        result={'status':'FLOATING_VARIATIONAL_SEARCH_NOT_FINITE_RING_CERTIFICATE','algorithm':'ordinary infinite TEBD with U(1) blocks','chi_cap':chi,'A':aa.tolist(),'B':bb.tolist(),'charges_A_left':qb.tolist(),'charges_A_right':qa.tolist(),'history':history,'seconds':time.monotonic()-start}
        pathlib.Path(output).write_text(json.dumps(result,indent=2))
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--chi',type=int,default=32);ap.add_argument('--output',required=True);x=ap.parse_args();run(x.chi,x.output)
