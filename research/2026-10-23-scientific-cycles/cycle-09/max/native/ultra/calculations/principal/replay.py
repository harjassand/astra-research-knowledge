#!/usr/bin/env python3
"""Exact finite composite-D decoder admissions and final matched cost table."""
import argparse
from fractions import Fraction
from itertools import product
import json, math
from pathlib import Path
import sys, time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'search'))
from colored_search import parameters


def decoder_checks():
    cases=0; digits=0; cosets=0
    for D in [2,3,4,6]:
        for c in range(1,6):
            for Q in range(1,4):
                groups=[[i for i in range(1,c) if (i-1)%Q==color]
                        for color in range(Q)]
                groups=[g for g in groups if g]
                pivots=[g[0] for g in groups]
                free=[i for i in range(c) if i not in pivots]
                assert free[0]==0
                coset={}
                for x in product(range(D),repeat=c):
                    u=tuple(sum(x[i] for i in g)%D for g in groups)
                    y=list(x)
                    for g,p,uu in zip(groups,pivots,u):
                        y[p]=(sum(x[i] for i in g)-uu)%D
                    assert all(y[p]==0 for p in pivots)
                    z=tuple(y[i] for i in free)
                    coset.setdefault(u,set()).add(z)
                    # Explicit inverse to the unsifted coordinate map, including
                    # the translated syndrome, valid even for composite D.
                    inv=list(y)
                    for g,p,uu in zip(groups,pivots,u):
                        inv[p]=(uu-sum(inv[i] for i in g if i!=p))%D
                    assert tuple(inv)==x
                    digits+=1
                for vals in coset.values():
                    assert len(vals)==D**len(free)
                cosets+=len(coset);cases+=1
    return dict(status='PASS',integer_dimensions=[2,3,4,6],cases=cases,
                basis_vectors_checked=digits,affine_cosets_checked=cosets,
                scope='exact coefficient-one decoder/permutation; equal phases proved analytically')


def geom(u):
    return (u+1)*math.log(u+1)-u*math.log(u) if u else 0


def cost_table():
    table=[]
    for D,L,eps in [(2,2**16,Fraction(1,2**16)),
                    (2,2**20,Fraction(1,64)),
                    (2,2**20,Fraction(1,2**20)),
                    (2,2**30,Fraction(1,2**30)),
                    (6,2**20,Fraction(1,2**20))]:
        t,s,Q=parameters(L,D,eps);w=3*Q;e=float(eps)
        h=-e*math.log(e)-(1-e)*math.log1p(-e)
        R=(1-e)*math.log(L)-geom(w+1/(D-1))-h
        a=0;powD=1
        while powD*D<=L:powD*=D;a+=1
        table.append(dict(D=D,L=L,global_half_trace_error=str(eps),t=t,s=s,Q=Q,w=w,
                          source_preselected_mean_nats=(L+1)*math.log(D)/2,
                          source_deterministic_exact_nats=L*math.log(D),
                          total_local_old_memory_dimension=f'{L}*{D}^{L}',
                          lower_target_Bell_allocation_when_K_equals_L=max(1,L-w),
                          score_deficit_nats_upper=(w+e*L)*math.log(D),
                          classical_symbols_each_direction_upper=Q,
                          communication_nats_each_direction_lower=max(0,R),
                          one_way_joint_error_lower=max(0,1-(w+a+2)/L),
                          parity_controlled_adds_per_party_upper=L-1,
                          decoder_controlled_adds_per_party_upper=L-1,
                          shared_seed_bits=0,aux_entangled_supply_nats=0,
                          source_clock_access=0,
                          control_integer_operations_order='t log(L+1)',
                          control_weight_bitlength_order='t+log L',
                          physical_execution='NOT_PERFORMED'))
    return table


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,
                                                       default=Path(__file__).parent)
    out=parser.parse_args().output_dir;out.mkdir(parents=True,exist_ok=True)
    wall=time.perf_counter();cpu=time.process_time()
    result=dict(status='PASS',decoder=decoder_checks(),matched_resource_table=cost_table(),
                all_length_proof='PROOF.txt; finite checks are admissions only',
                ordinary_stock_advantage='NOT_ESTABLISHED',Bell_loss_optimality='OPEN')
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    timing=dict(wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
                quantum_hardware_calls=0,paid_compute=0,parameter_search_runs=0,
                total_discovery_inference_cost='UNKNOWN')
    (out/'TIMING.json').write_text(json.dumps(timing,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',**timing)))


if __name__=='__main__':main()
