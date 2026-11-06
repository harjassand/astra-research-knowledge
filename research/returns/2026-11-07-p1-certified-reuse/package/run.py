"""Acquire once, then evaluate later nonlinear and dynamic attachments.

python3 run.py                builds the retained exact certificates
python3 run.py --check-only   replays the saved acquisition and flow paths

No third-party packages are required. Numerical proposals use ordinary
floats; all reported error certificates use exact rational residuals.
"""
import argparse,copy,hashlib,json,time
from fractions import Fraction as Q
from pathlib import Path
from memory import (require,round_dyadic,acquire,replay_acquisition,compact,
                    sqrt_upper)
from verified_flow import (build_emulator,build_full,propose_path,
                           certify_reduced,certify_full)

HERE=Path(__file__).resolve().parent


def dump(name,obj):
    (HERE/name).write_text(json.dumps(obj,separators=(',',':'))+'\n')


def source_matrix(n=192,tail_change=Q(0)):
    H=[[Q(0)]*n for _ in range(n)]
    for i in range(n):
        H[i][i]=Q(1)+Q(i%3-1,64)
        if i+1<n:H[i][i+1]=H[i+1][i]=Q(-1,8)
    H[40][40]+=tail_change
    return H


def validate_source(H,a,b):
    """Exact diagonal-dominance certificates imply the spectral bounds."""
    n=len(H)
    require(all(len(row)==n for row in H))
    require(all(H[i][j]==H[j][i] for i in range(n) for j in range(n)))
    lower=min(H[i][i]-sum((abs(H[i][j]) for j in range(n) if j!=i),Q(0)) for i in range(n))
    upper=max(H[i][i]+sum((abs(H[i][j]) for j in range(n) if j!=i),Q(0)) for i in range(n))
    require(Q(a)<=lower<=upper<=Q(b))
    return {'spectral_lower':str(lower),'spectral_upper':str(upper),
            'nonzero_coefficients':sum(bool(v) for row in H for v in row)}


class QuantizedSource:
    def __init__(self,H):
        self.rows=[[(j,v) for j,v in enumerate(row) if v] for row in H]
        self.n=len(H);self.calls=0;self.products=0;self.quantizations=0;self.max_bits=0
    def __call__(self,x,p):
        require(len(x)==self.n and sum((v*v for v in x),Q(0))<=1)
        result=[]
        for row in self.rows:
            value=Q(0)
            for j,h in row:
                product=h*x[j];value+=product;self.products+=1
                self.max_bits=max(self.max_bits,abs(product.numerator).bit_length(),
                                  product.denominator.bit_length(),abs(value.numerator).bit_length(),
                                  value.denominator.bit_length())
            y=round_dyadic(value,p)
            require(abs(y-value)<=Q(1,1<<(p+1)))
            result.append(y);self.quantizations+=1
        self.calls+=1
        return result
    def counts(self):
        return {'calls':self.calls,'scalar_products':self.products,
                'scalar_additions':self.products,'coordinate_quantizations':self.quantizations,
                'max_dot_product_bits':self.max_bits}


def scenarios():
    # These declarations are instantiated only after the acquisition record
    # is fixed. The acquisition function accepts no later load or task.
    return [
      {'name':'uncoupled_load','attachment':{'dimension':0},'load':[],
       'segments':[{'duration':'1','input':['1','0','-1/2']},
                   {'duration':'1','input':['0','0','0']}]},
      {'name':'coupled_quartic_load','attachment':{'dimension':0},
       'load':[{'degree':1,'weight':'1/2','direction':['1','0','0']},
               {'degree':3,'weight':'1/3','direction':['1','-1','1']}],
       'segments':[{'duration':'1/2','input':['1','1/2','0']},
                   {'duration':'1/2','input':['0','-1/2','1']},
                   {'duration':'1','input':['0','0','0']}]},
      {'name':'new_dynamic_attachment','attachment':{
          'dimension':2,'damping':['1','3/2'],
          'skew':[['0','0','0','1','0'],['0','0','0','0','1/2'],
                  ['0','0','0','-1/2','0'],['-1','0','1/2','0','1/4'],
                  ['0','-1/2','0','-1/4','0']]},
       'load':[{'degree':3,'weight':'1/2','direction':['1','0','-1','1','0']},
               {'degree':1,'weight':'1/4','direction':['0','1','0','0','1']}],
       'segments':[{'duration':'1','input':['1','1/2','-1/4','0','0']},
                   {'duration':'1','input':['0','0','0','0','0']}]}
    ]


def inverse_first_diagonal(H):
    # Exact continued elimination for this tridiagonal fixture; no inverse oracle.
    d=H[-1][-1]
    for i in range(len(H)-2,-1,-1):d=H[i][i]-H[i][i+1]**2/d
    return 1/d


def ambiguity(record):
    require(all(Q(row['query'][40])==0 for row in record['history']))
    minus=source_matrix(tail_change=Q(-1,32));plus=source_matrix(tail_change=Q(1,32))
    low=validate_source(minus,'2/3','4/3');high=validate_source(plus,'2/3','4/3')
    gm,gp=inverse_first_diagonal(minus),inverse_first_diagonal(plus)
    require(gm>gp)
    return {'changed_coordinate':40,'diagonal_perturbations':['-1/32','1/32'],
            'all_acquisition_inputs_zero_in_changed_coordinate':True,
            'identical_exact_actions_and_quantized_reports':True,
            'minus_spectral_certificate':low,'plus_spectral_certificate':high,
            'first_port_DC_responses':[str(gm),str(gp)],
            'strict_DC_difference':str(gm-gp),
            'all_modes_visible_from_first_port':'Nonzero tridiagonal off-diagonals make e_0 cyclic.'}


def static_failure():
    H1=[[Q(5,4),Q(1,2)],[Q(1,2),Q(1)]]
    H2=[[Q(5,4),Q(1)],[Q(1),Q(4)]]
    for H in [H1,H2]:
        for a,b,c in [(H[0][0]-Q(1,2),H[0][1],H[1][1]-Q(1,2)),
                      (Q(5)-H[0][0],-H[0][1],Q(5)-H[1][1])]:
            require(a>0 and c>0 and a*c-b*b>0)
    S=[H[0][0]-H[0][1]**2/H[1][1] for H in [H1,H2]]
    third=[H[0][0]**2+H[0][1]**2 for H in [H1,H2]]
    require(S==[Q(1),Q(1)] and third[0]!=third[1])
    return {'matrices':[[[str(x) for x in row] for row in H] for H in [H1,H2]],
            'DC_port_impedances':[str(x) for x in S],
            'unit_step_third_derivatives':[str(x) for x in third],
            'shared_spectral_interval':['1/2','5']}


def verify_task_path(path,case):
    """Bind a trajectory certificate to the requested later scientific task."""
    require(path['load']==case['load'],'Path uses a different nonlinear load')
    require(len(path['pieces'])==len(case['segments']),'Changed input segmentation')
    for part,segment in zip(path['pieces'],case['segments']):
        require(list(map(Q,part['input']))==list(map(Q,segment['input'])),
                'Path uses a different input')
        require(Q(part['step'])*(len(part['nodes'])-1)==Q(segment['duration']),
                'Path uses a different time interval')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only',action='store_true');args=parser.parse_args()
    start=time.monotonic();H=source_matrix();validation=validate_source(H,'2/3','4/3')
    if args.check_only:
        record=json.loads((HERE/'ACQUISITION.json').read_text())
        acquisition_counts=json.loads((HERE/'RESULTS.json').read_text())['acquisition_instrument_work']
    else:
        source=QuantizedSource(H)
        record=acquire(source,192,[0,4,8],'2/3','4/3','1/10000')
        acquisition_counts=source.counts();dump('ACQUISITION.json',record)
    replay=replay_acquisition(record)
    validation=validate_source(H,record['contract']['a'],record['contract']['b'])
    source_check=QuantizedSource(H)
    for row in record['history']:
        expected=source_check(list(map(Q,row['query'])),record['contract']['precision_bits'])
        require([str(x) for x in expected]==row['report'])
    model=compact(record);frozen=json.dumps(model,sort_keys=True,separators=(',',':')).encode()
    digest=hashlib.sha256(frozen).hexdigest()
    if args.check_only:
        require(json.loads((HERE/'PORT_MODEL.json').read_text())==model,
                'Online model does not match acquisition record')
        require(json.loads((HERE/'RESULTS.json').read_text())['model_sha256']==digest,
                'Changed retained model digest')
    else:dump('PORT_MODEL.json',model)
    results=[]
    for case in scenarios():
        name=case['name'];L,R,alpha=build_emulator(model,case['attachment'])
        LF,RF,alphaF=build_full(H,model,case['attachment']);require(R==RF and alpha==alphaF)
        if args.check_only:
            saved=json.loads((HERE/(name+'.json')).read_text())
            path,full=saved['emulator_path'],saved['source_reference_path']
        else:
            path=propose_path(L,case['load'],R,case['segments'])
            full=propose_path(LF,case['load'],R,case['segments'])
        verify_task_path(path,case);verify_task_path(full,case)
        certificate=certify_reduced(model,path,case['attachment'])
        reference=certify_full(LF,full,R,alpha)
        # Check the independently integrated full-source reference, retaining
        # its own numerical error. It is never an input to acquisition or prediction.
        dc=[Q(x)-Q(y) for x,y in zip(certificate['terminal_observed'],reference['terminal_observed'])]
        observed_difference=sqrt_upper(sum((x*x for x in dc),Q(0)))
        require(observed_difference<=Q(certificate['uniform_observed_error_radius'])+
                                     Q(reference['uniform_state_error_radius']))
        summary={'name':name,'observed_coordinates':R,'emulator_dimension':len(L),
                 'full_source_dimension':len(LF),'emulator_certificate':certificate,
                 'source_reference_certificate':reference,
                 'terminal_reference_difference_bound':str(observed_difference),
                 'additional_native_acquisition_calls':0,
                 'proposal_field_evaluations':path['proposal_field_evaluations'],
                 'source_reference_field_evaluations':full['proposal_field_evaluations']}
        results.append(summary)
        if not args.check_only:dump(name+'.json',{'case':case,'emulator_path':path,
                                                 'source_reference_path':full,'summary':summary})
        print(json.dumps({'completed':name,'error_radius':float(Q(certificate['uniform_observed_error_radius'])),
                          'reference_difference':float(observed_difference),'emulator_states':len(L)}),flush=True)
    require(hashlib.sha256(json.dumps(model,sort_keys=True,separators=(',',':')).encode()).hexdigest()==digest)
    witness=ambiguity(record);failure=static_failure()
    bad=copy.deepcopy(record);bad['moments'][0][0][0]='100'
    rejected=False
    try:replay_acquisition(bad)
    except ValueError:rejected=True
    require(rejected)
    report={'date':'2026-11-07','status':'PASS','model_sha256':digest,
            'source_spectral_certificate':validation,'contract':record['contract'],
            'acquisition_instrument_work':acquisition_counts,
            'source_aware_verification_work':source_check.counts(),
            'replay':replay,'later_tasks':results,'same_model_for_every_task':True,
            'source_not_identified':witness,'static_summary_failure':failure,
            'corrupted_memory_coefficient_rejected':rejected,
            'elapsed_seconds':time.monotonic()-start,
            'independent_or_formal_verification':False,
            'physical_experiments_performed':False}
    if not args.check_only:dump('RESULTS.json',report)
    print(json.dumps({'status':'PASS','acquisition':replay,'elapsed_seconds':report['elapsed_seconds'],
                      'source_ambiguity_proved':True,'corrupted_coefficient_rejected':True},indent=2))


if __name__=='__main__':main()
