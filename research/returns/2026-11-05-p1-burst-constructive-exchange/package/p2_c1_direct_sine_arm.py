"""C1 canonical meter, finite C1 source force, exact original sine arms.

Each pointer coupling uses cubic smoothstep edges with peak1 and slew<=96.
This removes step edges and derivative discontinuities in the meter coupling.
"""
import argparse
import json
from decimal import Decimal
from pathlib import Path
from p2_slew_direct_sine_arm import point,interval_piece

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--interval',action='store_true')
    parser.add_argument('--pieces',type=int,default=100)
    args=parser.parse_args()
    if args.interval:
        rows=[]
        for j in range(args.pieces):
            lo=str(Decimal(j)/(4*Decimal(args.pieces)))
            hi=str(Decimal(j+1)/(4*Decimal(args.pieces)))
            r=interval_piece(lo,hi,profile='cubic'); rows.append(r)
            print(json.dumps({'piece':j,'k':[lo,hi],'upper':r['variance_upper'],
                'amplitude':r['amplitude_upper'],'det_upper':r['determinant_upper'],
                'strict':r['strict']}),flush=True)
            assert r['strict']
        out={'arithmetic':'mpmath directed interval, 40 decimal digits',
             'model':'C1 cubic smoothstep canonical meter coupling',
             'domain':'0 <= k <= 1/4','all_strict':True,
             'uniform_variance_upper':max(r['variance_upper'] for r in rows),
             'uniform_amplitude_upper':max(r['amplitude_upper'] for r in rows),
             'determinant_upper':max(r['determinant_upper'] for r in rows),
             'pieces':rows}
        path=Path(__file__).with_name('p2_c1_direct_sine_arm_interval.json')
    else:
        out={'model':'C1 canonical meter and original eta=.5 sine arms',
             'rows':[point(k,profile='cubic') for k in (0.,.01,.1,.25)]}
        for r in out['rows']:
            assert r['dither_sine_amplitude']<1
            assert abs(r['position_feedback_initial_x_gain'])<1e-12
            assert abs(r['final_x_residual_momentum_covariance'])<1e-12
        path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(path)
