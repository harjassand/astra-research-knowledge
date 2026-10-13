"""Propagate accepted physical leakage/cavity through repeated actual maps.

No EOL code projection. Pump remains on between G106 cycles; there is no GF
echo. The ancilla comparison is the same favorable finite-pulse abstraction
in alternative_control_gates.py, not experimental accepted-Choi data.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse
import json
import time
import numpy as np
import binned_record_test as r
import alternative_control_gates as c
ROOT=Path(__file__).resolve().parent


def main():
    start=time.perf_counter()
    parser=argparse.ArgumentParser();parser.add_argument('--cycles',type=int,default=8)
    parser.add_argument('--nf',type=int,default=16);parser.add_argument('--nfreq',type=int,default=80)
    parser.add_argument('--output',default='REPEATED_RESULTS.json')
    args=parser.parse_args()
    r.f.ecr.MEASURED_HALF_GE_CAVITY_SHIFT_MHZ=.5
    g=r.f.ecr.calibrate_g()
    model=r.f.make_model(args.nf,2503.,217.28013507543088,g)
    rows,receiver=r.f.schedule(model,3.,5.,.8,24,8)
    receiver['carrier_ladder_amplitude']=[float(a[0,1].real) for a in model['carrier']]
    bins,_=r.bin_receivers(rows,receiver,1,.02)
    value=r.initial_state(args.nf);record=[]
    # Full9x9 data map, including residual e, from the finite SWAP comparator.
    A,_=c.ancilla_cycle(3.8,initial=np.eye(9,dtype=complex))
    avalue=c.prep(3);ancilla=[]
    for cycle in range(1,args.cycles+1):
        for group,threshold in bins:
            value,_=r.accepted_bin(model,value,group,receiver['probe_MHz'],threshold,args.nfreq)
        m=r.metrics(value,args.nf);record.append({'cycle':cycle,'elapsed_us':3.8*cycle,'metrics':m})
        avalue=A@avalue;ancilla.append({'cycle':cycle,'metrics':c.channel_metrics(avalue,3)})
        print(json.dumps({'cycle':cycle,'record':m,'ancilla':ancilla[-1]['metrics']}),flush=True)
    result={'status':'REPEATED_ACCEPTED_PHYSICAL_MAPS_NO_END_OF_LINE_PROJECTOR',
            'arguments':vars(args),'runtime_seconds':time.perf_counter()-start,
            'G106_record_cycles':record,'finite_SWAP_ancilla_comparator_cycles':ancilla,
            'scope':'Fixed3.8us no-echo cycles. Code/erasure populations and cavity density are retained into next direct-readout cycle; ancilla is reset as part of its measured syndrome SWAP. No acquired noise at proposed G106 bias, no full pump-on/off instrument, no matched experimental Choi channel.'}
    (ROOT/args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'result':args.output,'runtime_seconds':result['runtime_seconds']}))


if __name__=='__main__':main()
