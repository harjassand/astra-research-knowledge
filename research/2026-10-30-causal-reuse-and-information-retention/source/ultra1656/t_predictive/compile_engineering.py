"""Access-gated engineering compiler; formal theorem is in the proof files.

The numerical protocol is intentionally far smaller than the formal universal
sample schedule and has NO guaranteed approximation accuracy. It is not an audit
replacement or a condition-free numerical SVD/optimization certificate.
"""
from pathlib import Path
from itertools import product
import json,time,hashlib
import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
import cvxpy as cp

HERE=Path(__file__).resolve().parent


class TargetSamples:
    def __init__(self,T,rng):
        self.T,self.rng,self.calls=T,rng,0
    def draw(self):
        self.calls+=1
        p=.18 if self.rng.random()<.41 else .72
        return tuple((self.rng.random(self.T)<p).astype(int))


class Teacher:
    def __init__(self,T,kappa,rng):
        self.T,self.kappa,self.rng=T,kappa,rng
        self.next_calls=self.conditional_samples=0
        self.locked=False
    def _mass(self,h):
        ones=sum(h);n=len(h)
        P=.41*.18**ones*.82**(n-ones)+.59*.72**ones*.28**(n-ones)
        half=self.T//2
        if n<=half:
            R=2.**(-n)
        else:
            R=2.**(-half) if h[half:]==h[:n-half] else 0.
        return (1-self.kappa)*P+self.kappa*R
    def next(self,h):
        if self.locked:raise RuntimeError('TEACHER CALL AFTER COMPILATION')
        self.next_calls+=1
        p0=self._mass(h+(0,))/self._mass(h)
        return np.array([p0,1-p0])
    def probability(self,h,f):
        answer=1.
        for o in f:
            answer*=self.next(h)[o];h=h+(o,)
        return answer
    def sample(self,h):
        if self.locked:raise RuntimeError('TEACHER CALL AFTER COMPILATION')
        self.conditional_samples+=1
        f=[]
        while len(h)<self.T:
            o=int(self.rng.random()>=self.next(h)[0]);f.append(o);h=h+(o,)
        return tuple(f)


def density(teacher,h,f):
    return 2.**(-len(f)) if h is None else teacher.probability(h,f)


def sample_mixture(teacher,rows,L,count,rng):
    out=[]
    for _ in range(count):
        h=rows[int(rng.integers(len(rows)))]
        out.append(tuple(rng.integers(2,size=L)) if h is None else teacher.sample(h))
    return out


def fresh_basis(teacher,prefixes,L,rank,M,rng):
    rows=list(prefixes);measure=rows+[None]
    futures=sample_mixture(teacher,measure,L,M,rng)
    probabilities=np.array([[density(teacher,h,f) for f in futures] for h in measure])
    mu=probabilities.mean(axis=0)
    U=probabilities[:-1].T/(M*mu[:,None])
    left,singular,right=np.linalg.svd(U,full_matrices=False)
    d=min(rank,int(np.sum(singular>1e-9)))
    d=max(1,d)
    coordinates=left[:,:d].T@U
    selected=[int(i) for i in qr(coordinates,pivoting=True,mode='economic')[2][:d]]
    swaps=0
    while True:
        coefficients=np.linalg.solve(coordinates[:,selected],coordinates)
        i,j=np.unravel_index(np.argmax(abs(coefficients)),coefficients.shape)
        if abs(coefficients[i,j])<=2+1e-8:break
        selected[i]=int(j);swaps+=1
        if swaps>1000:raise RuntimeError('barycentric acquisition did not terminate')
    return [rows[i] for i in selected],{'singular_values':singular.tolist(),'selected':selected,'swaps':swaps,
                                       'max_coordinate_coefficient':float(abs(coefficients).max()),
                                       'status':'known-rank truncation diagnostic, not formal robust threshold qualifier'}


class Compiled:
    def __init__(self,cache,T,tau,C):
        self.cache,self.T,self.tau,self.C=cache,T,tau,C
        self.solves=0;self.statuses=[];self.max_FW_gap=0.;self.max_constraint_error=0.
    def probabilities(self,alpha,t):
        raw=alpha@self.cache[t]['next']
        rounded=np.maximum(raw,self.tau/2)
        return rounded/rounded.sum()
    def transition(self,alpha,t,o,probability):
        R=self.cache[t+1]['R']
        beta=alpha*self.cache[t]['next'][:,o]/probability
        w=beta@self.cache[t]['child'][o]
        floor=self.cache[t+1]['floor']
        reference=np.maximum(w,floor)
        x=cp.Variable(R.shape[0]);z=x@R
        constraints=[cp.sum(x)==1,x<=self.C,x>=-self.C,z>=self.tau]
        objective=cp.sum(cp.rel_entr(z,reference)-z)/R.shape[1]
        problem=cp.Problem(cp.Minimize(objective),constraints)
        problem.solve(solver='CLARABEL',max_iter=200,tol_gap_abs=1e-8,tol_gap_rel=1e-8,tol_feas=1e-9)
        self.solves+=1;self.statuses.append(problem.status)
        if x.value is None:raise RuntimeError('convex inference returned no coefficient state')
        answer=np.array(x.value)
        # A diagnostic dual-gap LP; not a rigorous outward certificate.
        gradient=R@np.log(np.maximum(answer@R,1e-300)/reference)/R.shape[1]
        result=linprog(gradient,A_ub=-R.T,b_ub=-self.tau*np.ones(R.shape[1]),A_eq=np.ones((1,len(answer))),b_eq=[1.],
                       bounds=[(-self.C,self.C)]*len(answer),method='highs')
        if result.success:self.max_FW_gap=max(self.max_FW_gap,float(gradient@answer-result.fun))
        else:self.max_FW_gap=float('inf')
        error=max(abs(answer.sum()-1),max(0.,self.tau-float(np.min(answer@R))),max(0.,float(abs(answer).max())-self.C))
        self.max_constraint_error=max(self.max_constraint_error,error)
        return answer
    def law(self):
        states={():np.array([1-self.tau,self.tau])};masses={():1.}
        for t in range(self.T):
            for h in [h for h in states if len(h)==t]:
                p=self.probabilities(states[h],t)
                for o in (0,1):
                    child=h+(o,);masses[child]=masses[h]*p[o]
                    if t+1<self.T:states[child]=self.transition(states[h],t,o,p[o])
        return {h:p for h,p in masses.items() if len(h)==self.T}


def compile_model(source,teacher,T,N,M,D,rank,tau,rng):
    cache=[];dataset=[];geometry=[]
    for t in range(T):
        batch=[source.draw() for _ in range(N)];dataset.extend(batch)
        if t==0:rows=[()]
        else:
            rows,receipt=fresh_basis(teacher,[x[:t] for x in batch],T-t,rank,M,rng)
            geometry.append(receipt)
        rows=rows+[None]
        futures=sample_mixture(teacher,rows,T-t,D,rng)
        probabilities=np.array([[density(teacher,h,f) for f in futures] for h in rows])
        mu=probabilities.mean(axis=0)
        R=probabilities/mu
        nxt=np.array([[.5,.5] if h is None else teacher.next(h) for h in rows])
        theta=tau/(4*(rank+1));a=tau/4
        cache.append({'rows':rows,'futures':futures,'mu':mu,'R':R,'next':nxt,'floor':theta*a**(T-t)/mu})
    for t in range(T-1):
        futures=cache[t+1]['futures'];mu=cache[t+1]['mu'];rows=cache[t]['rows']
        cache[t]['child']=[]
        for o in (0,1):
            cache[t]['child'].append(np.array([[density(teacher,None if h is None else h+(o,),f) for f in futures] for h in rows])/mu)
    # Drop all teacher/source references; model only receives finite numerical cache.
    return Compiled(cache,T,tau,8*(rank+1)),dataset,geometry


def target_probability(h,pi=.41,a=.18,b=.72):
    ones=sum(h);n=len(h)
    return pi*a**ones*(1-a)**(n-ones)+(1-pi)*b**ones*(1-b)**(n-ones)


def ordinary_em(data,T):
    counts=np.array([sum(x) for x in data],dtype=float)
    output=[]
    for start in [(.5,.1,.8),(.25,.35,.65)]:
        pi,a,b=start
        for _ in range(500):
            left=pi*a**counts*(1-a)**(T-counts)
            right=(1-pi)*b**counts*(1-b)**(T-counts)
            w=left/(left+right)
            pi=float(w.mean());a=float((w*counts).sum()/(T*w.sum()));b=float(((1-w)*counts).sum()/(T*(1-w).sum()))
            a=np.clip(a,1e-8,1-1e-8);b=np.clip(b,1e-8,1-1e-8)
        output.append({'start':start,'pi':pi,'a':a,'b':b})
    return output


def main():
    protocol=json.loads((HERE/'ENGINEERING_PROTOCOL.json').read_text());p=protocol['input'];T=protocol['source']['T']
    rng=np.random.default_rng(p['seed']);source=TargetSamples(T,rng);teacher=Teacher(T,.02,rng)
    started=time.perf_counter()
    model,data,geometry=compile_model(source,teacher,T,p['fresh_prefixes_per_cut'],p['geometry_futures'],p['projection_futures'],p['rank_budget'],.005,rng)
    compilation=time.perf_counter()-started
    before={'next_calls':teacher.next_calls,'conditional_samples':teacher.conditional_samples};teacher.locked=True
    started=time.perf_counter();law=model.law();inference=time.perf_counter()-started
    assert before=={'next_calls':teacher.next_calls,'conditional_samples':teacher.conditional_samples}
    truth={h:target_probability(h) for h in law}
    tv=sum(abs(law[h]-truth[h]) for h in law)/2
    kl=sum(truth[h]*np.log(truth[h]/law[h]) for h in law)
    started=time.perf_counter();fits=ordinary_em(data,T);ordinary_seconds=time.perf_counter()-started
    for fit in fits:
        fit['tv']=sum(abs(target_probability(h,fit['pi'],fit['a'],fit['b'])-truth[h]) for h in law)/2
    record={'status':'completed engineering access control, NOT formal acquisition accuracy qualification',
            'protocol_sha256':hashlib.sha256((HERE/'ENGINEERING_PROTOCOL.json').read_bytes()).hexdigest(),
            'compilation_seconds':compilation,'exhaustive_inference_seconds':inference,'P_trajectory_samples':source.calls,
            'teacher_compilation':before,'teacher_inference_calls':0,'teacher_locked':teacher.locked,
            'known_source_rank_P':2,'known_source_middle_rank_Q':2**(T//2),
            'known_Delta_upper':-float(np.log(.98)),'total_variation':float(tv),'KL_P_to_compiled':float(kl),
            'compiled_probability_sum':sum(law.values()),'convex_solves':model.solves,
            'solver_statuses':{s:model.statuses.count(s) for s in set(model.statuses)},
            'max_diagnostic_FW_gap':model.max_FW_gap,'max_diagnostic_constraint_violation':model.max_constraint_error,
            'ordinary_mixture_EM':{'seconds':ordinary_seconds,'same_P_trajectories':len(data),'fits':fits},
            'geometry':geometry,'law':[{'word':list(h),'compiled':float(law[h]),'target':float(truth[h])} for h in law]}
    (HERE/'ENGINEERING_EXECUTION.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ['law','geometry']},indent=2))


if __name__=='__main__':main()
