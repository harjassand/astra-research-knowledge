"""Execute fixed-design native source acquisition, retaining public raw data."""
from pathlib import Path
import hashlib,json,time
import numpy as np
from private_source import sample_port

ROOT=Path(__file__).resolve().parent
N=2**20
TICK_SCALE=2**20

def main():
    import sys
    kind='macro' if '--macro' in sys.argv else 'original'
    m=6 if kind=='macro' else 4
    outdir=ROOT/'macro_run' if kind=='macro' else ROOT
    outdir.mkdir(exist_ok=True)
    started=time.perf_counter(); rows=[]; raw={}
    for port in range(m):
        endpoint,ticks,cost=sample_port(port,N,7341029+port*191+(900000 if kind=='macro' else 0),kind=kind)
        # Each partial integer sum fits uint64 even in the worst case;
        # Python integer accumulation prevents overflow across blocks.
        total_ticks=sum(int(ticks[j:j+1024].sum(dtype=np.uint64)) for j in range(0,N,1024))
        total_squared=0
        for j in range(0,N,1024):
            x=ticks[j:j+1024].astype(np.uint64)
            total_squared+=int((x*x).sum(dtype=np.uint64))
        rows.append({'port':port,'n':N,
            'endpoint_counts':[int(np.sum(endpoint==j)) for j in range(m)],
            'pending_count':int(np.sum(endpoint<0)),
            'sum_ticks':str(total_ticks),'sum_squared_ticks':str(total_squared),
            'raw_sha256':hashlib.sha256(endpoint.tobytes()+ticks.tobytes()).hexdigest(),
            'cost':cost})
        raw[f'endpoint_{port}']=endpoint; raw[f'ticks_{port}']=ticks
    record={
        'schema':'astra.native_boundary_excursion_record.v1',
        'port_count':m,'horizon':24,'tick_scale':TICK_SCALE,
        'contracts':{
            'source':'finite irreducible reversible continuous-time Markov source',
            'port_holding_rate':'1',
            'hidden_excursion_tail':'Pr(sigma>t) <= exp(-t/2), every prepared port',
            'timestamp_absolute_allowance':'1/524288',
            'resolved_individual_ports':True,
            'independent_exact_port_resets':'supplied operational capability',
            'coarse_readout':'next port identity or still outside at H; no restart on outside',
            'clock_and_tail_status':'supplied warranties, not inferred from finite counts',
            'software_sampling':'individual PCG64 trajectories; ideal IID draws are a theorem premise',
        },
        'rows':rows,
        'execution_wall_seconds':time.perf_counter()-started,
        'scope':'synthetic execution, no equipment operation; no hidden state count or generator in learner input',
    }
    if kind=='macro':
        record['contracts']['module_ports']=[[0,1],[2,3],[4,5]]
        record['contracts']['module_separation']='Every cross-module edge has two resolved port endpoints; an interior excursion remains in its departure module.'
    (outdir/'NATIVE_EXCURSION_RECORD.json').write_text(json.dumps(record,indent=2)+'\n')
    np.savez_compressed(outdir/'NATIVE_EXCURSION_RAW.npz',**raw)
    print(json.dumps({'trials':m*N,'native_jumps':sum(r['cost']['total_native_jumps'] for r in rows),
        'native_time':sum(r['cost']['elapsed_native_time'] for r in rows),
        'pending':sum(r['pending_count'] for r in rows),
        'wall_seconds':record['execution_wall_seconds'],
        'raw_bytes':(outdir/'NATIVE_EXCURSION_RAW.npz').stat().st_size},indent=2))

if __name__=='__main__': main()
