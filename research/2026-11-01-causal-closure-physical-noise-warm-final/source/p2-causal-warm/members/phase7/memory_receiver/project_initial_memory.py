"""Project the actual finite-mediator output away from ALL initial-mode responses.

The same receiver is orthogonal to both Z1 signs. This is an output-mode
calculation, not a declaration that unobserved outputs are harmless.
"""
from pathlib import Path
import sys, json
import numpy as np
from scipy.linalg import svd
from scipy.special import ndtr, ndtri

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'new_research'/'root'))
sys.path.insert(0,str(ROOT/'new_research'/'conventional_routes'))
from finite_mediator_parity import Model,waveforms
from optimize_finite_mediator import matrices

def simpson_weights(t):
    n=len(t)
    assert n%2==1 and np.allclose(np.diff(t),t[1]-t[0])
    w=np.ones(n);w[1:-1:2]=4;w[2:-1:2]=2
    return w*(t[1]-t[0])/3

def generator(m,z):
    return np.array([[-m['kb']/2,0,-1j*m['g']],
                     [0,-m['kc']/2-1j*z*m['chi'],-1j*m['g']],
                     [-1j*m['g'],-1j*m['g'],-m['Gamma']/2]],complex)

def responses(m,t):
    columns=[]
    for z in (1,-1):
        val,vec=np.linalg.eig(generator(m,z));iv=np.linalg.inv(vec)
        E=np.einsum('ij,tj,jk->tik',vec,np.exp(t[:,None]*val),iv)
        columns.append(np.sqrt(m['Gamma'])*E[:,2,:])
    return np.column_stack(columns)

def project(m,t,A,label):
    w=simpson_weights(t);H=responses(m,t);hw=np.sqrt(w)[:,None]*H
    ua,ss,vh=svd(hw,full_matrices=False)
    rank=int(np.sum(ss>ss[0]*1e-12));Q=ua[:,:rank]
    a=1j*np.asarray(A);aw=np.sqrt(w)*a
    removed=Q@(Q.conj().T@aw);rw=aw-removed
    N=float(np.vdot(aw,aw).real);Neff=float(np.vdot(rw,rw).real)
    f=rw/np.sqrt(w)/np.sqrt(Neff)
    residual=f.conj()@(w[:,None]*H)
    beta=np.vdot(f,w*a)
    return dict(label=label,T=m['T'],model=m,N=N,N_effective=Neff,
                retained_fraction=Neff/N,signal_overlap=[beta.real,beta.imag],
                response_rank=rank,response_singular_values=ss.tolist(),
                max_homogeneous_overlap=float(np.max(abs(residual))),
                mode_norm=float(np.vdot(f,w*f).real),
                max_real_part_of_expected_imaginary_mode=float(np.max(abs(f.real))),
                same_pulse_assignment_error=float(ndtr(-2*np.sqrt(m['eta']*Neff))),
                amplitude_multiplier_for_original_q=float(np.sqrt(N/Neff)),
                raw_q=float(ndtr(-2*np.sqrt(m['eta']*N))),
                endpoints_mode=[[f[0].real,f[0].imag],[f[-1].real,f[-1].imag]]),f,H

def main():
    rows=[]
    for T in (4.,8.,12.,16.,24.,32.):
        m=Model(T=T,kb=1e-4,kc=1e-4)
        md=dict(T=m.T,g=m.g,Gamma=m.Gamma,chi=m.chi,kb=m.kb,kc=m.kc,eta=m.eta)
        t=np.linspace(0,T,12001);A=waveforms(m,t)['A']
        row,_,_=project(md,t,A,'sin6');rows.append(row)
        print('sin6',T,'retained',row['retained_fraction'],'q',row['same_pulse_assignment_error'],flush=True)
    src=json.loads((ROOT/'new_research/conventional_routes/finite_mediator_optimization_results.json').read_text())
    m=src['model'];t=np.linspace(0,m['T'],24001)
    for index in (0,len(src['optimized'])-1):
        c=np.array(src['optimized'][index]['coefficients']);F=matrices(len(c)-1,t,m)
        A=F['A']@c
        row,f,H=project(m,t,A,'optimized_order_'+str(len(c)-1));rows.append(row)
        print(row['label'],'retained',row['retained_fraction'],'q',row['same_pulse_assignment_error'],flush=True)
    out={'scope':'Vacuum fresh inputs, conserved physical Z during each window, actual same temporal mode rejects all initial-mode amplitudes for both signs. Full arbitrary-state theorem in report; this numeric projection only computes the receiver and signal cost.',
         'rows':rows}
    Path(__file__).with_name('initial_memory_projection_results.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
