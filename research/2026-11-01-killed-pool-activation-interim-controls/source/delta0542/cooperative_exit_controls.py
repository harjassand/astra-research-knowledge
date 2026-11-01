"""Actual first-r-exit controls for the distinguishing m=5 two-A family.

All B overflow is absorbed as a separate unfavorable outcome. Thus up plus
overflow bounds the full first-up probability at the displayed inputs; this
is neither a closed truncation nor a numerical recurrence proof.
"""
import json,math,hashlib
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.sparse import coo_matrix,csc_matrix
from scipy.sparse.linalg import splu
from cooperative_pool_controls import ff

ROOT=Path(__file__).resolve().parents[2]


def H(b,m):
    if b==0:return 0
    u,v=divmod(b-1,m)
    return u*(m-1)+v+1


def solve_level(r,m=5,Bmax=36):
    q=m+1
    states=[(a,r+H(b,m)-a,b) for b in range(Bmax+1) for a in range(r+H(b,m)+1)]
    ix={s:i for i,s in enumerate(states)}
    rows=[];cols=[];values=[];rhs=np.zeros((len(states),5));exact_rows=[]
    for i,(a,x,b) in enumerate(states):
        cat=ff(b,q);channels=[]
        for j,(ku,kd) in enumerate(zip((2,7,11),(1,3,5)),2):
            up=cat*ku*ff(a,j)*ff(x,m-j)
            down=cat*kd*ff(a,j+1)*ff(x,m-j-1)
            if up:channels.append((up,(a+1,x-1,b)))
            if down:channels.append((down,(a-1,x+1,b)))
        channels.append((1,(a+1,x,b+1)))
        if a*b:channels.append((a*b,(a+m-1,x,b+m)))
        if a>=m and b>=q:channels.append((cat*ff(a,m),(a-m,x,b-q)))
        total=sum(k for k,t in channels)
        rows.append(i);cols.append(i);values.append(1.)
        rhs[i,3]=1/total;rhs[i,4]=1.
        internal=[];absorbed=[0,0,0]
        for rate,t in channels:
            nr=t[0]+t[1]-H(t[2],m);p=rate/total
            if nr==r+1:rhs[i,0]+=p;absorbed[0]+=rate
            elif nr==r-1:rhs[i,1]+=p;absorbed[1]+=rate
            else:
                assert nr==r
                if t[2]>Bmax:rhs[i,2]+=p;absorbed[2]+=rate
                else:
                    rows.append(i);cols.append(ix[t]);values.append(-p)
                    internal.append((rate,ix[t]))
        exact_rows.append((total,internal,absorbed+[1,total]))
    mat=csc_matrix(coo_matrix((values,(rows,cols)),shape=(len(states),len(states))))
    lu=splu(mat);val=lu.solve(rhs)
    float_residual=float(np.max(abs(mat@val-rhs)))
    float_sumerror=float(np.max(abs(val[:,:3].sum(axis=1)-1)))
    mp.mp.dps=90
    high=[[mp.mpf(float(v)) for v in row] for row in val]
    def residuals(v):
        out=[]
        for i,(total,internal,b) in enumerate(exact_rows):
            row=[]
            for col in range(5):
                e=mp.mpf(b[col])-total*v[i][col]
                for rate,j in internal:e+=rate*v[j][col]
                row.append(e/total)
            out.append(row)
        return out
    refinement=[]
    for iteration in range(9):
        rem=residuals(high)
        norms=[max(abs(row[c]) for row in rem) for c in range(5)]
        refinement.append([str(x) for x in norms])
        if max(norms)<mp.mpf('1e-65'):break
        correction=lu.solve(np.array([[float(v) for v in row] for row in rem]))
        for i in range(len(high)):
            for c in range(5):high[i][c]+=mp.mpf(float(correction[i,c]))
    # Validate the FINAL residuals with outward-rounded interval arithmetic,
    # using exact integer rates and decimal point values as the approximants.
    mp.iv.dps=90
    quantized=[[mp.nstr(v,78) for v in row] for row in high]
    interval=[[mp.iv.mpf(v) for v in row] for row in quantized]
    bounds=[0.]*5
    for i,(total,internal,b) in enumerate(exact_rows):
        for col in range(5):
            e=mp.iv.mpf(b[col])-total*interval[i][col]
            for rate,j in internal:e+=rate*interval[j][col]
            e/=total
            # The next binary64 value above the rounded interval endpoint
            # is a conservative dyadic upper bound on that endpoint.
            bound=math.nextafter(float(abs(e).b),math.inf)
            bounds[col]=max(bounds[col],bound)
    max_steps=max(math.nextafter(float(row[4]),math.inf) for row in quantized)
    assert all(mp.mpf(row[4])>0 for row in quantized) and bounds[4]<0.01
    # If w>0 and (I-P)w>=1-e, then (I-P)^-1 1<=w/(1-e).
    # Therefore the exact solution error for residual bound d is <=d max(w)/(1-e).
    denominator_lower=math.nextafter(1-bounds[4],-math.inf)
    certified_errors=[math.nextafter(math.nextafter(b*max_steps,math.inf)/denominator_lower,math.inf) for b in bounds]
    assert max(certified_errors)<1e-45
    val=np.array([[float(v) for v in row] for row in quantized])
    sumerror=max(abs(sum(mp.mpf(v) for v in row[:3])-1) for row in quantized)
    assert sumerror<mp.mpf('1e-45')
    section=np.array([i for i,(a,x,b) in enumerate(states) if b==q and a>=2])
    worst=int(section[np.argmax(val[section,0]+val[section,2])])
    dormant=ix[(0,r+H(m,m),m)]
    return {'residual_r':r,'states':len(states),'B_overflow_boundary':Bmax,
            'max_active_section_up_plus_overflow':float(val[worst,0]+val[worst,2]),
            'maximizing_input_A_X_B':states[worst],
            'up_probability':float(val[worst,0]),'explicit_overflow_probability':float(val[worst,2]),
            'max_active_section_mean_first_exit_time':float(val[section,3].max()),
            'dormant_low_entrance_up_probability':float(val[dormant,0]),
            'initial_float_equation_residual':float_residual,
            'initial_float_probability_sum_error':float_sumerror,
            'all_input_interval_residual_bounds':bounds,
            'certified_all_input_absolute_solution_errors':certified_errors,
            'all_input_high_precision_probability_sum_error':str(sumerror),
            'max_expected_embedded_steps_upper_bound':max_steps/denominator_lower,
            'display_precision_note':'Displayed probabilities/times are rounded binary64; certified errors apply to the computed 78-digit decimal approximants.',
            'refinement_iterations':len(refinement)-1}


def main():
    rows=[]
    for r in (8,16,32,64,128):
        row=solve_level(r);rows.append(row);print(json.dumps(row),flush=True)
    result={'status':'PASS finite open-boundary full-CME first-exit controls',
            'model':'m=5,q=6,2A+3X <-> 3A+2X <-> 4A+X <-> 5A, common 6B',
            'scope':'Numerical Dirichlet controls only. Overflow is unfavorable, not silently reflected or deleted.',
            'rows':rows,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'outputs/mechanism_selection_20261101/cooperative_exit_controls.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
