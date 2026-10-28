"""Replay every owned source construction; no external edits or network."""
import sys
sys.dont_write_bytecode=True
import importlib,contextlib,io,json,time
from seam_residual import BASE


def run():
    start=time.monotonic();rows=[]
    jobs=[('seam_residual','numerical_discovery'),
          ('local_multiplicative_residual','numerical_discovery'),
          ('qbp_collar','numerical_discovery'),
          ('rung_residual_budget','interval_budget'),
          ('exact_small_collar_limit','exact_source_limit'),
          ('block_purity_readout','positive_arithmetic_ansatz_enclosure'),
          ('verify_construction','exact_rational_and_independent_matrix_controls'),
          ('coarse_true_purity','coarse_actual_Gibbs_bracket')]
    for name,scope in jobs:
        tick=time.monotonic()
        with contextlib.redirect_stdout(io.StringIO()):importlib.import_module(name).run()
        rows.append(dict(job=name,scope=scope,status='REPLAYED',seconds=time.monotonic()-tick))
        print(name,scope,'REPLAYED',flush=True)
    result=dict(status='ALL_EIGHT_JOBS_REPLAYED_AT_THEIR_DECLARED_SCOPES',
        rows=rows,elapsed_seconds=time.monotonic()-start,
        writes_confined_to=str(BASE),network_required=False,
        fine_cold_purity_inputs_acquired=0,
        scope='Discovery norms/ODEs remain discovery. Exact proof/interval readout checks pass at their own scope. The actual cold brackets are far wider than the bootstrap tolerance.')
    (BASE/'results/REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
