"""Deterministic exact software oracles, not a recognition/novelty benchmark.
The ordinary comparator retains the SAME generator and all hidden gauge work.
Compiler receives only the dense tensors/embedding, never that work or answer.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,time,sys
from itertools import product
from compiler import compile_network
from local_recognition import clear_input
from modular import stage
from fisher import topology
R=Path(__file__).resolve().parent
SOURCE=R.parent/'hidden_representation_comparator_20261027/finite_field_gate_check.py'
ns={'__name__':'ordinary_test_generator','__file__':str(SOURCE)}
exec(compile(SOURCE.read_text(),str(SOURCE),'exec'),ns)


def instance(k,odd=False,perturb=False):
    rotation,edges=ns['prism'](k);base,dense=ns['tensors'](rotation,edges,odd,perturb)
    return {'name':f'signed_prism{k}_odd{odd}_perturb{perturb}',
            'tensors':[[dense[v][bits] for bits in ns['BITS']] for v in range(2*k)],
            'edges':[[v,rotation[v].index(w),w,rotation[w].index(v)] for v,w in edges]}


def direct(data):
    ts,Ds,ports,H=clear_input(data);E=len(data['edges']);total=0;pins=[0]*(2*E)
    for state in product(range(2),repeat=E):
        val=1
        for v,T in enumerate(ts):
            bits=[state[eid] for eid,w,j in ports[v]];val*=T[4*bits[0]+2*bits[1]+bits[2]]
        total+=val
        for eid,b in enumerate(state):pins[2*eid+b]+=val
    den=1
    for d in Ds:den*=d
    return total,pins,Q(total,den)


def main():
    started=time.perf_counter();checks=[]
    for odd in (False,True):
        data=instance(3,odd);tag='ODD' if odd else 'EVEN';(R/f'INPUT_SIGNED6_{tag}.json').write_text(json.dumps(data,indent=2)+'\n')
        z,pins,partition=direct(data);out=compile_network(data,200,True)
        (R/f'OUTPUT_SIGNED6_{tag}.json').write_text(json.dumps(out,indent=2)+'\n')
        assert out['status']=='EXACT',out
        assert Q(out['partition'])==partition,(out['partition'],partition)
        if z:
            got=[[Q(x) for x in row] for row in out['normalized_edge_weights']]
            expected=[[Q(pins[2*i],z),Q(pins[2*i+1],z)] for i in range(len(data['edges']))]
            assert got==expected,(got,expected)
            assert not out['normalized_weights_are_probabilities']
            ts,Ds,ports,H=clear_input(data);top=topology(len(ts),data['edges'])
            good=out['accepted_prime_certificates'][0]['prime']
            flipped=stage(ts,data['edges'],ports,top,good,True,branch_flips=[0,2,5])
            assert flipped['residue']==z%good
            if flipped['pin_residues'] is not None:assert flipped['pin_residues']==[p%good for p in pins]
        else:
            assert out['normalized_edge_weights'] is None and any(pins)
        checks.append({'case':tag,'partition':str(partition),'direct_assignments':1<<len(data['edges']),'original_edge_pin_integer_pairs':[pins[2*i:2*i+2] for i in range(len(data['edges']))],
                       'compiler_exact':True,'accepted_primes':len(out['accepted_prime_certificates']),'rejected_primes':len(out['rejected_primes']),'wall_s_compiler':out.get('wall_seconds_including_recognition'),'zero_partition_pins_not_falsely_zeroed':not z})
        print(json.dumps({k:v for k,v in checks[-1].items() if k!='original_edge_pin_integer_pairs'}),flush=True)
    perturb=instance(3,False,True);out=compile_network(perturb,30,False);assert out['status']=='UNKNOWN'
    checks.append({'case':'parity_breaking_perturbation','compiler_status':out['status'],'warning':'failure is NOT hardness or absence of all other tractability'})
    budget=compile_network(instance(3),0,True);assert budget['status']=='UNKNOWN';checks.append({'case':'zero_prime_budget','status':'UNKNOWN; no partial CRT answer'})
    report={'scope':'exact integration checks only; generated hidden gauges are NOT evidence of novelty or comparator advantage','source_generator':str(SOURCE),'source_generator_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'checks':checks,'selected_check_wall_s':time.perf_counter()-started,'ordinary_alternative_has_generator_and_gauges':True}
    (R/'INTEGRATION_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
