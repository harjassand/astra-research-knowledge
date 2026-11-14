"""Exact finite boundary-observation/power-writing diagnostic, introduced model.

The hypothetical signed square-current adaptation is NOT supplied by the P3
binary relay circuit. No material or global finite-noise/pulse claim is made.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

EDGES=[(0,4),(1,4),(4,5),(2,5),(3,5),(0,2)]
NODES=[0,1,2,4,5]
INDEX={n:i for i,n in enumerate(NODES)}
PATTERNS=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]


def solve(matrix,rhs):
    a=[[F(x) for x in row]+[F(b)] for row,b in zip(matrix,rhs)]
    for k in range(len(a)):
        p=next(i for i in range(k,len(a)) if a[i][k])
        a[k],a[p]=a[p],a[k];d=a[k][k];a[k]=[x/d for x in a[k]]
        for i in range(len(a)):
            if i!=k:
                q=a[i][k];a[i]=[x-q*y for x,y in zip(a[i],a[k])]
    return [row[-1] for row in a]


def determinant(a):
    a=[list(row) for row in a];out=F(1)
    for k in range(len(a)):
        p=next((i for i in range(k,len(a)) if a[i][k]),None)
        if p is None:return F(0)
        if p!=k:a[k],a[p]=a[p],a[k];out=-out
        d=a[k][k];out*=d
        for i in range(k+1,len(a)):
            q=a[i][k]/d
            for j in range(k+1,len(a)):a[i][j]-=q*a[k][j]
    return out


def boundary_observations(r):
    k=[[F(0)]*len(NODES) for _ in NODES]
    for (u,v),resistance in zip(EDGES,r):
        for n in (u,v):
            if n in INDEX:k[INDEX[n]][INDEX[n]]+=1/resistance
        if u in INDEX and v in INDEX:
            k[INDEX[u]][INDEX[v]]-=1/resistance
            k[INDEX[v]][INDEX[u]]-=1/resistance
    energies=[];fields=[]
    for q in PATTERNS:
        potential=solve(k,[q[n] if n<3 else 0 for n in NODES])
        voltages=dict(zip(NODES,potential));voltages[3]=F(0)
        currents=[(voltages[u]-voltages[v])/resistance for (u,v),resistance in zip(EDGES,r)]
        energies.append(sum(F(q[n])*voltages[n] for n in range(3)))
        fields.append([i*i for i in currents])
    return energies,fields


def inverse_from_boundary_energies(f):
    z=[[F(0)]*3 for _ in range(3)]
    for i in range(3):z[i][i]=f[i]
    for k,(i,j) in enumerate(((0,1),(0,2),(1,2)),3):
        z[i][j]=z[j][i]=(f[k]-f[i]-f[j])/2
    y=[z[i][0]-z[i][2] for i in range(3)]
    d=y[0]-y[2]
    coefficient=(z[1][2]-z[0][2])/((y[0]-y[1])*y[2])
    tree=[[z[i][j]+coefficient*y[i]*y[j] for j in range(3)] for i in range(3)]
    r4=tree[0][2];r2=tree[0][1]-r4
    return [tree[0][0]-tree[0][1],tree[1][1]-tree[0][1],r2,
            tree[2][2]-r4,r4,d+1/coefficient]


def main():
    target=[F(3,2)]*6
    gains=[F(1,2),F(1),F(3,2),F(5,4),F(3,4),F(2)]
    rows=[]
    # Teacher gets ONLY boundary energies. It reconstructs aggregate resistance
    # by the explicit inverse, then computes fields from that inferred model.
    for values in product((1,2),repeat=6):
        plant_r=list(map(F,values));energies,actual_fields=boundary_observations(plant_r)
        inferred=inverse_from_boundary_energies(energies);assert inferred==plant_r
        _,teacher_fields=boundary_observations(inferred)
        coefficients=solve(list(map(list,zip(*teacher_fields))),[x-y for x,y in zip(target,inferred)])
        produced=[sum(field[e]*u for field,u in zip(actual_fields,coefficients)) for e in range(6)]
        assert produced==[x-y for x,y in zip(target,plant_r)]
        actual_velocity=[gain*x for gain,x in zip(gains,produced)]
        assert all(v*(goal-r)>0 for v,goal,r in zip(actual_velocity,target,plant_r))
        rows.append({'resistances':list(map(str,plant_r)),
                     'field_determinant':str(determinant(actual_fields)),
                     'sum_absolute_coefficients':str(sum(map(abs,coefficients))),
                     'boundary_inverse_and_ideal_velocity_exact':True})
    chord=[]
    for rho in (F(1,1000),F(1,100),F(1,10),F(1),F(10)):
        f,fields=boundary_observations([F(1)]*5+[rho])
        assert inverse_from_boundary_energies(f)==[F(1)]*5+[rho]
        d=determinant(fields);formula=-8*rho*rho/(rho+3)**4
        assert d==formula
        chord.append({'rho':str(rho),'exact_square_field_determinant':str(d)})
    result={'scope':'INTRODUCED six-edge cyclic resistor graph; exact observations and hypothetical signed local square-current adaptation',
            'edges':EDGES,'boundary':[0,1,2,3],'hidden':[4,5],'patterns':PATTERNS,
            'corner_cases':rows,'chord_cases':chord,
            'conditional_global_controller':'If aggregate resistance is stably recoverable, power-pattern matrix V(r) has full row rank, and local law is rdot=A(r,hidden)*V(r)*u with unknown positive diagonal A, choose u=V(rhat)^+(rstar-rhat). With exact inferred rhat=r, rdot_e=a_e*(rstar_e-r_e), so all coordinates stay between initial and target and converge at the declared gain floor.',
            'physical_time_cost':'Coefficients u are synthesized by signed time-sharing; elapsed pulse time is proportional to sum(abs(u)), not merely one controller step.',
            'limitations':['Exact ideal averaged vector field only; no finite-pulse controller executed.',
                           'Zero observation error in these finite exact cases; no global noisy inverse bound.',
                           'Local square-current law and global reversible cue are INTRODUCED and physically unqualified; the P3 binary relay circuit does not supply them.',
                           'Recoverability alone supplies no useful conditioning, source-work or retention bound.',
                           'Full microscopic cell states need not be identified if an aggregate inverse and positive aggregate gains suffice.',
                           'Classical envelope sensitivity, inverse-network algebra and feedback linearization are credited; this is not a foundational novelty claim.']}
    p=Path(__file__);result['script_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    q=p.with_suffix('.json');q.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'corner_cases':len(rows),'largest_coefficient_l1':str(max(F(x['sum_absolute_coefficients']) for x in rows)),
                      'chord_cases':chord,'script_bytes':p.stat().st_size,'script_sha256':result['script_sha256'],
                      'json_bytes':q.stat().st_size,'json_sha256':hashlib.sha256(q.read_bytes()).hexdigest()}))


if __name__=='__main__':main()
