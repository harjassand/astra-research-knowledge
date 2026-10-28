"""Uniform correction-noise bounds using finite coefficient dissipation."""
from fractions import Fraction as F
from pathlib import Path
import json
from echo_compiler import EchoCompiler, Interval, interval_expr, bilinear_expr, dot, matvec
from uniform_certificate import dominate, diagonal, mm, transpose, sub, psd


def noise_certificate(compiler, metric):
    r=compiler.r
    if not psd(metric,strict=True):
        raise ValueError('Positive computational metric required')
    basis=[[F(i==j) for j in range(r)] for i in range(r)]
    gram_radii=[[interval_expr(bilinear_expr(compiler.dictionary,x,(),y),
                              compiler.records).radius for y in basis] for x in basis]
    gamma=dominate(metric,diagonal([sum(row,F(0)) for row in gram_radii]))
    zetas=[];witnesses=[]
    for i in range(compiler.q):
        t=compiler.maps[i]
        budget=sub(metric,mm(transpose(t),mm(metric,t)))
        if not psd(budget,strict=True):
            raise ValueError('This proposal routine needs strictly positive computational dissipation')
        radii=[[interval_expr(compiler.defect_expr(i,x,y),compiler.records).radius
                for y in basis] for x in basis]
        rows=[sum(row,F(0)) for row in radii]
        cols=[sum((radii[j][k] for j in range(r)),F(0)) for k in range(r)]
        d=diagonal([max(x,y) for x,y in zip(rows,cols)])
        zeta=dominate(budget,d)
        zetas.append(zeta)
        witnesses.append({'computational_dissipation':budget,
                          'entry_radius_bilinear_dominator':d,'zeta':zeta})
    cwc=dot(compiler.initial,matvec(metric,compiler.initial))
    return {'gram_uncertainty_bound':gamma,'weak_defect_uncertainty_bounds':zetas,
            'witnesses':witnesses,
            'all_word_correction_noise_bound':cwc*(gamma+max(zetas)),
            'requires_no_uniform_coefficient_gap_in_theorem':True}


def decode(x):
    if isinstance(x,dict) and 'rational' in x:return F(x['rational'])
    if isinstance(x,dict):return {k:decode(v) for k,v in x.items()}
    if isinstance(x,list):return [decode(v) for v in x]
    return x


def run():
    from run_echo_experiment import dumpable
    root=Path(__file__).resolve().parents[1]
    raw=decode(json.loads((root/'results'/'DISSIPATION_EXPERIMENT.json').read_text()))
    results=[]
    for family in ['fixtures','fixed_source_noise_sweep','fixed_source_depth_sweep']:
        for f in raw[family]:
            records={tuple(r['word']):Interval(r['interval']['lo'],r['interval']['hi'])
                     for r in f['decoded_records']}
            compiler=EchoCompiler(f['dictionary'],2,records,f['maps'])
            cert=noise_certificate(compiler,[[F(1)]])
            total=f['dissipation_certificate']['signed_remainder_bound_all_words']+cert['all_word_correction_noise_bound']
            results.append({'family':family,'g':f['slow_scale_g'],'eta':f['raw_adc_radius'],
                            'depth':f['depth'],'noise_certificate':cert,
                            'refined_all_word_total_bound':total,
                            'previous_total_bound':f['new_total_all_word_bound'],
                            'new_source_queries':0})
    (root/'results'/'DISSIPATION_NOISE_REFINEMENT.json').write_text(json.dumps(dumpable(results),indent=2)+'\n')
    print('refined',len(results),'fixtures without new source queries; main bound',
          float(results[4]['refined_all_word_total_bound']))


if __name__=='__main__':run()
