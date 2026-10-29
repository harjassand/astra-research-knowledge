"""Local final receipt; syntax/transport is not a scientific whole review."""
from pathlib import Path
import ast,hashlib,importlib.metadata,json,platform


def main():
    root=Path(__file__).parent
    syntax=[]
    for p in sorted(root.glob('*.py')):
        ast.parse(p.read_text(),filename=str(p));syntax.append(p.name)
    rows=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.name=='FINAL_RECEIPT.json' or '__pycache__' in p.parts:continue
        raw=p.read_bytes();rows.append({'path':str(p.relative_to(root)),
             'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    dependencies=[]
    for p in (root.parent/'t_velocity_rate/hard_sphere.py',
              root.parent/'t_near_equilibrium/UNIFORM_QUERY_PROOF.md',
              root.parent/'root_complex_collision/PROOF.md'):
        dependencies.append({'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    cert=json.loads((root/'NONRADIAL_CERTIFICATE.json').read_text())
    static=json.loads((root/'STATIC_CERTIFICATE.json').read_text())
    consumer=json.loads((root/'CONSUMER.json').read_text())
    out={'status':'CONSTRUCTED_AT_DECLARED_IDEAL_REAL_SCOPE',
         'independent_whole_review_of_this_new_packet':'NOT_YET_PERFORMED',
         'row_scope':'all velocities, full angular absolute kernel, arbitrary angular source',
         'eta':'199/200','mean_nodes_bound':400,
         'source_class':'nonnegative mass1, mean0, energy3, ||(f0-M)/(M^(3/4)phi)||infty<=1/10000; known uniformly bounded evaluator',
         'continuous_output':'positive normalized approximate g_t, not exact f_t',
         'advertised_uniform_TV':'1/1000000000000',
         'sharp_analytic_TV':static['continuous_clipping_pointwise_sharp']['normalized_TV_bound'],
         'literal_fair_bit_or_float_TV_contract':'NOT_ACQUIRED',
         'practical_all_solver_advantage':'UNKNOWN; new lost the fixed transient test',
         'physical_input_qualification':'NOT_PERFORMED','historical_novelty':'UNKNOWN',
         'row_build_seconds':cert['seconds'],'static_consumer_seconds':static['seconds'],
         'new128_t1_seconds':consumer['new']['seconds'],
         'ordinary_exact128_t1_seconds':consumer['ordinary_exact_lineage']['seconds'],
         'ordinary_Gaussian128_seconds':consumer['ordinary_Gaussian']['seconds'],
         'retained_zero_cohort_nonlinear_events':True,'retained_zero_clippings':True,
         'nonlinear_word_controls':'two native gain/loss paths; not iid',
         'syntax_checked':syntax,
         'runtime':{'python':platform.python_version(),
                    **{k:importlib.metadata.version(k) for k in ('numpy','scipy','sympy','python-flint')}},
         'manifest':rows,'manifest_file_count':len(rows),
         'manifest_total_bytes':sum(x['bytes'] for x in rows),
         'read_only_dependencies':dependencies,
         'frozen_radial_note':'Only requested H=DZ notation changed after original manifest; A review binds current proof SHA4dd8a65a. No old dynamics rerun.',
         'no_stochastic_reruns_or_new_parameter_grids_after_consumer':True}
    (root/'FINAL_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('manifest','sharp_analytic_TV')},indent=2))


if __name__=='__main__':main()
