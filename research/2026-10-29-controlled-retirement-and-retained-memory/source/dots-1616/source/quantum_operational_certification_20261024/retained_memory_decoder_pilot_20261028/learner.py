"""Source-disabled floating implementation of the manuscript's d=2 learner.
Public interface: act(i,z), observe(y). No source imports, memory, U, probabilities,
expected losses, or private audit records. Input labels j,s are not needed by update.
This is NOT the exact rational certified solver in manuscript section 6.
"""
from time import perf_counter
import numpy as np
from quantum_math import D, BASIS, C0, choi, barrier, tp_residual

class Learner:
    def __init__(self, gamma=1., epsilon=.25):
        self.gamma=gamma; self.epsilon=epsilon
        self.eta=gamma/(64*D*D)
        self.delta=self.eta*epsilon/64
        self.theta=np.zeros(D)
        self.pending=None
        self.failures=[]

    def act(self,i,z):
        start=perf_counter()
        if self.pending is not None: raise RuntimeError('unconsumed action')
        if not 0<=i<D or z not in (-1,1): raise ValueError('invalid private coins')
        c=choi(self.theta)
        grad,h=barrier(c)
        # numpy cholesky is H=L L^T; V=(3/4)L^{-T}, hence V^T H V=9I/16.
        l=np.linalg.cholesky(h)
        v=.75*np.linalg.solve(l.T,np.eye(D))
        dual=np.linalg.solve(v.T,np.eye(D))
        gram=v.T@h@v
        play=c+z/2*np.einsum('a,aij->ij',v[:,i],BASIS)
        self.pending=(i,z,grad,h,dual[:,i],self.theta.copy())
        diag={'whitening_seconds':perf_counter()-start,
              'whitening_eigen_min':float(np.linalg.eigvalsh(gram).min()),
              'whitening_eigen_max':float(np.linalg.eigvalsh(gram).max()),
              'center_eigen_min':float(np.linalg.eigvalsh(c).min()),
              'played_eigen_min':float(np.linalg.eigvalsh(play).min()),
              'played_tp_residual':tp_residual(play),
              'center_hessian_condition':float(np.linalg.cond(h))}
        if diag['whitening_eigen_min']<.5-1e-12 or diag['whitening_eigen_max']>1+1e-12:
            raise ArithmeticError('floating whitening guard failed')
        return play,diag

    def observe(self,y):
        start=perf_counter()
        if y not in (0,1): raise ValueError('return datum must be a bit')
        if self.pending is None: raise RuntimeError('no frozen action')
        i,z,grad0,h0,dual,old=self.pending
        self.pending=None
        ghat=2*D*y*z*dual
        candidate=old.copy(); iterations=0; backtracks=0
        success=True; reason=None
        try:
            if y:
                for step in range(25):
                    grad,h=barrier(choi(candidate))
                    residual=self.eta*ghat+grad-grad0
                    norm=float(np.linalg.norm(residual))
                    if norm <= min(self.delta/20,1e-11): break
                    direction=np.linalg.solve(h,-residual)
                    scale=1.
                    for bt in range(40):
                        trial=candidate+scale*direction
                        if np.linalg.eigvalsh(choi(trial)).min()>0:
                            trialgrad,_=barrier(choi(trial))
                            if np.linalg.norm(self.eta*ghat+trialgrad-grad0) <= (1-.1*scale)*norm:
                                break
                        scale*=.5;backtracks+=1
                    else: raise ArithmeticError('Newton backtracking exhausted')
                    candidate=trial;iterations+=1
                else: raise ArithmeticError('Newton iteration cap exhausted')
            residual=self.eta*ghat+barrier(choi(candidate))[0]-grad0
            delta=candidate-old
            locality_sq=float(delta@h0@delta)
            residual_norm=float(np.linalg.norm(residual))
            if residual_norm>self.delta or locality_sq>.25 or np.linalg.eigvalsh(choi(candidate)).min()<=0:
                raise ArithmeticError('floating step certificate failed')
            self.theta=candidate
        except Exception as exc:
            success=False;reason=repr(exc)
            self.theta=old # physical replacement, NOT silently a successful prox
            self.failures.append(reason)
            residual_norm=float(np.linalg.norm(self.eta*ghat))
            locality_sq=0.
        dual_norm_sq=float(ghat@np.linalg.solve(h0,ghat))
        return {'prox_seconds':perf_counter()-start,'newton_iterations':iterations,
                'newton_backtracks':backtracks,'prox_success':success,'failure':reason,
                'stationarity_residual':residual_norm,'stationarity_target':self.delta,
                'locality_squared':locality_sq,'dual_norm_squared':dual_norm_sq,
                'variance_bound':8*D*D*y,'theta_after':self.theta.tolist()}
