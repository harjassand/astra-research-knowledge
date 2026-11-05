"""Optimize independent initialization and final readout for a fixed cascade.

Every carrier meets S and then k receiver qubits at the same angle, and is
discarded. No intermediate receiver control is optimized here. Alternation is
over an arbitrary pure initialized frame and a physical final CPTP decoder.
It gives feasible values/local optima, not a global theorem.
"""
import sys,json,argparse
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'joint_channel'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'joint_operational'))
from pure_frame_cascade import channel,ptS,power_psd,initial
from control_search import SDPSolver,choi_cost,adjoint_local,trace_pair,herm

pauli=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
bell=np.array([1.,0.,0.,1.])/np.sqrt(2)
phi=np.outer(bell,bell)

def frame_map(power,k):
    m=2**k;d=2*m
    out=np.zeros((4*m*m,m*m),complex)
    for a in range(m):
        for b in range(m):
            frame=np.zeros((m,m),complex);frame[a,b]=1
            choi=np.zeros((2*m,2*m),complex)
            for i in range(2):
                for j in range(2):
                    source=np.zeros((2,2));source[i,j]=1
                    image=(power@np.kron(source,frame).reshape(-1)).reshape(d,d)
                    choi[i*m:(i+1)*m,j*m:(j+1)*m]=ptS(image,2,m)/2
            out[:,a*m+b]=choi.reshape(-1)
    return out

def run(k,theta,t,restarts=4,sweeps=15):
    m=2**k;n=max(1,round(t/theta**4))
    power=np.linalg.matrix_power(channel(k,theta),n)
    fmap=frame_map(power,k)
    rng=np.random.default_rng(12341+k)
    solver=SDPSolver(m,2,tol=2e-9)
    best=None
    for trial in range(restarts):
        if trial==0:omega=initial(k,'triad')
        else:
            v=rng.normal(size=m)+1j*rng.normal(size=m);v/=np.linalg.norm(v)
            omega=np.outer(v,v.conj())
        decoder=None;history=[]
        for iteration in range(sweeps):
            choi=herm((fmap@omega.reshape(-1)).reshape(2*m,2*m))
            cost=choi_cost(choi,phi,2,m)
            decoder,info=solver.solve(cost,decoder)
            fidelity=trace_pair(cost,decoder)
            history.append(fidelity)
            effect=adjoint_local(phi,decoder,2,m)
            initcost=herm((fmap.conj().T@effect.reshape(-1)).reshape(m,m))
            val,vec=np.linalg.eigh(initcost);v=vec[:,-1]
            omega=np.outer(v,v.conj())
            if iteration>1 and abs(history[-1]-history[-2])<2e-9:break
        choi=herm((fmap@omega.reshape(-1)).reshape(2*m,2*m))
        cost=choi_cost(choi,phi,2,m)
        decoder,_=solver.solve(cost,decoder)
        fidelity=trace_pair(cost,decoder)
        images=[]
        for p in pauli:
            # E(sigma/2)=Tr_R[(sigma^T tensor I) Choi].
            images.append(np.einsum('ba,aibj->ij',p.T,choi.reshape(2,m,2,m)))
        inv=power_psd(images[0],-.25)
        a=sum(np.linalg.norm(inv@x@inv,'fro')**2 for x in images[1:])/3
        record={'k':k,'theta':theta,'N':n,'Ntheta4':n*theta**4,'trial':trial,
                'Fe':fidelity,'Petz_visibility':a,'history':history,
                'choi_trace':float(np.trace(choi).real),'choi_min_eigenvalue':float(np.linalg.eigvalsh(choi)[0])}
        print(json.dumps(record),flush=True)
        if best is None or fidelity>best[0]:best=(fidelity,omega,decoder,record)
    tag=f'cascade_frame_k{k}_theta{theta:g}_t{t:g}'
    Path('joint_root/results').mkdir(exist_ok=True)
    np.savez_compressed(f'joint_root/results/{tag}.npz',initial_state=best[1],decoder_choi=best[2],frame_map=fmap)
    Path(f'joint_root/results/{tag}.json').write_text(json.dumps(best[3],indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--k',type=int,nargs='+',default=[2,3]);p.add_argument('--theta',type=float,default=.05)
    p.add_argument('--t',type=float,nargs='+',default=[.1,.3,1.,3.]);p.add_argument('--restarts',type=int,default=4);p.add_argument('--sweeps',type=int,default=15)
    arg=p.parse_args()
    for k in arg.k:
        for t in arg.t:run(k,arg.theta,t,arg.restarts,arg.sweeps)
