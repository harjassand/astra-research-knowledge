from pathlib import Path
import json
import numpy as np
P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
def star_unitary(n,t):
    d=2**(n+1);u=np.eye(d,dtype=complex);ids=np.arange(d)
    for j in range(1,n+1):
        a=n;b=n-j;mask=((ids>>a)^(ids>>b))&1;perm=ids^(mask<<a)^(mask<<b)
        u=np.cos(t)*u+1j*np.sin(t)*u[perm,:]
    return u
def bath_ops(n,t):
    d=2**n;u=star_unitary(n,t);bs=[]
    for p in P:
        jj=u@np.kron(p,np.eye(d))@u.conj().T
        bs.append((jj[:d,:d]+jj[d:,d:])/2)
    return bs
def lie_dim(gens,tol=1e-9):
    d=len(gens[0]);bas=[]
    def add(a):
        a=(a+a.conj().T)/2;a-=np.trace(a)*np.eye(d)/d
        nv=np.linalg.norm(a)
        if nv<1e-13:return
        a=a/nv
        for _ in range(2):
            for b in bas:a-=np.vdot(b,a).real*b
        norm=np.linalg.norm(a)
        if norm>tol:bas.append(a/norm)
    for a in gens:add(a)
    cursor=0
    while cursor<len(bas):
        a=bas[cursor]
        for g in gens:add(1j*(a@g-g@a))
        cursor+=1
        if len(bas)>=d*d-1:break
    return len(bas)
def main():
    rows=[]
    for n in range(1,5):
        t=.6;bs=bath_ops(n,t);z=np.linalg.eigvalsh(bs[2])
        row={'n':n,'theta':t,'lie_dimension':lie_dim(bs),'z_spectrum':z.tolist(),
             'allup_signal':float(bs[2][0,0].real),'expected_allup':1-np.cos(t)**(2*n),
             'gram':float(np.trace(bs[0]@bs[0]).real/2**n),'known_gram':1-(1-np.sin(t)**4)**n}
        if n<=3:
            d=2**n;u=star_unitary(n,t);ks=[u[a*d:(a+1)*d,b*d:(b+1)*d]/np.sqrt(2) for a in range(2) for b in range(2)]
            sup=sum(np.kron(k.conj(),k) for k in ks);sv=np.linalg.svd(sup,compute_uv=False)
            row['bath_channel_singular_values']=sv.tolist()
        rows.append(row);print(json.dumps(row))
    Path(__file__).with_name('operator_structure.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
