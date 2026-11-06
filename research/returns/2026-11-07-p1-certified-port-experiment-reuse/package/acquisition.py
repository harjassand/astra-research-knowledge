"""Source-independent port-only acquisition plan, fitting and exact checks.

The finite SDP fallback is proved in THEOREM.txt. The executed proposer
uses the already-installed SciPy LP solver and a fixed positive-residue
dictionary. Its output is untrusted until the rational checks pass.
"""
from fractions import Fraction as Q
from exact import C,require,ceilq,dyadic,encode,inverse,spectral_bound,psd


def plan(r,a,A0,c0,epsilon):
    a,A0,c0,epsilon=map(Q,(a,A0,c0,epsilon))
    require(r>0 and a>0 and A0>=a and c0>=0 and epsilon>0)
    epsilon=min(epsilon,a/4);M=r*c0+1;tau=epsilon/(16*r)
    N=max(2,ceilq(8*(c0+M)/(a*epsilon)))
    L=max(1,ceilq(16*c0/(a*tau)))
    mu=min(Q(1,4*r*L),a*tau/(16*L));C0=A0+c0/a
    frequencies=[2*a*i*N/Q(N*N-i*i) for i in range(N)]
    gamma=[tau/(64*r*(w+C0+1)**2) for w in frequencies]
    return encode({'r':r,'a':a,'A0':A0,'c0':c0,'epsilon':epsilon,'M':M,
                   'tau':tau,'frequency_count':N,'frequencies':frequencies,
                   'per_coordinate_budgets':gamma,'complete_grid_poles':L,
                   'complete_grid_mu':mu,'real_trials':2*r*N,
                   'scalar_readouts':2*r*r*N})


def process_record(record):
    contract=record['contract'];r=contract['r'];a=Q(contract['a'])
    expected=plan(r,a,contract['A0'],contract['c0'],contract['epsilon'])
    require(contract==expected,'Acquisition contract differs from its explicit rational plan.')
    C0=Q(contract['A0'])+Q(contract['c0'])/a
    rows=record['observations'];require(len(rows)==contract['frequency_count'])
    data=[];radii=[]
    for i,row in enumerate(rows):
        w=Q(contract['frequencies'][i]);require(Q(row['frequency'])==w)
        gamma=Q(row['certified_coordinate_error'])
        require(0<=gamma<=Q(contract['per_coordinate_budgets'][i]))
        G=[[C(*entry) for entry in line] for line in row['response_matrix']]
        require(len(G)==r and all(len(line)==r for line in G))
        sigma=2*r*gamma;m=w+C0
        require(m*sigma<1)
        radius=m*m*sigma/(1-m*sigma)
        Z=inverse(G)
        R=[[Z[u][v]-(C(0,w) if u==v else C()) for v in range(r)] for u in range(r)]
        # Reciprocal data are complex symmetric, not Hermitian.
        R=[[(R[u][v]+R[v][u])/2 for v in range(r)] for u in range(r)]
        data.append(R);radii.append(radius)
    return data,radii


def propose(record,poles=None,bits=42):
    import numpy as np
    from scipy.optimize import linprog
    contract=record['contract'];r=contract['r'];a=Q(contract['a'])
    poles=list(map(Q,poles or [a,5*a/4,3*a/2,2*a,4*a,8*a]))
    data,radii=process_record(record)
    directions=[]
    for i in range(r):
        v=[Q(0)]*r;v[i]=1;directions.append(v)
    for i in range(r):
        for j in range(i+1,r):
            for sign in [-1,1]:
                v=[Q(0)]*r;v[i]=1;v[j]=sign;directions.append(v)
    pairs=[(i,j) for i in range(r) for j in range(i,r)]
    npairs=len(pairs);nweights=len(poles)*len(directions);dim=npairs+nweights+1
    A=[];rhs=[]
    for w0,target in zip(contract['frequencies'],data):
        w=Q(w0)
        for pair_index,(i,j) in enumerate(pairs):
            for imaginary in [False,True]:
                row=np.zeros(dim)
                if not imaginary:row[pair_index]=1
                for ell,pole in enumerate(poles):
                    z=C(1)/C(pole,w)
                    factor=z.im if imaginary else z.re
                    for vv,v in enumerate(directions):
                        row[npairs+ell*len(directions)+vv]=-float(factor*v[i]*v[j])
                value=float(target[i][j].im if imaginary else target[i][j].re)
                row[-1]=-1;A.append(row);rhs.append(value)
                other=-row;other[-1]=-1;A.append(other);rhs.append(-value)
    mass=np.zeros(dim)
    for ell in range(len(poles)):
        for j,v in enumerate(directions):mass[npairs+ell*len(directions)+j]=float(sum(x*x for x in v))
    A.append(mass);rhs.append(float(Q(contract['M'])))
    bound=float(Q(contract['A0'])+1)
    objective=np.zeros(dim);objective[-1]=1
    result=linprog(objective,A_ub=np.array(A),b_ub=np.array(rhs),
                   bounds=[(-bound,bound)]*npairs+[(0,None)]*(nweights+1),
                   method='highs')
    require(result.success,'The optional numerical proposal did not succeed; the general SDP fallback is not implemented in this example.')
    Aa=[[Q(0)]*r for _ in range(r)]
    for k,(i,j) in enumerate(pairs):Aa[i][j]=Aa[j][i]=dyadic(Q.from_float(result.x[k]),bits)
    weights=[];residues=[]
    for ell in range(len(poles)):
        w=[max(Q(0),dyadic(Q.from_float(result.x[npairs+ell*len(directions)+j]),bits))
           for j in range(len(directions))]
        R=[[sum((weight*v[i]*v[j] for weight,v in zip(w,directions)),Q(0))
            for j in range(r)] for i in range(r)]
        weights.append(w);residues.append(R)
    return encode({'r':r,'a':a,'A':Aa,'poles':poles,'residues':residues,
                   'positive_dictionary':directions,'dictionary_weights':weights,
                   'coefficient_bits':bits,'proposal_status':'untrusted numerical LP',
                   'proposal_objective':float(result.fun),'proposal_iterations':int(result.nit),
                   'proposal_variables':dim,'proposal_inequalities':len(rhs)})


def certify(record,model):
    contract=record['contract'];r=contract['r'];a=Q(contract['a'])
    require(model['r']==r and Q(model['a'])==a)
    A=[list(map(Q,row)) for row in model['A']]
    require(len(A)==r and all(len(row)==r for row in A))
    require(all(A[i][j]==A[j][i] for i in range(r) for j in range(r)))
    residues=[[list(map(Q,row)) for row in R] for R in model['residues']]
    poles=list(map(Q,model['poles']));require(len(residues)==len(poles))
    require(all(v>=a for v in poles) and all(psd(R) for R in residues))
    mass=sum((R[i][i] for R in residues for i in range(r)),Q(0))
    require(mass<=Q(contract['M']))
    data,radii=process_record(record)
    local=[];fits=[]
    for w0,target,eta in zip(contract['frequencies'],data,radii):
        w=Q(w0)
        prediction=[[C(A[i][j])-sum((C(R[i][j])/C(pole,w)
                         for R,pole in zip(residues,poles)),C())
                     for j in range(r)] for i in range(r)]
        fit=spectral_bound([[prediction[i][j]-target[i][j] for j in range(r)] for i in range(r)])
        fits.append(fit);local.append(fit+eta)
    coverage=2*(Q(contract['c0'])+mass)/(a*contract['frequency_count'])
    error=max(local)+coverage
    require(error<a,'Uncertified dissipation margin')
    require(error<=Q(contract['epsilon']),'Candidate does not meet the requested error target.')
    S=[[A[i][j]-sum((R[i][j]/pole for R,pole in zip(residues,poles)),Q(0))
        for j in range(r)] for i in range(r)]
    require(psd([[S[i][j]-(a-error if i==j else Q(0)) for j in range(r)] for i in range(r)]))
    return encode({'status':'PASS','operator_error':error,'sample_error_max':max(local),
                   'fit_error_max':max(fits),'inverse_error_max':max(radii),
                   'all_frequency_coverage_error':coverage,'residue_trace_mass':mass,
                   'port_margin':a-error,'state_dimension':r*(1+len(poles)),
                   'coefficient_count':r*r*(1+len(poles)),'new_source_calls':0,
                   'certification':'exact rational finite-data check plus proved uniform frequency cover'})
