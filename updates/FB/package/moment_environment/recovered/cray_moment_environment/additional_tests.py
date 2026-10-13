"""Additional noncommuting-matrix diagnostics and an exact non-Gaussian failure."""
from fractions import Fraction
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
import sympy as sp
from experiment import psd_factor, impurity_energy, full_h, fermionic_hamiltonian


def paired_bath(poles):
    es=[]; vs=[]
    for e,L in poles:
        if e<1e-14:
            es.extend([0.]*L.shape[1]); vs.append(L)
        else:
            for sign in [-1,1]:
                es.extend([sign*e]*L.shape[1]); vs.append(L/np.sqrt(2))
    return np.array(es),np.concatenate(vs,axis=1)


def matrix_ph_tests():
    rng=np.random.default_rng(80326)
    m=2; e=np.array([.2,.55,.9])
    V=(rng.normal(size=(m,3))+1j*rng.normal(size=(m,3)))*.2
    W=2*V@V.conj().T; S=2*(V*(e**2))@V.conj().T
    L=psd_factor(W); Linv=np.linalg.pinv(L)
    B=Linv@S@Linv.conj().T
    lam,Q=np.linalg.eigh(B)
    low=paired_bath([(np.sqrt(lam[i]),(L@Q[:,i:i+1])) for i in range(m)])
    a,b=.1,1.
    Wa=(b*b*W-S)/(b*b-a*a); Wb=(S-a*a*W)/(b*b-a*a)
    high=paired_bath([(a,psd_factor(Wa)),(b,psd_factor(Wb))])
    true=(np.concatenate([-e,e]),np.concatenate([V,V],axis=1))
    def free(bath):
        ee,v=bath; ev=eigvalsh(full_h(np.zeros((m,m)),bath))
        return float(np.minimum(ev,0).sum()-np.minimum(ee,0).sum())
    R=free(low)-free(high)
    out=[]
    for u in [-2.,0.,3.]:
        ha=np.array([[.3,.17+.08j],[.17-.08j,-.5]])
        z=[impurity_energy(ha,x,[(0,1,u)]) for x in [high,true,low]]
        assert z[0]<=z[1]+1e-9 and z[1]<=z[2]+1e-9
        assert z[2]-z[0] <=R+1e-9
        out.append(dict(U=u,lower_energy=z[0],true_energy=z[1],upper_energy=z[2],
                        width=z[2]-z[0],universal_free_width=R))
    return out


def exact_failure():
    ha=np.diag([-1.,-1.]); bath=(np.array([1.,1.]),.8*np.eye(2))
    def rational_H(ub):
        num=fermionic_hamiltonian(full_h(ha,bath),[(0,1,1.),(2,3,float(ub))]).toarray().real
        return sp.Matrix([[sp.Rational(str(round(x,12))) for x in row] for row in num])
    Hlo=rational_H(sp.Rational(-9,5)); Hhi=rational_H(sp.Integer(2))
    shift=Hhi+sp.Rational(19,10)*sp.eye(16)
    LL,DD=shift.LDLdecomposition(hermitian=False)
    pivots=[DD[i,i] for i in range(16)]
    assert all(x>0 for x in pivots)
    assert LL*DD*LL.T==shift
    val,vec=np.linalg.eigh(np.array(Hlo,float))
    q=sp.Matrix([sp.Rational(int(round(x*1000000)),1000000) for x in vec[:,0]])
    rq=(q.T*Hlo*q)[0]/(q.T*q)[0]
    assert rq < sp.Rational(-19,10)
    return dict(
        reference_energy='-19/10',
        bath_hamiltonian='n_2+n_3+U_B*n_2*n_3',
        impurity_hamiltonian='-n_0-n_1+n_0*n_1',
        coupling='(4/5)*(d_0^dagger c_2+d_1^dagger c_3+h.c.)',
        lower_bath_U='-9/5',upper_bath_U='2',
        low_trial_vector=[str(x) for x in q],low_trial_energy=str(rq),
        high_shift_LDL_pivots=[str(x) for x in pivots],
        certified_conclusion='E(U_B=-9/5)<-19/10<E(U_B=2)',
        identical_data='Uncoupled-bath vacuum Green function: G(z)=I_2/(z-1), for either U_B.'
    )

if __name__=='__main__':
    out=dict(matrix_ph_tests=matrix_ph_tests(),exact_non_gaussian_failure=exact_failure())
    Path(__file__).with_name('additional_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
