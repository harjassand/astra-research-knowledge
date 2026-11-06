"""Exact compressed outcome intervals and noncommuting postselection witness."""
import json
from pathlib import Path
from fractions import Fraction as Q
from certified_blocks import log_bounds,sqrt_bounds,serializable

ROOT=Path(__file__).resolve().parent
S=1<<128
def down(x): return Q((x.numerator*S)//x.denominator,S)
def up(x): return -down(-x)

def distribution(label,error):
    data=json.loads((ROOT/f'{label.upper()}_N64_BLOCKS.json').read_text())
    low=[Q(0)]*65; high=[Q(0)]*65
    for b in data['blocks']:
        diag=[sum(int(x)**2+int(y)**2 for x,y in zip(rr,ii)) for rr,ii in zip(b['A_re'],b['A_im'])]
        norm=sum(diag); q=Q(b['probability_count'],1<<b['probability_bits'])
        for k,d in zip(b['keep'],diag):
            index=(64-b['L'])//2+k; value=q*d/norm
            low[index]+=down(value); high[index]+=up(value)
    return low,high,[max(Q(0),v-error) for v in low],[min(Q(1),v+error) for v in high]

def main():
    records=json.loads((ROOT/'FINITE_SYSTEM_CONSTRUCTION.json').read_text())
    errors={r['label']:Q(r['certified_numerical_trace_bound']) for r in records['runs']}
    cl,ch,cpl,cph=distribution('canonical',errors['canonical'])
    wl,wh,wpl,wph=distribution('window',errors['window'])
    allowed=[k for k in range(65) if abs(64-2*k)<=16]
    plo=sum(cl[k] for k in allowed)-errors['canonical']
    phi=sum(ch[k] for k in allowed)+errors['canonical']
    assert plo>0
    td_lower=Q(0)
    for k in allowed:
        postlo=cpl[k]/phi; posthi=cph[k]/plo
        td_lower+=max(Q(0),wpl[k]-posthi,postlo-wph[k])/2
    raritylo=-log_bounds(phi)[1]/2; rarityhi=-log_bounds(plo)[0]/2
    penaltylo=Q(records['hard_window_total_free_energy_penalty_interval'][0])
    cohgap=penaltylo-rarityhi; assert cohgap>0 and td_lower>0
    inputs=json.loads((ROOT/'INPUT_MODEL.json').read_text()); gamma=Q(1,4)+Q(inputs['control'][0])
    sl,sh=sqrt_bounds(Q(984),96)
    result={'scope':'Exact rational outward bounds for the supplied N64 model; no physical model uncertainty included.',
            'canonical_window_probability':[down(plo),up(phi)],
            'rarity_free_energy_bound_interval':[down(raritylo),up(rarityhi)],
            'noncommuting_extra_free_energy_certified_lower':down(cohgap),
            'constrained_vs_postselected_trace_distance_certified_lower':down(td_lower),
            'native_H_off_window_coupling_norm_interval':[down(gamma*sl),up(gamma*sh)],
            'witness':'Classical total variation of the collective-Z outcome laws lower-bounds full state trace distance.'}
    (ROOT/'OBSERVABLE_CERTIFICATES.json').write_text(json.dumps(serializable(result),indent=2)+'\n')
    for k,v in result.items():
        if isinstance(v,Q): print(k,float(v))
        elif isinstance(v,list): print(k,[float(x) for x in v])

if __name__=='__main__': main()
