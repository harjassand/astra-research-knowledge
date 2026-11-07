from fractions import Fraction as Q
from pathlib import Path
from time import perf_counter
import json,hashlib
import numpy as np
from exact import encode, require
from native import NativePort
from acquire import acquire
from game import ProtocolGame,COMMANDS,REQUESTS,DEADLINE,observe,SCALE,ANALOG_THRESHOLD

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
def save(name,x):
    (OUT/name).write_text(json.dumps(encode(x),indent=2,sort_keys=True)+'\n')

def main():
    start=perf_counter();port=NativePort();native_prepare=perf_counter()-start
    start=perf_counter();learned=acquire(port);acq_time=perf_counter()-start
    save('ACQUISITION.json',learned)
    save('NATIVE_ACQUISITION_COST.json',port.costs())
    start=perf_counter();game=ProtocolGame(learned['G']);crit=game.critical()
    eps=learned['epsilon'];star=crit['critical_radius']
    # A dyadic reader budget strictly inside the sound side of the interval.
    r=Q((int((star-2*eps)*4096)),4096)
    require(r>0)
    winning=game.solve(r+eps,True);wv=game.verify(winning)
    rfail=Q(int((star+2*eps)*4096)+1,4096)
    losing=game.solve(rfail-eps,True);lv=game.verify(losing)
    require(winning['initial_winning'] and not losing['initial_winning'])
    synth_time=perf_counter()-start
    save('MODEL.json',{'G':learned['G'],'epsilon':eps,'m':game.m,'h':learned['h'],
                       'lead':learned['lead'],'command_alphabet':COMMANDS,'quantizer_threshold_code':Q(1,2),
                       'exact_analogue_comparator_boundary':ANALOG_THRESHOLD,
                       'request_alphabet':REQUESTS,'deadline_ticks':DEADLINE,
                       'reader_radius':r,'nominal_game_radius':r+eps,
                       'failing_reader_radius':rfail,'nominal_losing_radius':rfail-eps})
    save('CRITICAL_NOISE.json',dict(crit,source_optimal_radius_lower=max(Q(0),star-eps),
                                  source_optimal_radius_upper=star+eps))
    save('GAME_CERTIFICATE.json',{'winning':{k:v for k,v in winning.items() if k in ('radius','initial_winning','winning_states','total_states','iterations')},
                                'losing':{k:v for k,v in losing.items() if k in ('radius','initial_winning','winning_states','total_states','iterations')},
                                'winning_audit':wv,'losing_audit':lv,
                                'legal_suffixes':game.M,'all_length_four_words':7**4,
                                'build_signed_products':game.build_mults,'build_additions':game.build_adds,
                                'game_solves':game.solve_calls,'fixed_point_rounds':game.total_rounds,
                                'counted_core_boolean_operations':game.boolean_checks,
                                'whole_fixed_point_boolean_operation_upper':100*game.total_rounds*game.M*6*DEADLINE*7,
                                'policy_entries':winning['policy'].size,'policy_entry_bits':3,
                                'max_abstract_word_prediction_integer_bits':max(abs(v).bit_length() for y in game.pred for v in y)})
    save('POLICY.json',{'words':game.words,'policy':winning['policy'].tolist(),
                        'winning':winning['W'].astype(int).tolist(),'rank':winning['rank'].tolist()})
    # The source continues from acquisition. Only finite relaxation is applied.
    before=port.costs();start=perf_counter()
    s=game.initial;target=0;k=DEADLINE-1;completed=0;age=0
    a=int(winning['policy'][s,target,k])
    port.advance((0,0,0),learned['W'])
    transcript=[];request_counter=0;max_age=0
    while completed<120:
        require(a>=0)
        port.advance(COMMANDS[a],learned['h']-learned['lead'])
        raw=port.read(REQUESTS[target],r)
        o=observe(raw);sp=int(game.next[s,a]);require(sp>=0)
        cols=winning['allowed'][sp]
        require(all(v in col for v,col in zip(o,cols)))
        require(sum(v!=0 for v in o)<=1)
        axis,sign=REQUESTS[target];served=o[axis]==sign
        age+=1
        transcript.append({'step':len(transcript),'request':target,'remaining':k+1,'suffix':s,
                           'action':a,'read_integers':raw,'observation':o,'served':served,'next_suffix':sp})
        s=sp
        if served:
            max_age=max(max_age,age);age=0;completed+=1
            # A deterministic, declared hostile request sequence, not a proof of
            # the universal request claim (which is supplied by the game audit).
            request_counter+=1
            target=(5*request_counter+request_counter//7+request_counter//13)%6
            k=DEADLINE-1
        else:
            require(k>0);k-=1
        require(winning['W'][s,target,k])
        next_a=int(winning['policy'][s,target,k]) if completed<120 else None
        # The old command stays in effect while the next decision is computed.
        # This positive window is part of the calibrated time contract.
        port.advance(COMMANDS[a],learned['lead'])
        if next_a is not None:a=next_a
    use_time=perf_counter()-start
    save('TRANSCRIPT.json',transcript)
    rawbytes=(OUT/'TRANSCRIPT.json').read_bytes()
    scalar_reads=3*len(transcript)
    # Measured values exceed threshold despite the entire declared error.
    service_bound=ANALOG_THRESHOLD-r
    save('EXECUTION.json',{'status':'PASS','completed_requests':completed,'sampled_intervals':len(transcript),
                          'vector_reads':len(transcript),'scalar_reads':scalar_reads,
                          'maximum_request_delay_ticks':max_age,'deadline_ticks':DEADLINE,
                          'service_time_upper_source_units':DEADLINE*learned['h'],
                          'deployment_relaxation_time':learned['W'],
                          'deployment_active_time':len(transcript)*learned['h'],
                          'total_deployment_time':learned['W']+len(transcript)*learned['h'],
                          'certified_true_target_signed_output_at_every_acknowledgement':service_bound,
                          'certified_true_target_signed_output_at_command_boundary':service_bound-7*learned['lead'],
                          'read_to_command_computation_window':learned['lead'],
                          'reader_radius':r,'minimum_guaranteed_noise_margin_below_optimum':star-eps-r,
                          'source_absolute_supply_bound':4*(learned['W']+len(transcript)*learned['h']),
                          'force_L2_cap':Q(2),'force_slew_L2_cap':Q(32),
                          'online_hidden_reads':0,'online_policy_lookups':len(transcript),
                          'online_scalar_threshold_comparisons_upper':6*len(transcript),
                          'online_controller_nontrivial_real_arithmetic':0,
                          'controller_small_integer_operations_bound_per_round_excluding_table_access':500,
                          'sequential_table_bit_operation_bound_per_round':(6*winning['policy'].size+100)*55**2,
                          'serial_bit_rate_sufficient_for_this_conservative_bound':Q((6*winning['policy'].size+100)*55**2)/learned['lead'],
                          'deadline_hardware_status':'software throughput measured; no physical WCET or supply-device calibration claimed',
                          'transcript_sha256':hashlib.sha256(rawbytes).hexdigest(),
                          'scope':'one executed adversarial software history; all histories are covered by the separate mathematical game certificate'})
    save('NATIVE_TOTAL_COST.json',port.costs())
    save('RUNTIME.json',{'native_preparation_seconds':native_prepare,'acquisition_seconds':acq_time,
                         'synthesis_and_game_verification_seconds':synth_time,'deployment_seconds':use_time})
    print(json.dumps(encode({'epsilon':eps,'critical':crit,'reader_radius':r,'failing_radius':rfail,
                             'suffix_states':game.M,'states':winning['total_states'],
                             'winning_states':winning['winning_states'],'rounds':len(transcript),
                             'max_delay':max_age,'native_prepare_seconds':native_prepare,
                             'synthesis_seconds':synth_time,'use_seconds':use_time}),indent=2))

if __name__=='__main__':main()
