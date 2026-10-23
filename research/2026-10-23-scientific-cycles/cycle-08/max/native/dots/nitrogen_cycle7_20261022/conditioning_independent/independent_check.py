"""Independent high-precision quadrature in original conversion coordinate.
Does not import or execute the parent algorithm. Conditional model check only.
"""
from pathlib import Path
import json, hashlib
import mpmath as m
m.mp.dps=70
root=Path(__file__).resolve().parents[1]
raw=(root/'oxidation_operation/input.json').read_bytes()
inputs=json.loads(raw); parent=json.loads((root/'oxidation_operation/result.json').read_text())
M=m.mpf
F0=M(inputs['standard_flow_L_min'])/M(inputs['declared_standard_molar_volume_L_mol'])/60
k=M(inputs['event_k_cm6_molecule2_s'])*M(inputs['Avogadro'])**2/M('1e12')
c=M(inputs['pressure_Pa'])/(M(inputs['R_J_mol_K'])*M(inputs['T_K']))
eps=M('0.0001')
def volume(a,b,x,partition):
    # partition(z) is fraction of oxidized nitrogen residing in N2O4.
    def integrand(z):
        f=1-a*z/2-partition(z)*a*z/2
        no= c*a*(1-z)/f
        oxygen=c*(b-a*z/2)/f
        sink=2*k*no**2*oxygen
        return 1000*F0*a/sink
    breaks=sorted(set([M(0),x]+[M(t) for t in ['0.5','0.9','0.95','0.98','0.99'] if M(t)<x]))
    return m.quad(integrand,breaks)
rows=[]
for pr in parent['rows']:
    a=M(pr['initial_NO_fraction']);b=M(inputs['oxygen_feed_fraction'])-a/2
    x=(a-eps)/(a*(1-eps)) if pr['target_type']=='common_NO_slip_100ppm' else M(str(pr['conversion']))
    vdim=volume(a,b,x,lambda z:M(1));vmono=volume(a,b,x,lambda z:M(0))
    # Non-equilibrium, oscillating admissible partition, not a physical equilibrium claim.
    vmix=volume(a,b,x,lambda z:(1+m.sin(29*z))/2)
    lo,hi=map(lambda v:M(str(v)),pr['PFR_volume_L_evaluated_k_bracket'])
    assert lo<vdim<vmix<vmono<hi
    cstr=[]
    for s in [M(1),M('.5')]:
        f=1-s*a*x
        sink=2*k*(c*a*(1-x)/f)**2*(c*(b-a*x/2)/f)
        cstr.append(1000*F0*a*x/sink)
    for v,reported in zip(cstr,pr['CSTR_volume_L_evaluated_k_bracket']):
        assert abs(v-M(str(reported)))/v<M('1e-14')
    row=dict(configuration=pr['configuration'],target_type=pr['target_type'],conversion=float(x),direct_quadrature_L=[float(vdim),float(vmono)],oscillatory_partition_L=float(vmix),parent_enclosure_L=[float(lo),float(hi)],enclosure_pass=True,CSTR_direct_L=list(map(float,cstr)),minimum_oxygen_molar_flow_ratio=float(b-a*x/2),maximum_NO_ppm=float(1e6*a*(1-x)/(1-a*x)))
    if pr['target_type']=='common_NO_slip_100ppm':
        xmono=(a-eps)/(a*(1-eps/2))
        row['no_dimer_exact_100ppm_conversion']=float(xmono)
        row['no_dimer_exact_100ppm_volume_L']=float(volume(a,b,xmono,lambda z:M(0)))
    rows.append(row)
comparisons=[]
for i in range(3):
    ordinary=rows[i];split=rows[i+3]
    comparisons.append({'target_type':ordinary['target_type'],'conversion_label':ordinary['conversion'] if i<2 else 'robust_100ppm','matched_all_dimer_split_over_ordinary':split['direct_quadrature_L'][0]/ordinary['direct_quadrature_L'][0],'matched_no_dimer_split_over_ordinary':split['direct_quadrature_L'][1]/ordinary['direct_quadrature_L'][1],'independent_partition_ratio_bracket':[split['direct_quadrature_L'][0]/ordinary['direct_quadrature_L'][1],split['direct_quadrature_L'][1]/ordinary['direct_quadrature_L'][0]]})
result={'input_sha256':hashlib.sha256(raw).hexdigest(),'method':'70-decimal mpmath adaptive tanh-sinh quadrature in original X; species-flow-derived chemical sink; no parent import','F0_mol_s':float(F0),'event_k_m6_mol2_s':float(k),'C_mol_m3':float(c),'all_checks_pass':True,'rows':rows,'comparisons':comparisons,'caveat':'Numerical cross-check is not itself a rigorous enclosure or physical confidence bound; parent exact-rational monotone construction supplies its mathematical enclosure.'}
(root/'conditioning_independent/result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
