"""Two-primitive extension of the noisy cache; same acquired dominant space.

Run: OPENBLAS_NUM_THREADS=1 python check_affine_noncommuting.py
No dominant basis is provided to the learner. It is used only to construct the
synthetic fixed source and verify the approximation-width hypothesis.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import solve, eigh
from noisy_galerkin_benchmark import Source, next_power_two, project_out, near_zero_threshold, spectral


class AffineCache:
    def __init__(self, actions, n, alpha, mu, epsilon, audit):
        self.actions=actions
        self.n,self.alpha,self.mu=n,alpha,mu
        self.epsilon=epsilon
        self.tau=mu*epsilon/(1+epsilon)
        self.sigma=self.tau/16
        self.u=np.empty((n,0))
        self.yus=[np.empty((n,0)) for _ in actions]
        self.cap=1
        self.audit=audit
        self.diagonals=[]
        self.refreshes=[]

    @property
    def rank(self):
        return self.u.shape[1]

    def append(self,w):
        q=project_out(self.u,w)
        q/=np.linalg.norm(q)
        self.u=np.column_stack([self.u,q])
        newcap=next_power_two(self.rank+1)
        if newcap!=self.cap:
            self.cap=newcap
            tol=self.sigma/np.sqrt(self.cap)
            self.yus=[np.column_stack([action(self.u[:,i],tol) for i in range(self.rank)])
                      for action in self.actions]
            self.refreshes.append({"rank":self.rank,"cap":self.cap,"primitive_actions":len(self.actions)*self.rank})
        else:
            tol=self.sigma/np.sqrt(self.cap)
            self.yus=[np.column_stack([yu,action(q,tol)]) for yu,action in zip(self.yus,self.actions)]

    def solve(self,rhs,theta):
        assert np.sum(np.abs(theta))<=1+1e-14
        rank_before=self.rank
        for iteration in range(self.n+2):
            q=project_out(self.u,rhs)
            qnorm=np.linalg.norm(q)
            if qnorm>near_zero_threshold(self.n,np.linalg.norm(rhs)):
                q/=qnorm
                v=np.column_stack([self.u,q])
                ys=[np.column_stack([yu,action(q,self.sigma/np.sqrt(self.cap))])
                    for yu,action in zip(self.yus,self.actions)]
            else:
                v,ys=self.u,self.yus
            y=sum(weight*yj for weight,yj in zip(theta,ys))
            g=v.T@y
            h=self.alpha*np.eye(v.shape[1])+(g+g.T)/2
            self.audit.trial(v,ys,y,theta,self.sigma,h)
            z=solve(h,v.T@rhs,assume_a="sym")
            x=v@z
            xnorm=np.linalg.norm(x)
            cert=np.linalg.norm(rhs-self.alpha*x-y@z)+self.sigma*xnorm
            if cert<=self.tau*xnorm:
                return x,{"rank_before":rank_before,"rank_after":self.rank,"trials":iteration+1,
                          "enrichments":self.rank-rank_before,"certificate_ratio":float(cert/(self.tau*xnorm))}
            w=project_out(self.u,y@z)/xnorm
            diagonal=float(np.linalg.norm(w))
            assert diagonal>=self.tau-2*self.sigma-1e-10
            self.diagonals.append(diagonal)
            self.append(w)
        raise RuntimeError("No certificate")


class AffineAudit:
    def __init__(self,matrices,alpha):
        self.matrices=matrices
        self.alpha=alpha
        self.maximum_individual_error_ratio=0.0
        self.maximum_weighted_error_ratio=0.0
        self.maximum_orthogonality_defect=0.0
        self.minimum_h_eigenvalue=float("inf")

    def trial(self,v,ys,y,theta,sigma,h):
        each=[spectral(yj-bj@v)/sigma for yj,bj in zip(ys,self.matrices)]
        btheta=sum(weight*bj for weight,bj in zip(theta,self.matrices))
        combined=spectral(y-btheta@v)/sigma
        self.maximum_individual_error_ratio=max(self.maximum_individual_error_ratio,max(each))
        self.maximum_weighted_error_ratio=max(self.maximum_weighted_error_ratio,combined)
        self.maximum_orthogonality_defect=max(self.maximum_orthogonality_defect,spectral(v.T@v-np.eye(v.shape[1])))
        self.minimum_h_eigenvalue=min(self.minimum_h_eigenvalue,float(eigh(h,eigvals_only=True)[0]))
        assert max(each)<=1+1e-8
        assert combined<=1+1e-8

    def result(self,rhs,x,theta,epsilon):
        a=self.alpha*np.eye(rhs.size)+sum(weight*bj for weight,bj in zip(theta,self.matrices))
        truth=solve(a,rhs,assume_a="pos")
        error=float(np.linalg.norm(truth-x)/np.linalg.norm(truth))
        assert error<=epsilon+1e-9
        return error


def main():
    rng=np.random.default_rng(91871)
    n,r,tasks=128,4,40
    alpha=mu=0.2
    epsilon=0.02
    tau=mu*epsilon/(1+epsilon)
    tail=tau/8
    basis,_=np.linalg.qr(rng.normal(size=(n,r)))
    rotation,_=np.linalg.qr(rng.normal(size=(r,r)))
    cores=[np.diag([4.0,2.0,1.0,0.5]),rotation@np.diag([3.5,2.5,0.8,0.3])@rotation.T]
    matrices=[]
    noise_matrices=[]
    for core in cores:
        fullq,_=np.linalg.qr(rng.normal(size=(n,n)))
        small_eigs=rng.uniform(0.1,1.0,n)
        small_eigs[-1]=1.0
        # Each tail is generic, dense and strictly positive on the FULL space.
        perturbation=tail*(fullq*small_eigs)@fullq.T
        matrices.append(basis@core@basis.T+perturbation)
        noise=rng.normal(size=(n,n))
        noise_matrices.append(noise/spectral(noise))
    sources=[Source(b,nz) for b,nz in zip(matrices,noise_matrices)]
    audit=AffineAudit(matrices,alpha)
    cache=AffineCache([s.action for s in sources],n,alpha,mu,epsilon,audit)
    rows=[]
    previous=np.zeros(n)
    for task in range(tasks):
        # The next source mixture depends on the preceding computed answer.
        first=0.5+0.45*np.sin(0.37*task+0.2*np.sum(previous[:4]))
        theta=np.array([first,1-first])
        rhs=rng.normal(size=n)+0.2*previous
        rhs/=np.linalg.norm(rhs)
        calls_before=sum(s.calls for s in sources)
        x,info=cache.solve(rhs,theta)
        info.update({"task_index":task,"theta":theta.tolist(),
                     "source_calls":sum(s.calls for s in sources)-calls_before,
                     "true_relative_error":audit.result(rhs,x,theta,epsilon)})
        rows.append(info)
        previous=x
    projector=np.eye(n)-basis@basis.T
    result={"scope":"Finite diagnostic of the k=2 theorem; no supplied useful basis; no novelty or practical comparison claim",
            "dimension":n,"primitives":2,"tasks":tasks,"dominant_dimension":r,
            "alpha":alpha,"mu":mu,"epsilon":epsilon,"tau":tau,"sigma":cache.sigma,
            "tail_bound":tail,"verified_outside_dominant_norms":[spectral(projector@b) for b in matrices],
            "commutator_operator_norm":spectral(matrices[0]@matrices[1]-matrices[1]@matrices[0]),
            "source_calls_by_primitive":[s.calls for s in sources],
            "total_source_calls":sum(s.calls for s in sources),
            "source_output_scalars":sum(s.output_scalars for s in sources),
            "sum_inverse_tolerance_squared":sum(s.precision_cost for s in sources),
            "retained_rank":cache.rank,"retained_basis_and_action_scalars":(1+2)*n*cache.rank,
            "maximum_true_relative_error":max(row["true_relative_error"] for row in rows),
            "maximum_individual_error_matrix_ratio":audit.maximum_individual_error_ratio,
            "maximum_weighted_error_matrix_ratio":audit.maximum_weighted_error_ratio,
            "maximum_orthogonality_defect":audit.maximum_orthogonality_defect,
            "minimum_reduced_matrix_eigenvalue":audit.minimum_h_eigenvalue,
            "minimum_enrichment_diagonal":min(cache.diagonals),
            "required_diagonal_floor":cache.tau-2*cache.sigma,
            "capacity_refreshes":cache.refreshes,"task_rows":rows,"status":"PASS"}
    Path(__file__).with_name("affine_noncommuting_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="task_rows"},indent=2))


if __name__=="__main__":
    main()
