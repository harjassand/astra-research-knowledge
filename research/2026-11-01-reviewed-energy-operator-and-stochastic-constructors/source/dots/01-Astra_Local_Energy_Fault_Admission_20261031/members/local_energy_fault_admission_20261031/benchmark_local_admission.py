"""Reproducible classical acquisition costs, not hardware or simulator costs."""
import copy,json,time,platform,sys
from pathlib import Path
from fractions import Fraction
import acquire_local_admission as m
from test_acquire_local_admission import fixture,million
HERE=Path(__file__).parent

def maxbits(x):
    if type(x) is int:return max(1,abs(x).bit_length())
    if type(x) is list:return max(map(maxbits,x),default=0)
    if type(x) is dict:return max(map(maxbits,x.values()),default=0)
    return 0

def large_explicit(n=10000):
    s=million();s['task']['id']='explicit-ten-thousand-source-chain-inspection'
    s['source_model']={'mode':'explicit','sources':[
        {'loss_lower':[1000000000,1],'injection_upper':[1,1]} for _ in range(n)],
        'hopping':[{'i':i,'j':i+1,'real':[100000000,1],'imag':[0,1]} for i in range(n-1)]}
    s['couplings'][0]['source']=n//2
    return s

def run():
    rows=[]
    for name,spec in [('explicit_four',fixture()),('symbolic_million',million()),('explicit_ten_thousand',large_explicit())]:
        start=time.perf_counter();cert=m.acquire(spec);elapsed=time.perf_counter()-start
        start=time.perf_counter();verified=m.verify_admitted(spec,cert);vtime=time.perf_counter()-start
        eta=Fraction(*cert['certificate']['eta_upper'])
        row={'name':name,'status':cert['status'],'full_external_verify':verified,
             'acquisition_seconds':elapsed,'verification_seconds':vtime,
             'input_canonical_bytes':len(m.canonical(spec).encode()),
             'certificate_canonical_bytes':len(m.canonical(cert).encode()),
             'input_max_integer_bits':maxbits(spec),'certificate_max_integer_bits':maxbits(cert),
             'eta_upper_exact':m.pair(eta),'eta_upper_decimal_diagnostic':float(eta),
             'source_qubits':cert['resources']['source_qubits'],
             'explicitly_inspected_sources':cert['resources']['explicitly_inspected_sources'],
             'explicitly_inspected_edges':cert['resources']['explicitly_inspected_edges'],
             'raw_integrated_hamiltonian_amplitude_upper':cert['comparators']['raw_integrated_hamiltonian_amplitude_upper'],
             'input_sha256':m.digest(spec),'certificate_sha256':m.digest(cert)}
        rows.append(row)
    return {'scope':'Classical exact rational input acquisition and recomputation only; timing is diagnostic and platform-dependent. No gates, physical rates or FT architecture executed.',
            'python':sys.version.split()[0],'platform':platform.platform(),'rows':rows}
if __name__=='__main__':
    data=run();print(json.dumps(data,indent=2))
    (HERE/'local_admission_benchmark.json').write_text(json.dumps(data,indent=2)+'\n')
