"""Root exact port-level checks of candidate full compiler, read-only imports."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import hashlib,json

root=Path(__file__).resolve().parent
producer=root.parents[1]/'alternative/representation_operation_20261027'
sys.path.insert(0,str(producer))
from compiler import compile_network

def main():
    fixtures=json.loads((root/'PORT_FIXTURES.json').read_text());reports=[]
    for case in fixtures:
        out=compile_network(case['input'])
        assert out['status']=='EXACT',out
        assert F(out['partition'])==F(case['oracle']['exact_partition'])
        expected=case['oracle']['normalized_original_bit_weights']
        if expected is None:
            assert out['normalized_edge_weights'] is None
        else:
            assert [[F(x) for x in r] for r in out['normalized_edge_weights']]==[[F(x) for x in r] for r in expected]
        reports.append({'scope':case['scope'],'oracle_partition':case['oracle']['exact_partition'],'compiler_output':out,'status':'PASS'})
    files=['compiler.py','fields.py','fisher.py','local_recognition.py','modular.py']
    result={'status':'PASS','scope':'four root rational port fixtures; original exhaustive truth',
      'source_sha256':{p:hashlib.sha256((producer/p).read_bytes()).hexdigest() for p in files},
      'reports':reports}
    (root/'INTEGRATION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'source_sha256':result['source_sha256'],
      'cases':[{'scope':r['scope'],'Z':r['oracle_partition'],'accepted_primes':len(r['compiler_output']['accepted_prime_certificates']),'rejected_primes':len(r['compiler_output']['rejected_primes'])} for r in reports]}))

if __name__=='__main__':main()
