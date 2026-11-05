#!/usr/bin/env python3
"""Terminal-Bell control starting from the independently pure matched cascade."""
from rotor_control import *


def cascade_setup(k,theta,frame,solver,tol):
    mem=spin_rep(.5)
    for _ in range(k-1):mem=tensor_rep(mem,spin_rep(.5))
    inp=tensor_rep(mem,spin_rep(.5));m=1<<k
    chan=RepChannel(inp,mem,[.5],solver,tol);dec=UnrestrictedDecoder(m,solver,tol);model=CollisionModel(m,theta)
    z=np.array([1,0],complex);x=np.array([1,1],complex)/np.sqrt(2);y=np.array([1,1j],complex)/np.sqrt(2)
    seq={'z':[z],'zx':[z,x],'triad':[z,x,y]}[frame]
    vector=np.array([1.],complex)
    for a in range(k):vector=np.kron(vector,seq[a%len(seq)])
    phi=np.array([1.,0.,0.,1.])/np.sqrt(2)
    model.rho0=np.kron(np.outer(phi,phi),np.outer(vector,vector.conj()))
    return model,chan,dec,inp


def cascade_initial(chan,inp,n,theta,seed):
    m=chan.o;k=int(round(np.log2(m)));u=np.eye(2*m,dtype=complex)
    for a in range(k):
        order=list(range(k+1));order[a],order[-1]=order[-1],order[a]
        p=permutation_unitary([2]*(k+1),order)
        u=(np.cos(theta)*np.eye(2*m)+1j*np.sin(theta)*p)@u
    coeff=chan.coeff_from_kraus([u.reshape(m,2,2*m)[:,e,:] for e in range(2)])
    return [[x.copy() for x in coeff] for _ in range(n)]


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--k',type=int,default=3);p.add_argument('--theta',type=float,default=.3);p.add_argument('--n',type=int,default=262);p.add_argument('--sweeps',type=int,default=12);p.add_argument('--frame',default='triad');p.add_argument('--solver',default='CLARABEL');p.add_argument('--tol',type=float,default=1e-8);p.add_argument('--out');a=p.parse_args()
    result,policy,decoder,states=optimize_rotor(a.k,a.theta,a.n,a.sweeps,a.frame,a.theta,0,a.solver,a.tol,_setup=cascade_setup,_policy=cascade_initial)
    result['model']='matched_cascade_control';result['k']=a.k
    if a.out:
        Path(a.out+'.json').write_text(json.dumps(result,indent=2));data={'states':np.array(states),'decoder':decoder[0]}
        for k,x in enumerate(zip(*policy)):data['policy_block_'+str(k)]=np.array(x)
        np.savez_compressed(a.out+'.npz',**data)
    print(json.dumps({'result':result},indent=2),flush=True)
