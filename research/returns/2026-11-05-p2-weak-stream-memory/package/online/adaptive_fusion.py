"""Physical covariant fusion receiver with greedy exact pinching-loss control.

All joint states are represented by their SU(2) multiplicity blocks. Matrix
sizes do not grow with retained spin J. This is an exploratory actual receiver,
not a performance theorem. Reference is time reversed, so initial Choi is a
singlet. No bath purifier, prepared bath label, or source return is used.
"""
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

I2=np.eye(2,dtype=complex)
PAULIS=[np.array([[0,1],[1,0]],complex),
        np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]


@lru_cache(maxsize=200000)
def cg2(j1,m1,j2,m2,j,m):
    """Condon-Shortley CG coefficient; all arguments doubled integers."""
    if m1+m2!=m or abs(m1)>j1 or abs(m2)>j2 or abs(m)>j:
        return 0.0
    if j<abs(j1-j2) or j>j1+j2 or ((j1+j2-j)&1):
        return 0.0
    vals=[(j+j1-j2)//2,(j-j1+j2)//2,(j1+j2-j)//2,
          (j1+j2+j)//2+1,(j+m)//2,(j-m)//2,
          (j1-m1)//2,(j1+m1)//2,(j2-m2)//2,(j2+m2)//2]
    logpref=math.log(j+1)+sum(math.lgamma(x+1) for x in vals[:3])-math.lgamma(vals[3]+1)
    logpref+=sum(math.lgamma(x+1) for x in vals[4:])
    aa=(j1+j2-j)//2;bb=(j1-m1)//2;cc=(j2+m2)//2
    dd=(j-j2+m1)//2;ee=(j-j1-m2)//2
    lo=max(0,-dd,-ee);hi=min(aa,bb,cc)
    ans=0.0
    for k in range(lo,hi+1):
        den=[k,aa-k,bb-k,cc-k,dd+k,ee+k]
        ans+=(-1.0 if k&1 else 1.0)*math.exp(.5*logpref-sum(math.lgamma(x+1) for x in den))
    return ans


@lru_cache(maxsize=None)
def external_basis(k):
    """List (coupling path, twice spin, {twice m: computational vector})."""
    data=[((1,),1,{1:np.array([1,0],complex),-1:np.array([0,1],complex)})]
    for count in range(1,k):
        nxt=[]
        for path,j,states in data:
            for jp in [j-1,j+1]:
                if jp<0:continue
                out={}
                for m in range(-jp,jp+1,2):
                    v=np.zeros(2**(count+1),complex)
                    for e,me in [(0,1),(1,-1)]:
                        mo=m-me
                        if mo in states:
                            ket=np.eye(2,dtype=complex)[:,e]
                            v+=cg2(j,mo,1,me,jp,m)*np.kron(states[mo],ket)
                    out[m]=v
                nxt.append((path+(jp,),jp,out))
        data=nxt
    return data


def magnetization(bits,k):
    return k-2*bits.bit_count()


@lru_cache(maxsize=30000)
def coupled_basis(twj,k,twl,twm):
    """Columns of total-L multiplicities in a fixed M computational slice.

    Rows are k exterior bitstrings. The spin-J magnetic number is uniquely
    fixed by M and that bitstring; invalid rows are zero.
    """
    columns=[]
    for path,twk,states in external_basis(k):
        if twl<abs(twj-twk) or twl>twj+twk or ((twj+twk-twl)&1):
            continue
        if abs(twm)>twl:continue
        vec=np.zeros(2**k,complex)
        for bits in range(2**k):
            mk=magnetization(bits,k);mj=twm-mk
            if mk in states:
                vec[bits]=states[mk][bits]*cg2(twj,mj,twk,mk,twl,twm)
        columns.append(vec)
    return np.column_stack(columns) if columns else np.zeros((2**k,0),complex)


def total_labels(twj,k):
    return sorted({twl for _,twk,_ in external_basis(k)
                   for twl in range(abs(twj-twk),twj+twk+1,2)})


def density_slice(blocks,twj,k,twm):
    out=np.zeros((2**k,2**k),complex)
    for twl,a in blocks.items():
        if abs(twm)>twl:continue
        b=coupled_basis(twj,k,twl,twm)
        out+=b@a@b.conj().T
    return out


def trace_blocks(blocks):
    return sum((twl+1)*np.trace(a).real for twl,a in blocks.items())


def purity_blocks(blocks):
    return sum((twl+1)*np.trace(a@a).real for twl,a in blocks.items())


@lru_cache(maxsize=1000)
def source_unitary(theta):
    swap=np.zeros((16,16),complex)
    for bits in range(16):
        sb=(bits>>2)&1;eb=bits&1
        target=bits ^ ((sb^eb)<<2) ^ (sb^eb)
        swap[target,bits]=1
    return math.cos(theta)*np.eye(16)+1j*math.sin(theta)*swap


def append_and_collide(blocks,twj,theta):
    result={}
    unitary=source_unitary(theta)
    for twl in total_labels(twj,4):
        physical=np.zeros((16,16),complex)
        for e,me in [(0,1),(1,-1)]:
            old=density_slice(blocks,twj,3,twl-me)
            physical[e::2,e::2]=old/2
        physical=unitary@physical@unitary.conj().T
        basis=coupled_basis(twj,4,twl,twl)
        result[twl]=basis.conj().T@physical@basis
    return result


def receiver_mid_vector(twj,tw_m,branch):
    """Total receiver spin J, obtained by fusing Q_J,E first to J+branch/2."""
    jp=twj+branch
    out=np.zeros(4,complex)
    if jp<0 or abs(tw_m)>twj:return out
    for r,mr in [(0,1),(1,-1)]:
        mp=tw_m-mr
        second=cg2(jp,mp,1,mr,twj,tw_m)
        for e,me in [(0,1),(1,-1)]:
            mq=mp-me
            out[2*r+e]=second*cg2(twj,mq,1,me,jp,mp)
    return out


@lru_cache(maxsize=30000)
def receiver_operators(twj,tw_m):
    """Q0,Qx,Qy,Qz on the R,E slice at fixed receiver magnetization."""
    branch_op=np.zeros((4,4),complex)
    for direction in [-1,1]:
        jp=twj+direction
        if jp<0:continue
        for r,mr in [(0,1),(1,-1)]:
            mp=tw_m-mr
            vector=np.zeros(4,complex)
            for e,me in [(0,1),(1,-1)]:
                vector[2*r+e]=cg2(twj,mp-me,1,me,jp,mp)
            branch_op+=direction*np.outer(vector,vector.conj())
    plus=receiver_mid_vector(twj,tw_m,1)
    minus=receiver_mid_vector(twj,tw_m,-1)
    mid=np.column_stack([plus,minus])
    qs=[mid@p@mid.conj().T for p in PAULIS]
    return [branch_op-qs[2]]+qs,mid


@lru_cache(maxsize=30000)
def slice_control_data(twj,twl):
    basis=coupled_basis(twj,4,twl,twl)
    physical=[np.zeros((16,16),complex) for _ in range(4)]
    mids=[]
    for rs in range(4):
        mrs=magnetization(rs,2)
        qs,mid=receiver_operators(twj,twl-mrs)
        sl=slice(4*rs,4*rs+4)
        for k in range(4):physical[k][sl,sl]=qs[k]
        mids.append(mid)
    reduced=[basis.conj().T@q@basis for q in physical]
    return reduced,mids


def sphere_quadratic_minimum(a,b):
    scale=max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    aa=(a+a.T)/(2*scale);bb=b/scale
    values,vectors=np.linalg.eigh(aa)
    bet=vectors.T@bb
    if np.linalg.norm(bet)<1e-13:return vectors[:,0]
    amin=values[0]
    active=np.abs(values-amin)<1e-11
    denom=values-amin
    inverse=np.zeros(3)
    inverse[~active]=bet[~active]/denom[~active]
    if np.linalg.norm(bet[active])<1e-11 and np.dot(inverse,inverse)<=1:
        sol=-inverse
        sol[np.where(active)[0][0]]=math.sqrt(max(0,1-np.dot(sol,sol)))
        return vectors@sol
    def secular(shift):return float(np.sum((bet/(values+shift))**2)-1)
    low=-amin+max(1e-14,1e-13*np.linalg.norm(bet[active]))
    if secular(low)<0:
        # Numerically degenerate hard case; lower endpoint approximates it.
        sol=-bet/(values+low)
        return vectors@(sol/np.linalg.norm(sol))
    high=max(1.0,low+1.0)
    while secular(high)>0:high=2*high+1
    shift=brentq(secular,low,high,xtol=1e-13)
    sol=-bet/(values+shift)
    return vectors@(sol/np.linalg.norm(sol))


def source_identity_projection(blocks,twj,k=4):
    reduced=output_blocks(blocks,twj,k)
    result={}
    low_mask=2**(k-2)-1
    for twl in blocks:
        physical=np.zeros((2**k,2**k),complex)
        for source,ms in [(0,1),(1,-1)]:
            old=density_slice(reduced,twj,k-1,twl-ms)/2
            indices=[((bits>>(k-2))<<(k-1))+(source<<(k-2))+(bits&low_mask)
                     for bits in range(2**(k-1))]
            physical[np.ix_(indices,indices)]=old
        basis=coupled_basis(twj,k,twl,twl)
        result[twl]=basis.conj().T@physical@basis
    return result


def optimal_direction(blocks,twj,q_weight=1.0):
    if twj==0:return np.array([0.,0.,1.]),0.0
    gram=np.zeros((4,4))
    actual_gram=np.zeros((4,4))
    projected=source_identity_projection(blocks,twj) if q_weight!=1 else None
    for twl,state in blocks.items():
        qs,_=slice_control_data(twj,twl)
        comm=[q@state-state@q for q in qs]
        if projected is not None:
            state_p=projected[twl]
            comm_p=[q@state_p-state_p@q for q in qs]
            comm_q=[x-y for x,y in zip(comm,comm_p)]
        for a in range(4):
            for b in range(a,4):
                val=(twl+1)*np.vdot(comm[a],comm[b]).real
                chosen=val if projected is None else (twl+1)*(
                    np.vdot(comm_p[a],comm_p[b]).real+q_weight*np.vdot(comm_q[a],comm_q[b]).real)
                gram[a,b]+=chosen;actual_gram[a,b]+=val
                if b!=a:gram[b,a]+=chosen;actual_gram[b,a]+=val
    direction=sphere_quadratic_minimum(gram[1:,1:],gram[0,1:])
    vec=np.r_[1.,direction]
    # D_new=dim(source+memory+carrier)=8(2J+1).
    loss=8*(twj+1)*float(vec@actual_gram@vec)/6
    return direction,max(0.,loss)


def middle_unitary(direction):
    observable=sum(n*p for n,p in zip(direction,PAULIS))
    values,vectors=np.linalg.eigh(observable)
    return vectors[:,::-1].conj().T


def branches(blocks,twj,direction):
    unitary=middle_unitary(direction)
    result={}
    for sign in [-1,1]:
        jp=twj+sign
        if jp<0:continue
        output={}
        for twl,state in blocks.items():
            output_basis=coupled_basis(jp,3,twl,twl)
            if output_basis.shape[1]==0:continue
            input_basis=coupled_basis(twj,4,twl,twl)
            _,mids=slice_control_data(twj,twl)
            operation=np.eye(16,dtype=complex)
            if twj>0:
                for rs,mid in enumerate(mids):
                    sl=slice(4*rs,4*rs+4)
                    operation[sl,sl]+=mid@(unitary-np.eye(2))@mid.conj().T
            fusion=np.zeros((8,16),complex)
            for oldbits in range(8):
                mp=twl-magnetization(oldbits,3)
                for e,me in [(0,1),(1,-1)]:
                    fusion[oldbits,2*oldbits+e]=cg2(twj,mp-me,1,me,jp,mp)
            reduced=output_basis.conj().T@fusion@operation@input_basis
            output[twl]=reduced@state@reduced.conj().T
        probability=trace_blocks(output)
        if probability>1e-15:
            result[sign]=(jp,{l:a/probability for l,a in output.items()},probability)
    return result


def initial_state(theta):
    singlet=np.array([0,1,-1,0],complex)/math.sqrt(2)
    rho=np.kron(np.outer(singlet,singlet.conj()),np.eye(4)/4)
    for target in [2,3]:
        swap=np.zeros((16,16),complex)
        for bits in range(16):
            left=(bits>>2)&1;right=(bits>>(3-target))&1
            dest=bits^((left^right)<<2)^((left^right)<<(3-target))
            swap[dest,bits]=1
        u=math.cos(theta)*np.eye(16)+1j*math.sin(theta)*swap
        rho=u@rho@u.conj().T
    blocks={}
    for twl in total_labels(1,3):
        basis=coupled_basis(1,3,twl,twl)
        physical=np.zeros((8,8),complex)
        valid=[]
        for bits in range(8):
            mq=twl-magnetization(bits,3)
            valid.append(2*bits+(1-mq)//2 if abs(mq)<=1 else None)
        for r in range(8):
            for c in range(8):
                if valid[r] is not None and valid[c] is not None:
                    physical[r,c]=rho[valid[r],valid[c]]
        blocks[twl]=basis.conj().T@physical@basis
    return blocks


def initial_mixed_frame(twj):
    """Singlet reference/source and fully tracial R,Q_J receiver."""
    singlet=np.array([0,1,-1,0],complex)/math.sqrt(2)
    sr=np.outer(singlet,singlet.conj())
    blocks={}
    for twl in total_labels(twj,3):
        physical=np.zeros((8,8),complex)
        for row in range(8):
            mq=twl-magnetization(row,3)
            if abs(mq)>twj:continue
            for col in range(8):
                mqp=twl-magnetization(col,3)
                if mq==mqp and (row&1)==(col&1):
                    physical[row,col]=sr[row>>1,col>>1]/(2*(twj+1))
        basis=coupled_basis(twj,3,twl,twl)
        blocks[twl]=basis.conj().T@physical@basis
    return blocks


def output_blocks(blocks,twj,k=3):
    result={}
    dout=2**(k-1)
    for twl in total_labels(twj,k-1):
        physical=np.zeros((dout,dout),complex)
        for source,ms in [(0,1),(1,-1)]:
            old=density_slice(blocks,twj,k,twl+ms)
            low_mask=2**(k-2)-1
            indices=[((bits>>(k-2))<<(k-1))+(source<<(k-2))+(bits&low_mask)
                     for bits in range(dout)]
            physical+=old[np.ix_(indices,indices)]
        basis=coupled_basis(twj,k-1,twl,twl)
        result[twl]=basis.conj().T@physical@basis
    return result


def information(blocks,twj,k=3):
    total=(2**k*(twj+1)*purity_blocks(blocks)-1)/3
    out=output_blocks(blocks,twj,k)
    acquired=(2**(k-1)*(twj+1)*purity_blocks(out)-1)/3
    return total,acquired


def trajectory(theta,n,rng,policy='optimal',check=False,initial_spin=None,q_weight=1.0,switch_step=None):
    if initial_spin is None:
        state=initial_state(theta);twj=1;start=3
    else:
        twj=round(2*initial_spin);state=initial_mixed_frame(twj);start=1
    losses=0.;records=[]
    max_spin=twj/2
    checkpoints={2,3,5,10,20,50,100,200,500,1000,n}
    for step in range(start,n+1):
        previous_total=information(state,twj)[0] if check else None
        incoming=append_and_collide(state,twj,theta)
        weight=q_weight if switch_step is None or step<=switch_step else 1.0
        direction,loss=optimal_direction(incoming,twj,weight)
        if policy=='canonical':direction=np.array([0.,0.,1.])
        outcomes=branches(incoming,twj,direction)
        if check:
            assert abs(trace_blocks(incoming)-1)<1e-9
            assert abs(sum(item[2] for item in outcomes.values())-1)<1e-9
            incoming_total,incoming_p=information(incoming,twj,4)
            old_total,old_p=information(state,twj)
            assert abs(incoming_total-old_total)<1e-9
            assert abs(incoming_p-old_p-math.sin(theta)**4*(old_total-old_p))<1e-9
            after=sum(prob*information(b,j)[0] for j,b,prob in outcomes.values())
            if policy=='optimal':assert abs(previous_total-after-loss)<1e-8,(previous_total,after,loss)
            for sign,(j,b,prob) in outcomes.items():
                expected=(j+1)/(2*(twj+1))
                assert abs(prob-expected)<1e-9,(twj,j,prob,expected)
        choices=list(outcomes)
        probabilities=np.array([outcomes[c][2] for c in choices]);probabilities/=probabilities.sum()
        selected=choices[int(rng.choice(len(choices),p=probabilities))]
        twj,state,prob=outcomes[selected]
        losses+=loss
        max_spin=max(max_spin,twj/2)
        if step in checkpoints:
            total,p=information(state,twj)
            records.append({'step':step,'spin':twj/2,'total_gram':total,'acquired_gram':p,
                            'source_residual_gram':total-p,'cumulative_conditional_loss':losses,
                            'petz_entanglement_fidelity':(1+3*p)/4})
    return {'theta':theta,'N':n,'policy':policy,'initial_spin':initial_spin,
            'q_weight':q_weight,'switch_step':switch_step,'max_spin':max_spin,'records':records}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--theta',type=float,default=.3)
    parser.add_argument('--n',type=int,default=100)
    parser.add_argument('--samples',type=int,default=1)
    parser.add_argument('--seed',type=int,default=1729)
    parser.add_argument('--policy',choices=['optimal','canonical'],default='optimal')
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--initial-spin',type=float)
    parser.add_argument('--q-weight',type=float,default=1.0)
    parser.add_argument('--switch-step',type=int)
    args=parser.parse_args()
    rng=np.random.default_rng(args.seed)
    runs=[]
    for sample in range(args.samples):
        run=trajectory(args.theta,args.n,rng,args.policy,args.check,args.initial_spin,args.q_weight,args.switch_step)
        runs.append(run)
        print(json.dumps({'sample':sample,'max_spin':run['max_spin'],'last':run['records'][-1]}),flush=True)
    result={'status':'actual finite-history receiver diagnostic, not a performance theorem',
            'parameters':vars(args),'runs':runs}
    name='adaptive_fusion_'+args.policy+'_'+str(args.theta).replace('.','p')+'_'+str(args.n)+'_'+str(args.samples)+'.json'
    if args.initial_spin is not None:name=name[:-5]+'_J'+str(args.initial_spin)+'.json'
    if args.q_weight!=1:name=name[:-5]+'_q'+str(args.q_weight)+'_switch'+str(args.switch_step)+'.json'
    Path(__file__).with_name(name).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
