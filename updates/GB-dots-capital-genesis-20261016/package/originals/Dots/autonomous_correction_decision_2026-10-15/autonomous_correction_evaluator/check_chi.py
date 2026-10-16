#!/usr/bin/env python3
"""Exact central-value CP obstruction; marginal-SD sensitivities are NOT confidence tests."""
import json,math
from evaluate import sections

def eigenvalues_symmetric(matrix):
    a=[r[:] for r in matrix];n=len(a)
    for _ in range(100):
        p,q=max(((i,j) for i in range(n) for j in range(i+1,n)),key=lambda ij:abs(a[ij[0]][ij[1]]))
        if abs(a[p][q])<1e-15:break
        theta=.5*math.atan2(2*a[p][q],a[q][q]-a[p][p]);c,s=math.cos(theta),math.sin(theta)
        app,aqq,apq=a[p][p],a[q][q],a[p][q]
        for k in range(n):
            if k in (p,q):continue
            akp,akq=a[k][p],a[k][q]
            a[k][p]=a[p][k]=c*akp-s*akq
            a[k][q]=a[q][k]=s*akp+c*akq
        a[p][p]=c*c*app-2*c*s*apq+s*s*aqq
        a[q][q]=s*s*app+2*c*s*apq+c*c*aqq
        a[p][q]=a[q][p]=0.
    return sorted(a[i][i] for i in range(n))

def check():
    out={}
    basis='IXYZ'
    for stem in ['Fig2b','Fig3e','Fig3f']:
        rows={r['basis_element']:r for r in sections(stem+'_chi_matrix.csv')[0]}
        a=[[float(rows[i+j]['chi_real']) for j in basis] for i in basis]
        sym=[[(a[i][j]+a[j][i])/2 for j in range(4)] for i in range(4)]
        neg=[]
        for i in basis:
            r=rows[i+i];v,e=float(r['chi_real']),float(r['chi_err_real'])
            if v<0:neg.append({'element':i+i,'central':v,'marginal_bootstrap_sd':e,'sd_shifts_to_zero':-v/e,'plus_one_marginal_sd':v+e,'plus_two_marginal_sd':v+2*e})
        eig=eigenvalues_symmetric(sym)
        out[stem]={'max_real_asymmetry':max(abs(a[i][j]-a[j][i]) for i in range(4) for j in range(4)), 'trace_real':sum(a[i][i] for i in range(4)),'negative_diagonals':neg,'symmetrized_real_eigenvalues':eig,'exact_central_values_admit_CP_completion':False,'reason':'Negative diagonal precludes PSD chi for every possible choice of omitted imaginary parts. Small real asymmetry also precludes exact Hermiticity; symmetrization is diagnostic only.','uncertainty_warning':'Central reconstructed estimates only. Marginal SD shifts are sensitivity checks, not joint confidence regions; physical dynamics are not asserted non-CP.'}
    return out
if __name__=='__main__': print(json.dumps(check(),indent=2))
