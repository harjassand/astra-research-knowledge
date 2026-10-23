"""One fixed nine-column symmetry-aware identifiability construction/replay.

The nine directions already occur in the stored 512-column transcript.
No matrix action, new probe, Krylov step or reconstruction is computed here.
"""
import time
START=time.perf_counter()
CPU=time.process_time()
from pathlib import Path
import argparse
import json
import resource
import numpy as np
from check_sparse_identifiability import (load,sha,require,is_prime_exact,PRIME,
                                         rank_witness,verify_selected_minor)


def main():
    ap=argparse.ArgumentParser()
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--construct',action='store_true')
    group.add_argument('--verify',action='store_true')
    ap.add_argument('--owner',type=Path,default=Path(__file__).resolve().parents[2]/'restore_pro2')
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    pp=root/'results/sparse_degeneracy_preliminary.json'
    cp=root/'results/symmetric_sparse_identifiability_certificate.json'
    x,supports,facts=load(args.owner)
    x=x[:,:9].copy()
    facts={**facts,'q':9,'max_original_row_support':facts['max_row_support'],
           'last_column_probe_depth':[0,1],
           'stored_column_indices':list(range(9)),
           'prefix_loading_note':'Shared loader materializes the original339-column prefix before slicing9; this cost is included.'}
    peeling=json.loads(pp.read_text())
    order=peeling['order'];n=facts['n']
    require(sorted(order)==list(range(n)),'peeling permutation')
    require(peeling['degeneracy']==8,'fixed admitted degeneracy')
    require(all(i in s for i,s in enumerate(supports)),'all graph diagonals present')
    g=[set(s)-{i} for i,s in enumerate(supports)]
    require(is_prime_exact(PRIME),'prime check')
    require((PRIME-1)**2<2**63,'int64 arithmetic guard')
    if args.verify:
        cert=json.loads(cp.read_text())
        require(cert['schema']=='symmetric-pattern-peeling-identifiability-v1','schema')
        require(cert['prime']==PRIME and cert['peeling_order_sha256']==sha(pp),'modulus/order binding')
        for k,v in facts.items():
            if not k.endswith('_seconds'):require(cert['facts'][k]==v,'source facts: '+k)
        require(cert['failed_vertices']==[] and len(cert['steps'])==n,'complete success certificate')
    else:
        require(not cp.exists(),'refuse overwrite of existing construction')
    live=[True]*n;degree=list(map(len,g));rows=[];cliques=[]
    started=time.perf_counter()
    for step,i in enumerate(order):
        require((degree[i],i)==min((degree[j],j) for j in range(n) if live[j]),
                'minimum degree/tie rule mismatch')
        remaining=sorted(j for j in g[i] if live[j])
        require(len(remaining)==degree[i]==peeling['remaining_degrees'][step],'saved remaining degree')
        local=sorted([i]+remaining)
        require(len(local)<=9,'prescribed nine columns insufficient')
        if len(local)==9 and all(v in g[u] for pos,u in enumerate(local) for v in local[pos+1:]):
            cliques.append(local)
        if args.construct:
            witness=rank_witness(x[local,:],PRIME)
            rows.append({'step':step,'vertex':i,'support':local,**witness})
        else:
            w=cert['steps'][step]
            require(w['step']==step and w['vertex']==i and w['support']==local,'local support binding')
            verify_selected_minor(x,local,w,PRIME)
        live[i]=False
        for j in g[i]:
            if live[j]:degree[j]-=1
    algebra_seconds=time.perf_counter()-started
    # Every9-clique's earliest peeled vertex has eight later neighbors, so this
    # bounded candidate test is complete for9-cliques in a degeneracy8 order.
    first_clique=cliques[0] if cliques else None
    if args.construct:
        failed=[r['vertex'] for r in rows if r['rank_mod_prime']!=len(r['support'])]
        cert={'schema':'symmetric-pattern-peeling-identifiability-v1','prime':PRIME,
              'facts':facts,'peeling_order_sha256':sha(pp),'steps':rows,
              'failed_vertices':failed,'first_nine_clique':first_clique,
              'number_nine_cliques_found':len(cliques)}
        cp.write_text(json.dumps(cert,separators=(',',':'))+'\n')
        receipt={'PASS':not failed,'mode':'construct','failed_vertices':failed,
                 'attempt_count':1,'construction_and_order_checks_wall_seconds':algebra_seconds}
    else:
        require(cert['first_nine_clique']==first_clique,'clique witness consistency')
        require(cert['number_nine_cliques_found']==len(cliques),'clique count consistency')
        receipt={'PASS':True,'mode':'verify','all_elimination_steps_checked':n,
                 'declared_minor_and_order_verification_wall_seconds':algebra_seconds}
    receipt.update({'facts':facts,'prime':PRIME,'first_nine_clique':first_clique,
                    'number_nine_cliques_found':len(cliques),
                    'exact_identification_query_count_if_nine_clique':9 if first_clique else None,
                    'certificate_bytes':cp.stat().st_size,'certificate_sha256':sha(cp),
                    'wall_seconds_including_imports':time.perf_counter()-START,
                    'cpu_seconds_including_imports':time.process_time()-CPU,
                    'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                    'not_claimed':['stable recovery','CDF accuracy lower bound','spectral speedup','new matrix actions already computed']})
    out=root/'results'/('symmetric_sparse_identifiability.json' if args.construct else 'symmetric_sparse_identifiability_replay.json')
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
