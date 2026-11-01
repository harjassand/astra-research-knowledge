"""Actual first-r-exit controls for the distinguishing m=5 two-A family.

All B overflow is absorbed as a separate unfavorable outcome. Thus up plus
overflow bounds the full first-up probability at the displayed inputs; this
is neither a closed truncation nor a numerical recurrence proof.
"""
import json,math,hashlib
from pathlib import Path
import numpy as np
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
    rows=[];cols=[];values=[];rhs=np.zeros((len(states),4))
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
        rhs[i,3]=1/total
        for rate,t in channels:
            nr=t[0]+t[1]-H(t[2],m);p=rate/total
            if nr==r+1:rhs[i,0]+=p
            elif nr==r-1:rhs[i,1]+=p
            else:
                assert nr==r
                if t[2]>Bmax:rhs[i,2]+=p
                else:rows.append(i);cols.append(ix[t]);values.append(-p)
    mat=csc_matrix(coo_matrix((values,(rows,cols)),shape=(len(states),len(states))))
    val=splu(mat).solve(rhs)
    residual=float(np.max(abs(mat@val-rhs)))
    sumerror=float(np.max(abs(val[:,:3].sum(axis=1)-1)))
    assert residual<2e-8 and sumerror<2e-7 and val.min()>-1e-9
    section=np.array([i for i,(a,x,b) in enumerate(states) if b==q and a>=2])
    worst=int(section[np.argmax(val[section,0]+val[section,2])])
    dormant=ix[(0,r+H(m,m),m)]
    return {'residual_r':r,'states':len(states),'B_overflow_boundary':Bmax,
            'max_active_section_up_plus_overflow':float(val[worst,0]+val[worst,2]),
            'maximizing_input_A_X_B':states[worst],
            'up_probability':float(val[worst,0]),'explicit_overflow_probability':float(val[worst,2]),
            'max_active_section_mean_first_exit_time':float(val[section,3].max()),
            'dormant_low_entrance_up_probability':float(val[dormant,0]),
            'all_input_equation_residual':residual,'all_input_probability_sum_error':sumerror}


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
