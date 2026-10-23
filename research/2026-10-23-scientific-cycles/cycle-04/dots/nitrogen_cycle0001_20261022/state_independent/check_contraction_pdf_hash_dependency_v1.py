"""Independent 60-digit scalar contraction; no imports from parent implementation.
Source decimal literals parsed line-by-line; coefficients evaluated by nested
Horner evaluation rather than einsum. Smooth exponent coefficients as printed.
"""
from pathlib import Path
import re,json,hashlib,time
import mpmath as mp
mp.mp.dps=60
D=Path(__file__).resolve().parent
start=time.monotonic()
src=D.parent/'mode_evidence/2017_numeric_assignments.txt'
values={}
for line in src.read_text().splitlines():
    # Only literal assignments, rejecting expressions and array initializations.
    m=re.fullmatch(r'\s*(En2_onn_3Asec|Eno|coeff_g|coeff_l)\((\d+(?:,\d+)*)\)\s*=\s*([-+\d.EeDd]+)\s*',line)
    if m:
        key=(m[1],tuple(map(int,m[2].split(','))))
        assert key not in values
        values[key]=mp.mpf(m[3].replace('D','E'))
N=[values['En2_onn_3Asec',(v,)] for v in range(60)]
O=[values['Eno',(w,)] for w in range(48)]
assert sum(n=='coeff_g' for n,idx in values)==108
assert sum(n=='coeff_l' for n,idx in values)==108
C={s:[[[values['coeff_'+s,(i,j,k)] for k in range(6)] for j in range(6)] for i in range(3)] for s in ['g','l']}
def evaluate(c,x,y):
    byj=[]
    for j in range(6):
        h=c[j][4]
        for k in range(3,-1,-1): h=h*y+c[j][k]
        byj.append(h+c[j][5]/y)
    h=byj[4]
    for j in range(3,-1,-1): h=h*x+byj[j]
    return h+byj[5]/x
raw=[[[evaluate(C['g' if x>=y else 'l'][i],x,y) for y in O] for x in N] for i in range(3)]
limits=[next((v for v,x in enumerate(N) if x>=y),200) for y in O]
def smooth(literal):
    a=[[row[:] for row in plane] for plane in raw]
    cross=[]
    for w,v in enumerate(limits):
        if v==59: lo,hi,targets=56,59,[58,57]
        elif v==58: lo,hi,targets=55,59,[58,57,56]
        elif 3<=v<=57: lo,hi,targets=v-3,v+2,[v+1,v,v-1,v-2]
        elif v==2: lo,hi,targets=0,4,[1,2,3]
        elif v==1: lo,hi,targets=0,3,[1,2]
        else: continue
        for i in range(3):
            low,high=a[i][lo][w],a[i][hi][w]
            def interp(q): return low+(high-low)*(N[q]-N[lo])/(N[hi]-N[lo])
            for q in targets:
                if literal and 3<=v<=57 and q==v+1:
                    assert w+1<48
                    a[i][v][w+1]=interp(q)
                    if i==0: cross.append([v,w+1])
                else: a[i][q][w]=interp(q)
    return a,cross
kb=mp.mpf('8.617333262145e-5');F=mp.mpf('96485.33212331002')
def population(E,T):
    q=[mp.exp(-(e-E[0])/(kb*T)) for e in E];z=mp.fsum(q)
    return [p/z for p in q]
def mean(E,p):return mp.fsum((e-E[0])*pi for e,pi in zip(E,p))
def row(a,T,Tv):
    p=population(N,Tv)
    events=[(v,w,p[v]*mp.exp(a[0][v][w]+a[1][v][w]/T+a[2][v][w]/T**2)/3) for v in range(60) for w in range(48)]
    total=mp.fsum(e for v,w,e in events)
    ein=mp.fsum((N[v]-N[0])*e for v,w,e in events)/total
    eout=mp.fsum((O[w]-O[0])*e for v,w,e in events)/total
    # Defined comparator, not an observed product distribution: draw reactant
    # and product independently from bound Boltzmann ladders at shared Tv.
    pin=mean(N,p);pout=mean(O,population(O,Tv))
    return dict(Ttrans_rot_K=T,Tv_N2_K=float(Tv),forward_k_cm3_s=total,reaction_weighted_N2_excitation_eV=ein,reaction_weighted_NO_excitation_eV=eout,mode_excitation_change_J_mol_forward_event=(eout-ein)*F,reaction_weighted_bath_energy_demand_J_mol_forward_event=(O[0]-N[0]+eout-ein)*F,population_fraction_v_ge_10=mp.fsum(p[10:]),reaction_fraction_v_ge_10=mp.fsum(e for v,w,e in events if v>=10)/total,nonpreferential_N2_excitation_eV=pin,nonpreferential_NO_excitation_at_Tv_eV=pout,nonpreferential_mode_change_at_Tv_J_mol=(pout-pin)*F,nonpreferential_NO_excitation_at_Tbath_eV=mean(O,population(O,T)))
rows=[]
for variant in ['literal','corrected_index']:
    a,cross=smooth(variant=='literal')
    for T,Tv in [(1700,mp.mpf('1700')),(1700,mp.mpf('1959.5075393144')),(1700,mp.mpf('2700')),(2700,mp.mpf('2700'))]:
        r=row(a,T,Tv);r['variant']=variant
        r['enhancement_over_same_QCT_thermal_population']=r['forward_k_cm3_s']/row(a,T,mp.mpf(T))['forward_k_cm3_s']
        r['original_7reaction_thermal_k_cm3_s']=mp.mpf('3e-10')*mp.exp(-mp.mpf(38000)/T)
        r['ratio_to_original_Arrhenius_not_vibrational_enhancement']=r['forward_k_cm3_s']/r['original_7reaction_thermal_k_cm3_s']
        rows.append(r)
# Compare only after independent calculation is complete.
parent=json.loads((D.parent/'state_contraction/forward_contraction.json').read_text())
errors=[]
for r in rows:
    match=next(q for q in parent['rows'] if q['variant']==r['variant'] and q['Ttrans_rot_K']==r['Ttrans_rot_K'] and abs(q['Tv_N2_K']-r['Tv_N2_K'])<1e-8)
    for k in r:
        if k in match and isinstance(r[k],mp.mpf) and match[k]!=0:
            errors.append(dict(variant=r['variant'],T=r['Ttrans_rot_K'],Tv=r['Tv_N2_K'],field=k,relative_error=abs((mp.mpf(match[k])-r[k])/r[k])))
def conv(x):
    if isinstance(x,mp.mpf):return mp.nstr(x,40)
    raise TypeError
out={'precision_decimal_digits':60,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_pdf_sha256':hashlib.sha256((D/'jp7b04442_si_002.pdf').read_bytes()).hexdigest(),'source_url':'https://ndownloader.figshare.com/files/9083011','limits':limits,'rows':rows,'max_relative_parent_disagreement':max(x['relative_error'] for x in errors),'comparison':errors,'elapsed_seconds':time.monotonic()-start}
(D/'independent_receipt.json').write_text(json.dumps(out,indent=2,default=conv))
for r in rows:
    print(r['variant'],r['Ttrans_rot_K'],r['Tv_N2_K'],*[mp.nstr(r[k],12) for k in ['forward_k_cm3_s','enhancement_over_same_QCT_thermal_population','reaction_weighted_N2_excitation_eV','reaction_weighted_NO_excitation_eV','nonpreferential_N2_excitation_eV','nonpreferential_NO_excitation_at_Tv_eV','mode_excitation_change_J_mol_forward_event']])
print('max relative disagreement',mp.nstr(out['max_relative_parent_disagreement'],8))
