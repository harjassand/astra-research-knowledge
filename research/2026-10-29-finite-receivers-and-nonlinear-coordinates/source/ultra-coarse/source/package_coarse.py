"""Expose ONLY the promised coarse observation/actuator contract."""
import csv,hashlib,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent


def main():
    tic=time.perf_counter();m=json.loads((HERE/'MODEL.json').read_text())
    keep=['NCO','NO2','COcoverage','Ocoverage','CO2hit']+[f'Tv{v}' for v in range(m['sites']+1)]
    with (HERE/'BASELINE_HIST.csv').open() as f,(HERE/'BASELINE_COARSE.csv').open('w') as g:
        r=csv.DictReader(f);w=csv.DictWriter(g,fieldnames=keep);w.writeheader()
        for row in r:w.writerow({k:row[k] for k in keep})
    c=dict(sites=m['sites'],horizon_seconds=m['horizon_seconds'],
       gas_activity_upper=m['gas_activity_upper'],
       source_graph='PAIR_GRAPH.json',
       source_model_sha256=hashlib.sha256((HERE/'MODEL.json').read_bytes()).hexdigest(),
       rates_scope='ONLY two calibrated adsorption coefficients; background reaction/diffusion/desorption rates excluded',
       observational_scope='adsorption marks, two endpoint coverages, separately supplied CO2-reaction path flag, total-vacancy residence histogram; no site labels or pair activity',
       row_count=20000,coarse_data_sha256=hashlib.sha256((HERE/'BASELINE_COARSE.csv').read_bytes()).hexdigest(),
       package_seconds=time.perf_counter()-tic)
    (HERE/'COARSE_CONTRACT.json').write_text(json.dumps(c,indent=2)+'\n')
    print(json.dumps(c,indent=2))


if __name__=='__main__':main()
