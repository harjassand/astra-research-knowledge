"""A posteriori full finite-grid ramp error from a polynomial defect.

DOP853 dense interpolation is degree seven. The ramp Hamiltonian has
degree-five time dependence, hence its Schroedinger defect has degree
at most twelve on each step. Thirteen-point Gauss-Legendre integrates
the squared Frobenius defect exactly in exact arithmetic. Cauchy-Schwarz
then bounds the integrated operator defect by the reported sum. Ordinary
rounding and eigensolver errors are still disclosed, not interval enclosed.
"""
from pathlib import Path
import importlib.util,json,math,time
import numpy as np
from scipy.sparse import eye,diags
from scipy.sparse.linalg import eigsh
from scipy.integrate import DOP853
from numpy.polynomial.legendre import leggauss

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('direct',HERE/'sparse_reciprocal.py')
direct=importlib.util.module_from_spec(spec);spec.loader.exec_module(direct)
def norm(a):return float(np.linalg.norm(a,2))

def run(height=203.7579951118813,hold=19.71756081512855,rise=4.,n=112,rtol=2e-9):
    start=time.monotonic();h0,w,code=direct.setup(n);dim=n*n
    shift=float(np.trace(code.T@(h0@code))/2);hc=h0-shift*eye(dim)
    def rhs(t,y):
        psi=y.reshape(dim,2)
        return (-1j*(hc@psi-height*direct.gate.smooth(t/rise)*(w[:,None]*psi))).reshape(-1)
    solver=DOP853(rhs,0.,code.astype(complex).reshape(-1),rise,rtol=rtol,atol=rtol*.01,max_step=.02)
    xx,weights=leggauss(13);xx=(xx+1)/2;weights=weights/2
    accumulated=0.;steps=0;max_defect=0.
    while solver.status=='running':
        solver.step();dense=solver.dense_output();h=dense.h
        y=np.zeros((13,dim*2),complex);dy=np.zeros_like(y)
        for i,f in enumerate(reversed(dense.F)):
            y+=f
            if i%2==0:
                dy=dy*xx[:,None]+y;y*=xx[:,None]
            else:
                dy=dy*(1-xx[:,None])-y;y*=1-xx[:,None]
        y+=dense.y_old;dy/=h
        times=dense.t_old+h*xx
        states=y.T.reshape(dim,26)
        hp=(hc@states).reshape(dim,2,13).transpose(2,0,1).reshape(13,dim*2)
        hp-=height*direct.gate.smooth(times[:,None]/rise)*np.tile(w, (2,1)).T.reshape(1,dim*2)*y
        residual=dy+1j*hp
        squared=np.sum(abs(residual)**2,axis=1)
        accumulated+=h*math.sqrt(float(weights@squared))
        max_defect=max(max_defect,float(math.sqrt(squared.max())))
        steps+=1
        if steps%500==0:print('audit',steps,solver.t,'bound',accumulated,'seconds',time.monotonic()-start,flush=True)
    state=solver.y.reshape(dim,2)
    ha=h0-diags(height*w)-shift*eye(dim)
    en,ev=eigsh(ha,k=48,which='SA',tol=5e-13);ii=np.argsort(en);en=en[ii];ev=ev[:,ii]
    co=ev.T@state;tail=norm(state-ev@co);eigen_residual=norm(ha@ev-ev*en)
    m=co.T@(np.exp(-1j*en*hold)[:,None]*co);target=np.diag([1j,1.]);phase=np.angle(np.trace(target.conj().T@m))
    gram=2*np.eye(2)-np.exp(-1j*phase)*target.conj().T@m-np.exp(1j*phase)*m.conj().T@target
    e2=float(np.linalg.eigvalsh(gram).max())
    # Ramp replacement affects both ends of the reciprocal overlap. For
    # approximate real orthonormal eigenvectors, a block-diagonal comparison
    # costs at most 2*T*eigen_residual in the hold propagator.
    overlap_bound=2*accumulated+accumulated**2+tail**2+2*hold*eigen_residual*norm(state)**2
    iso=norm(state.conj().T@state-np.eye(2))
    gram_defect=iso+tail**2
    polar_distance=gram_defect/(1+math.sqrt(1-gram_defect))
    overlap_normalization_bound=(1+math.sqrt(1+gram_defect))*polar_distance
    normalized_gate_bound=math.sqrt(max(0.,e2)+2*overlap_normalization_bound)
    linear_bound=normalized_gate_bound+4*(accumulated+tail+polar_distance)+hold*eigen_residual
    return dict(scope='Exact polynomial-defect and Duhamel formulas, evaluated in ordinary floating arithmetic on the actual112² finite grid. Transverse motion, continuum spatial convergence and interval rounding remain outside.',
        height=height,rise=rise,hold=hold,total_time=2*rise+hold,rtol=rtol,steps=steps,nfev=solver.nfev,
        elapsed_seconds=time.monotonic()-start,ramp_integrated_defect_upper=accumulated,
        maximum_sampled_frobenius_defect=max_defect,up_isometry_residual=iso,
        active_tail_norm=tail,active_eigen_residual=eigen_residual,
        numerical_gate_error=math.sqrt(max(0.,e2)),reciprocal_overlap_error_bound=overlap_bound,
        finite_grid_isometry_error_upper_from_defects=math.sqrt(max(0.,e2)+2*overlap_bound),
        projected_Gram_defect_bound=gram_defect,polar_normalization_distance_bound=polar_distance,
        normalized_reciprocal_gate_error_bound=normalized_gate_bound,
        finite_grid_isometry_error_linear_defect_bound=linear_bound,
        proof_note='Block-reflection unitary extension is proof-only; it does not require a physical ancilla, inverse bath, or reverse-time gate. Floating values are not interval enclosures.')

if __name__=='__main__':
    result=run();(HERE/'audited_ramp_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
