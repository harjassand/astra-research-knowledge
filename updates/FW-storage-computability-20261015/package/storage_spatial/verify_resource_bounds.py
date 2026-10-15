"""Own exact rational checks of the analytic resource receipt; no external code."""
from fractions import Fraction as F
import json
from pathlib import Path
D=Path(__file__).parent
N=10**22; delta=F(1,10**6); s=F(1,10**40); K=10**44
P=F(N)+4*delta+1; L=F(N)+2*delta
d1=F(4897,5000); d2=F(5103,5000)
M=224; Estar=2*M*2500000; R4=(2*M+1)*2500000
checks={}
def ck(name,statement):
    assert statement,name
    checks[name]=True
ck('full_entry_energy_28_over_15',F(1)+F(2,3)+F(1,5)==F(28,15))
ck('entry_budget_224',120*F(28,15)==M)
ck('horizon_error_less_than_1e_minus_3',(6960*Estar)**4 < F(1,1000)**4*(N-1)**3)
ck('R_less_than_184',R4<184**4)
ck('Rtot_less_than_200',R4+2*delta+256<200**4)
ck('P_less_than_2e22',P<2*10**22)
ck('L_fourth_root_less_than_1e6',L<10**24)
# Known reference: |h'| <= 3; |h''| <= 5040; |h'''| <=23520.
ck('reference_A0_less_than_11000',2*5040+2<11000)
ck('reference_A1_less_than_60000',2*23520+2*3+2*5040+2<60000)
x0=10**27
ck('principal_heat_exponent_at_least_x0',delta**2/(4*d1*s)>=x0)
ck('image_exponent_slope_at_least_x0_plus_1',1/(16*d1*s)>=x0+1)
qbound=F(216)/(s*x0**4) # 9/s * (4! / x0^4)
ck('q_less_than_1e_minus_65',qbound<F(1,10**65))
Lw=188*N
e0=11000*s+F(N)*Lw/F(10**65)
e1=60000*s+F(Lw,10**65)
ck('e0_less_than_2e_minus_19',e0<F(2,10**19))
ck('e1_less_than_7e_minus_36',e1<F(7,10**36))
h0=10**6*(2*F(2,10**19)/N+F(7,10**36))
ck('h0_less_than_8e_minus_30',h0<F(8,10**30))
heaterr=180*F(8,10**30)*201**3
exterr=3*180*F(7,10**36)*5**3
ck('heat_repair_less_than_1e_minus_19',heaterr<F(1,10**19))
ck('exterior_less_than_1e_minus_30',exterr<F(1,10**30))
a=F(1,10**84)
ck('isotropic_fourier_majorant_x',s*d1*(6/P)**2>=a)
ck('isotropic_fourier_majorant_y',s*d2>=a)
ck('a_K_squared_is_1e4',a*K*K==10000)
# exp(-10000) <= 100! / 10000^100 <= 100^100 / 10000^100 = 10^-200.
Etail=F(1,10**200)
Cbar=10**21
ck('coefficient_radius',200**4*P**3<Cbar**4)
S0=3*10**42; S1=4*10**84
Tail0=10**40*Etail; Tail1=10**84*Etail
T0=Cbar*2*Tail0*S0
T1=Cbar*2*(Tail1*S0+Tail0*S1)
ck('T0_bound',T0<=F(6,10**97))
ck('T1_bound',T1<F(7,10**53))
t0=10**6*(2*T1+2*T0/N)
ck('truncation_gradient_less_than_2e_minus_46',t0<F(2,10**46))
fouriererr=180*F(2,10**46)*202**3
ck('fourier_action_less_than_1e_minus_36',fouriererr<F(1,10**36))
spatial=120*delta+heaterr+exterr+fouriererr
ck('spatial_error_less_than_1e_minus_3',spatial<F(1,1000))
dim=2*(2*K+1)**2
ck('dimension_less_than_1e90',dim<10**90)
# Basis is 2cos/-2sin, so repaired gradient sup <= 10K, L4 <=10^6*10K.
Bj=10**51; S=10**141; Abox=10**163
ck('basis_sum_bound',dim*Bj<S)
ck('box_gradient_bound',2*10**6+Cbar*S<Abox)
rho=F(1,10**640)
griderr=180*rho*S*Abox**3
ck('grid_error_less_than_1e_minus_7',griderr<F(1,10**7))
points_per_coordinate=2*Cbar*10**640+1
ck('points_per_coordinate_less_than_1e662',points_per_coordinate<10**662)
ck('log10_grid_cardinality_less_than_1e93',662*dim<10**93)
ck('total_target_width_less_than_1e_minus_2',F(1,1000)+spatial+griderr+F(1,1000)<F(1,100))
receipt={'status':'all rational inequalities pass','checks':checks,'parameters':{'N':str(N),'delta':str(delta),'heat_time':str(s),'K':str(K),'Cbar':str(Cbar),'grid_spacing':str(rho),'real_dimension':str(dim),'log10_grid_cardinality_upper_bound':str(662*dim)},'not_performed':['full grid enumeration','objective evaluations','storage value enclosure'], 'arithmetic':'Python standard-library Fraction and integer arithmetic; analytic Gaussian bounds detailed in RESOURCE_RECEIPT.md'}
(D/'resource_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'real_dimension':str(dim),'log10_grid_cardinality_upper_bound':str(662*dim)}))
