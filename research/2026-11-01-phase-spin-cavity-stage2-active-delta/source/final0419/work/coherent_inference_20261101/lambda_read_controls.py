"""Full Lambda one-excitation read, with spontaneous branch noise retained.

The other excitation sectors are paid by their actual per-block mass, not
treated as a small global model error. No Raman elimination is used.
"""
import json,math,hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.sparse import csc_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'
def opnorm(x):return float(np.linalg.norm(x,2))
def maxeig(x):return float(np.linalg.eigvalsh((x+x.conj().T)/2)[-1])
def main():
    rows=[];X=np.array([[0,1],[1,0]],complex);Z=np.diag([1.,-1.])
    for ell in (2,4,8):
        # basis vacuum, s_i, e_i, one cavity photon
        d=2*ell+2;c=d-1;Is=np.eye(d);Ps=np.zeros((d,d));Pe=Ps.copy();Pc=Ps.copy();Pc[c,c]=1
        bs=np.zeros(d);bs[1:ell+1]=1/math.sqrt(ell);be=np.zeros(d);be[ell+1:2*ell+1]=1/math.sqrt(ell)
        Qs=np.outer(bs,bs);Qe=np.outer(be,be);Q=Qs+Qe+Pc
        C=np.zeros((d,d));S=np.zeros((d,d));branch=[];ground=[];phase=[];slow=[]
        ge=.02;ges=.005;phi=.001;gammas=.0001;kappa=.01
        for i in range(ell):
            s=1+i;e=1+ell+i;Ps[s,s]=1;Pe[e,e]=1;S[s,e]=S[e,s]=1
            L=np.zeros((d,d));L[s,e]=math.sqrt(ges);branch.append(L)
            L=np.zeros((d,d));L[0,e]=math.sqrt(ge);ground.append(L)
            L=np.zeros((d,d));L[0,s]=math.sqrt(gammas);slow.append(L)
            L=np.zeros((d,d));L[s,s]=L[e,e]=math.sqrt(2*phi);phase.append(L)
        C=np.outer(be,np.eye(d)[c])+np.outer(np.eye(d)[c],be)
        def adj(L):
            K=L.conj().T@L
            return L.conj().T@Q@L-(K@Q+Q@K)/2
        de=sum(adj(L) for L in branch);dg=sum(adj(L) for L in ground);dp=sum(adj(L) for L in phase)
        drift_error=opnorm(de-ges*(Pe/ell-Qe));phase_error=opnorm(dp-2*phi*((Ps+Pe)/ell-Qs-Qe))
        assert drift_error<1e-13 and phase_error<1e-13 and maxeig(dg)<1e-13
        assert opnorm(Q@S-S@Q)<1e-13 and opnorm(Q@C-C@Q)<1e-13
        Omega=1.;gc=.5;Tp=math.pi/(2*Omega);Tr=math.pi/(2*gc*math.sqrt(ell));T=Tp+Tr
        He=13*X+.2*Z;delta=.1
        Hs=np.kron(Is,He)+np.kron(S,Omega*(np.eye(2)+delta*Z))
        Hr=np.kron(Is,He)+np.kron(C,gc*math.sqrt(ell)*(np.eye(2)+delta*X))
        Lc=np.zeros((d,d));Lc[0,c]=math.sqrt(kappa)
        Ls=[np.kron(L,np.eye(2)) for L in branch+ground+phase+slow+[Lc]]
        dim=2*d;Id=eye(dim,format='csc')
        dissip=csc_matrix((dim*dim,dim*dim),dtype=complex)
        for L in Ls:
            L=csc_matrix(L);K=L.conj().T@L
            dissip+=kron(L.conj(),L)-.5*kron(Id,K)-.5*kron(K.T,Id)
        def generator(H):
            H=csc_matrix(H)
            return csc_matrix(-1j*(kron(Id,H)-kron(H.T,Id))+dissip)
        def effects(initial):
            inputs=np.column_stack([np.kron(initial,np.eye(2)[:,a:a+1]@np.eye(2)[b:b+1,:]).ravel(order='F') for b in range(2) for a in range(2)])
            gp=generator(Hs);gr=generator(Hr)
            mid=expm_multiply(Tp*gp,inputs,traceA=Tp*gp.diagonal().sum())
            end=expm_multiply(Tr*gr,mid,traceA=Tr*gr.diagonal().sum())
            effect=np.zeros((2,2),complex)
            for b in range(2):
             for a in range(2):
                rho=end[:,a+2*b].reshape(dim,dim,order='F')
                effect[b,a]=np.trace(rho[2*c:2*c+2,2*c:2*c+2])
            return effect
        false=effects(Ps/ell);true=effects(Qs)
        false_actual=opnorm(false);false_bound=(1+(ges+2*phi)*T)/ell
        noiseless_lower=math.cos(math.pi*delta/2)**4
        rate=max(ge+ges+2*phi,gammas+2*phi,kappa)
        true_bound=max(0.,math.sqrt(noiseless_lower)-rate*T/2)**2
        true_actual=float(np.linalg.eigvalsh((true+true.conj().T)/2)[0])
        assert false_actual<=false_bound+2e-11 and true_actual>=true_bound-2e-11
        rows.append({'atoms':ell,'pulse_duration':Tp,'collective_read_duration':Tr,
            'spontaneous_e_to_s_drift_identity_residual':drift_error,'dephasing_drift_identity_residual':phase_error,
            'actual_worst_source_false_read_probability':false_actual,'one_excitation_false_probability_upper':false_bound,
            'actual_worst_source_true_read_probability':true_actual,'no_jump_true_read_probability_lower':true_bound})
    result={'status':'PASS full Lambda one-excitation operator identities and noisy dynamics',
       'controls':rows,
       'full_product_thermal_false_bound':'p*(1-p)^(ell-1)*(1+(Gamma_es+2Gamma_phi)*T)+P(N>=2)+first_upward_event+initial_cavity_nonvac',
       'multiple_excitation_charge':'P(N>=2)<=ell*(ell-1)*p^2/2 per block; not a whole-run model failure budget',
       'limits':'actual common dipole and control couplings, source/capture, cavity geometry, rates, collection and detector qualification still needed; no practical advantage over Lambda Gaussian-memory incumbents established',
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'lambda_read_controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
