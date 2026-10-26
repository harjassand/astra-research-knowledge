#!/usr/bin/env python3
"""Analytic bounds and exact spectral-moment sign checks for sparse temporal echo.
Only standard library plus mpmath (for reporting values). The inequalities shown
in the output have rational safety cushions, not numerical matrix scans.
"""
import math,json
import mpmath as mp
mp.mp.dps=60
T=12.;tau=.5;L=T-2*tau;alpha=.16;eta=.01;Omega=12.;mu=2*math.pi
I=mp.mpf(11)*4**6*mp.beta(7,7)
Wmax=math.sqrt(6)*eta*Omega/math.sqrt(30)
vmax=eta*math.sqrt(Omega/5)*(4/5)**2
hmax=math.sqrt(6)*alpha
hpmax=(12/L)*hmax
radmax=alpha*vmax*math.sqrt(72*math.pi*float(I))
rhomin=math.sqrt(1-hmax*hmax-radmax*radmax)
rad_over_h=Wmax*T/2
rprime_over_h=(hpmax+Wmax*radmax)/rhomin+math.pi/(2*float(I)*math.sqrt(2)*alpha)
co=(hpmax+Wmax*radmax)/rhomin
cc=rprime_over_h*math.sqrt(3)+co*math.sqrt(2)
cn=math.hypot(co,cc)
qoc=Wmax*rad_over_h*math.sqrt(3)
qn=qoc*(2+math.sqrt(2))
schur=6*eta**2*Omega/5
margin=mu-cn-qn-schur
assert co < .469 and cc < 4.681 and cn <4.71
assert qn < .104 and schur < .0015 and margin >1.46
S=mp.sin(6); C=mp.cos(6)
m0=mp.sqrt(2)*(-5+6*S+5*C)/67500
m1=mp.sqrt(2)*(-96-5*mp.pi*C+6*S-6*mp.pi*S+5*mp.pi+60*C)/33750
m1cc=mp.mpf(72)/21875-6*mp.pi/3125
assert m0 < -.000039 and m1 < -.00143 and m1cc < -.00274
# Coarse *rigorously checkable* sign intervals: pi in (3.141592,3.141593)
# Taylor alternating series for sin(2pi-6) and cos(2pi-6) yield
# sin(6) in (-.280,-.279), cos(6) in (.960,.961).
# For M_1, upper bound each signed term independently.
N0_up=-5+6*(-.279)+5*.961
N1_up=-96-5*3.141592*.960+6*(-.279)-6*3.141593*(-.280)+5*3.141593+60*.961
assert N0_up<0 and N1_up<0
result={
 'parameters':{'T':T,'tau':tau,'mu':mu,'alpha':alpha,'eta':eta,'cutoff':Omega},
 'analytic_bounds':{'W_operator_norm_upper':Wmax,'v_sup':vmax,'h_max':hmax,'hprime_max':hpmax,'radiation_norm_upper':radmax,'storage_norm_lower':rhomin,'radiation_over_h_upper':rad_over_h,'rprime_over_h_upper':rprime_over_h,'C_outer_column_upper':co,'C_center_column_upper':cc,'C_operator_norm_upper':cn,'Q_operator_norm_upper':qn,'Schur_counterterm_upper':schur,'Schur_margin_lower':margin,'conservative_certified_margin':1.46},
 'exact_moment_forms':{'M0_outer_center':'sqrt(2)*(-5+6*sin(6)+5*cos(6))/67500','M1_outer_center':'sqrt(2)*(-96-5*pi*cos(6)+6*sin(6)-6*pi*sin(6)+5*pi+60*cos(6))/33750','M1_center_center':'72/21875-6*pi/3125'},
 'moments':{'M0_outer_center':str(m0),'M1_outer_center':str(m1),'M1_center_center':str(m1cc)},
 'moment_interval_guard':{'sin_6':'(-0.280,-0.279)','cos_6':'(0.960,0.961)','M0_numerator_upper':N0_up,'M1_numerator_upper':N1_up},
 'statement':'Sufficient continuous-time Schur positivity and nonzero early-time cross-moments; no temporal gridding used.'
}
with open('/mnt/data/astra_spatiotemporal_sparse_certificates.json','w') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
