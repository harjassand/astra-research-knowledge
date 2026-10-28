"""Numerical feasibility of simultaneous SO(3) boundary-channel deflation.

No numerical proposal in this file is a certified input. Actual rank-j
boundary vectors are probed through physical open-chain tensor correlations.
All SU(2) multiplets are included. The first accepted connected certificate
does not depend on this experiment.
"""
import pathlib,json,time,functools,math
import numpy as np
import scipy.linalg as la
from sympy.physics.wigner import clebsch_gordan
from sympy import Rational
from fugacity_messages import ROOT,blocks,paths
from triplet_discovery import swaps

TENSORS={0:[1,1,1,1,1],1:[-2,-1,0,1,2],2:[2,-1,-2,-1,2],
         3:[-1,2,0,-2,1],4:[1,-4,6,-4,1]}

@functools.lru_cache(None)
def pair_constants(rank):
    t=TENSORS[rank];result=[]
    for f in range(5):
        q=0
        for m in range(-2,3):
            for n in range(-2,3):
                cg=clebsch_gordan(2,2,f,m,n,m+n)
                q+=cg**2*t[m+2]*t[n+2]
        result.append(q/(2*f+1))
    if rank==1:
        assert result==[Rational(f*(f+1)-12,6) for f in range(5)]
    return tuple(result)

def boundary_moments(beta):
    ans={rank:[]for rank in range(1,5)}
    for n in range(2,7):
        sums={rank:0. for rank in ans}
        for total,bs in blocks(n):
            es,us=la.eigh(beta*sum(bs),check_finite=False)
            sub=[p for p in paths(n)if p[-1]==total]
            for rank in ans:
                qs=pair_constants(rank)
                q=np.diag([float(qs[p[2]])for p in sub])
                for edge in range(1,n-1):
                    sw=swaps(n,total)[edge];q=sw@q@sw
                diag=np.sum(us*(q@us),axis=0)
                sums[rank]+=(2*total+1)*np.dot(diag,np.exp(-es))
        for rank in ans:
            ans[rank].append((-1)**rank*sums[rank]/5**(n-2))
    return ans

def proposals(beta):
    moments=boundary_moments(beta);rows=[]
    for rank,m in moments.items():
        signed=[(-1)**(rank*r)*v for r,v in enumerate(m)]
        g=np.array([[signed[i+j]for j in range(2)]for i in range(2)])
        h=np.array([[signed[i+j+1]for j in range(2)]for i in range(2)])
        h2=np.array([[signed[i+j+2]for j in range(2)]for i in range(2)])
        es,us=la.eigh(h,g);c=us[:,-1];c/=max(abs(c))
        theta=c@h@c/(c@g@c);var=c@h2@c/(c@g@c)-theta**2
        rows.append({'rank':rank,'moments':m,'theta_signed_J':float(theta),
                     'variance_J':float(var),'candidate_coefficients':c.tolist()})
    return rows

def main():
    start=time.monotonic();out=[]
    exact=json.loads((ROOT/'results/scalar_loop_certificate.json').read_text())
    for beta,name in [(1.5,'3/2'),(3.,'3'),(6.,'6')]:
        rows=proposals(beta);data=next(x for x in exact['rows']if x['beta_exact']==name)
        ts={x['rank']:x['theta_signed_J']for x in rows};vs={x['rank']:x['variance_J']for x in rows}
        ts[0]=data['theta_J_lower']
        residual={'I4':data['I4'][1]-ts[0]**4-ts[3]**4-ts[4]**4,
                  'O4':data['O4'][1]-ts[2]**4-ts[4]**4,
                  'N6':data['N6'][1]-ts[1]**6-ts[2]**6-2*ts[3]**6-2*ts[4]**6}
        rI=max(0,residual['I4'])**.25;rO=max(0,residual['O4'])**.25;rN=max(0,residual['N6'])**(1/6)
        rests={0:rI,1:rN,2:min(rO,rN),3:min(rI,rN/2**(1/6)),4:min(rI,rO,rN/2**(1/6))}
        for row in rows:
            j=row['rank'];row['other_in_same_spin_channel_modulus_upper_proposal']=rests[j]
            row['Temple_signed_eigenvalue_upper_proposal']=ts[j]+vs[j]/(ts[j]-rests[j])if ts[j]>rests[j]else None
        item={'beta':beta,'channels':rows,'residual_moment_mass_proposals':residual,
              'residual_radius_proposals':{'I':rI,'O':rO,'N':rN},
              'scalar_theta':ts[0],'scope':'NUMERICAL_FEASIBILITY_ONLY_NO_ACCEPTED_NEXT_INPUT'}
        out.append(item);print(json.dumps(item),flush=True)
    result={'status':'NUMERICAL_MULTICHANNEL_DEFLATION_FEASIBILITY','rows':out,'seconds':time.monotonic()-start,
            'tensor_pair_constants':{j:list(map(str,pair_constants(j)))for j in range(5)}}
    (ROOT/'results/multichannel_discovery.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
