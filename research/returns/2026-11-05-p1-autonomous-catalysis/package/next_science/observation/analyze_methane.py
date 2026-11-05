"""Reproducible descriptive calculations and a declared two-isotope box model.

This is not a new 3-D atmospheric inversion. Surface network global means
are not unqualified total atmospheric burdens; the model calculation explicitly
assumes that substitution and the prescribed minor sinks and source signatures.
"""
from pathlib import Path
import json
import numpy as np
import openpyxl

ROOT=Path(__file__).resolve().parent
w=openpyxl.load_workbook(ROOT/'isotope_source_4.xlsx',data_only=True,read_only=True)
v=list(w['Figure 1a'].values); vi=list(w['Figure 1b'].values)
t=np.array(v[1][1:],float)
c=np.array(v[2][1:],float)
d=np.array(vi[2][1:],float)
assert np.array_equal(t,np.array(vi[1][1:],float))
assert np.isfinite(np.c_[t,c,d]).all()
rstd=0.0111802
r=rstd*(1+d/1000)
x=c/(1+r)
y=x*r
alpha=1/1.0054
z,wt=np.polynomial.legendre.leggauss(8)
z=(z+1)/2;wt=wt/2

def interval_current(a,b,alpha=alpha):
    ids=np.where((t>=a)&(t<b))[0]
    X=x[ids];R=r[ids];T=t[ids]
    dx=np.diff(X);dr=np.diff(R)
    q=(1-alpha)*dx + np.sum(wt[None,:]*
        ((X[:-1,None]+dx[:,None]*z)/(R[:-1,None]+dr[:,None]*z))*dr[:,None],axis=1)
    return dict(start=float(T[0]),end=float(T[-1]),
                isotope_eliminated_current_ppb12_per_year=float(q.sum()/(T[-1]-T[0])),
                mean_ch4_ppb=float(c[ids].mean()),mean_delta_per_mil=float(d[ids].mean()),
                endpoint_ch4_slope=float((c[ids[-1]]-c[ids[0]])/(T[-1]-T[0])),
                endpoint_isotope_slope=float((d[ids[-1]]-d[ids[0]])/(T[-1]-T[0])))

years=np.arange(2000,2023)
C=np.array([c[(t>=j)&(t<j+1)].mean() for j in years])
D=np.array([d[(t>=j)&(t<j+1)].mean() for j in years])
R=rstd*(1+D/1000)
X=2.84*C/(1+R)
Y=X*R
DX=np.gradient(X,years)
DY=np.gradient(Y,years)

# Two explicit constructions use the same annual-mean observed histories,
# constant endmember signatures, and a declared global one-box approximation.
src_m=rstd*(1-62/1000)
src_f=rstd*(1-45/1000)
src_p=rstd*(1-24/1000)
E_p_total=25.0
E_p=E_p_total/(1+src_p)
k_oh0=0.1
k_other=1/90
alpha_target=1/1.009
alpha_other=(alpha_target*(k_oh0+k_other)-alpha*k_oh0)/k_other

def reconstruct(drop):
    ko=np.full(len(years),k_oh0)
    ko[years>=2020]*=(1-drop)
    A=DX+(ko+k_other)*X-E_p
    B=DY+(alpha*ko+alpha_other*k_other)*Y-E_p*src_p
    EF=(B-src_m*A)/(src_f-src_m)
    EM=A-EF
    e_total=EM*(1+src_m)+EF*(1+src_f)+E_p_total
    residual1=DX-(EM+EF+E_p-(ko+k_other)*X)
    residual2=DY-(src_m*EM+src_f*EF+src_p*E_p-(alpha*ko+alpha_other*k_other)*Y)
    rows=[]
    for i,j in enumerate(years):
        if j>=2015:
            rows.append(dict(year=int(j),microbial_Tg=float(EM[i]*(1+src_m)),
                            fossil_Tg=float(EF[i]*(1+src_f)),total_Tg=float(e_total[i]),
                            OH_loss_Tg=float(ko[i]*(X[i]+alpha*Y[i]))))
    return dict(OH_drop_after_2020=drop,rows=rows,
                max_mass_balance_residual=float(max(abs(residual1).max(),abs(residual2).max())),
                minimum_microbial_Tg=float((EM*(1+src_m)).min()),
                minimum_fossil_Tg=float((EF*(1+src_f)).min()))

def complete_interpolated_construction(drop):
    """Exact reconstruction for the complete piecewise-linear annual-mean path.

    Knots are annual midpoints. The OH change occurs at calendar 2020.0.
    On each open segment, burdens are linear and reconstructed emissions are
    linear. Endpoint positivity therefore certifies positivity on the segment.
    This interpolation is declared, not additional atmospheric observations.
    """
    knots=years+.5
    split=np.unique(np.r_[knots,2020.0])
    rows=[]
    for lo,hi in zip(split[:-1],split[1:]):
        idx=np.searchsorted(knots,(lo+hi)/2)-1
        sx=(X[idx+1]-X[idx])/(knots[idx+1]-knots[idx])
        sy=(Y[idx+1]-Y[idx])/(knots[idx+1]-knots[idx])
        ko=k_oh0*(1-drop if lo>=2020 else 1)
        ends=[]
        for u in [lo,hi]:
            xx=X[idx]+sx*(u-knots[idx]);yy=Y[idx]+sy*(u-knots[idx])
            aa=sx+(ko+k_other)*xx-E_p
            bb=sy+(alpha*ko+alpha_other*k_other)*yy-E_p*src_p
            ef=(bb-src_m*aa)/(src_f-src_m);em=aa-ef
            err=max(abs(sx-(em+ef+E_p-(ko+k_other)*xx)),
                    abs(sy-(src_m*em+src_f*ef+src_p*E_p-(alpha*ko+alpha_other*k_other)*yy)))
            ends.append(dict(t=float(u),microbial_Tg_per_year=float(em*(1+src_m)),
                             fossil_Tg_per_year=float(ef*(1+src_f)),
                             OH_loss_Tg_per_year=float(ko*(xx+alpha*yy)),residual=float(err)))
        rows.append(dict(start=float(lo),end=float(hi),endpoints=ends))
    return dict(drop=drop,path='piecewise linear X,Y through annual means at year+0.5; OH jump at 2020.0',
                minimum_microbial_Tg_per_year=min(e['microbial_Tg_per_year']for r in rows for e in r['endpoints']),
                minimum_fossil_Tg_per_year=min(e['fossil_Tg_per_year']for r in rows for e in r['endpoints']),
                max_balance_residual=max(e['residual']for r in rows for e in r['endpoints']),segments=rows)

w2=openpyxl.load_workbook(ROOT/'isotope_source_5.xlsx',data_only=True,read_only=True)
v2=list(w2['Figure 2a-d'].values)
pub={}
for label,idx in [('Joint',2),('Joint+OH',4)]:
    total=np.array(v2[idx][1:24],float)
    micro=np.array(v2[idx+6][1:24],float)
    fossil=np.array(v2[idx+12][1:24],float)
    before=(years>=2017)&(years<=2019);after=(years>=2020)&(years<=2022)
    pub[label]={f'{nm}_change_Tg_per_year':float(arr[after].mean()-arr[before].mean())
                for nm,arr in [('total',total),('microbial',micro),('fossil',fossil)]}

output=dict(
    scope='Descriptive observation contrasts and explicitly assumed one-box reconstructions; not a 3-D inversion or a confidence interval.',
    source='Oh et al. 2026, DOI 10.1038/s41467-026-74777-4, source workbooks 4 and 5',
    annual_observations=[dict(year=int(j),ch4_ppb=float(a),delta_per_mil=float(b))for j,a,b in zip(years,C,D)],
    isotope_current_periods={f'{a}-{b}':interval_current(a,b) for a,b in [(2008,2014),(2014,2020),(2017,2020),(2020,2023)]},
    fractionation_sensitivity={str(a):[interval_current(2017,2020,a),interval_current(2020,2023,a)]for a in [1/1.0054,1/1.0039]},
    published_inversion_comparison=pub,
    declared_box_parameters=dict(ppb_to_Tg=2.84,alpha_OH=alpha,alpha_other=alpha_other,
            OH_rate_per_year=k_oh0,minor_rate_per_year=k_other,
            microbial_delta=-62,fossil_delta=-45,pyrogenic_delta=-24,pyrogenic_Tg=25),
    countermodels=[reconstruct(q)for q in [0,.03,.04]],
    complete_interpolated_countermodels=[complete_interpolated_construction(q)for q in [0,.03,.04]],
)
(ROOT/'methane_calculations.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:output[k] for k in ['isotope_current_periods','published_inversion_comparison']},indent=2))
for r in output['countermodels']:
    print('MODEL',r['OH_drop_after_2020'],'residual',r['max_mass_balance_residual'],'positive minima',r['minimum_microbial_Tg'],r['minimum_fossil_Tg'])
    print(json.dumps(r['rows'][-6:],indent=2))
