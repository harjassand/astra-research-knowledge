"""Independent guard checks; no future-control verification is implied."""
import copy,hashlib,json
from pathlib import Path
from compile_affine_source import compile_affine
from acquire_affine_pauli_consumer import acquire_classical_coupling

def run():
    raw={'n':2,'F_columns':[2,1],'G_columns':[1,0,1],'offset':2}
    r=compile_affine(raw)
    def term(sx=1,sz=0,x=0,z=0,c='1'):
        return dict(system_x=sx,system_z=sz,source_x=x,source_z=z,coefficient=c)
    def call(ts):return acquire_classical_coupling(raw,r,dict(system_qubits=1,terms=ts))
    accepts=rejects=0
    for z in range(4):
        out=call([term(z=z)])
        assert out['source_diagonal_coupling_verified'] is True
        assert out['future_control_instrument_algebra_verified'] is False
        assert out['original_coin_records_preserved'] is False
        assert out['arbitrary_original_quantum_dilation_preserved'] is False
        accepts+=1
    for x in [1,2,3]:
        for z in range(4):
            try:call([term(x=x,z=z,c='1/'+str(1<<300))])
            except ValueError:rejects+=1
            else:raise AssertionError('Tiny but nonzero coherence term accepted')
    # Exact cancellation is performed across the entire identical Pauli key.
    ts=[term(x=3,z=2,c='1/3'),term(x=3,z=2,c='1/6'),term(x=3,z=2,c='-1/2'),term(z=1,c='7/9')]
    out=call(ts);assert len(out['original_terms'])==1 and out['original_terms'][0]['coefficient']=='7/9';accepts+=1
    for ts in [[term(x=1),term(x=1,sz=1,c='-1')],
               [term(x=1),term(x=1,z=1,c='-1')],
               [term(sx=0,x=1)]]:
        try:call(ts)
        except ValueError:rejects+=1
        else:raise AssertionError('Distinct Pauli or source-only coherence accepted')
    out=call([]);assert out['original_terms']==[];accepts+=1
    for bad in [None,[],dict(r,original_coin_records_preserved=True),dict(r,arbitrary_original_quantum_dilation_preserved=True)]:
        try:acquire_classical_coupling(raw,bad,dict(system_qubits=1,terms=[]))
        except ValueError:rejects+=1
        else:raise AssertionError('Invalid realization accepted')
    root=Path(__file__).parent
    result={'wrapper_sha256':hashlib.sha256((root/'acquire_affine_pauli_consumer.py').read_bytes()).hexdigest(),
            'valid_diagonal_or_exact_cancellation_cases':accepts,'invalid_coherence_or_realization_cases':rejects,
            'future_control_verification_flag_remains_false':True,'passed':True}
    path=root/'guarded_consumer_independent_checks.json';path.write_text(json.dumps(result,indent=2)+'\n');print(path.read_text())

if __name__=='__main__':run()
