"""Read-only audit of the saved finite game, model and complete transcript."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
import numpy as np
from game import ProtocolGame,REQUESTS,COMMANDS,DEADLINE,observe,SCALE,ANALOG_THRESHOLD
from exact import encode, require

P=Path(__file__).resolve().parent/'results'
def read(n):return json.loads((P/n).read_text())

def main():
    model=read('MODEL.json');saved=read('POLICY.json');result=read('EXECUTION.json')
    g=ProtocolGame(model['G']);eps=Q(model['epsilon']);r=Q(model['reader_radius'])
    sol=g.solve(r+eps,True);v=g.verify(sol)
    require(saved['words']==[list(w) for w in g.words])
    require(np.array_equal(np.array(saved['policy']),sol['policy']))
    require(np.array_equal(np.array(saved['winning'],dtype=bool),sol['W']))
    require(np.array_equal(np.array(saved['rank']),sol['rank']))
    lose=g.solve(Q(model['failing_reader_radius'])-eps,True);lv=g.verify(lose)
    critical=g.critical();stored=read('CRITICAL_NOISE.json')
    require(critical['critical_radius']==Q(stored['critical_radius']))
    require(critical['at_boundary_winning']==stored['at_boundary_winning'])
    trace=read('TRANSCRIPT.json');s=g.initial;t=0;k=DEADLINE-1;age=0;served=0;maxage=0
    support_checks=0;continuous_work=Q(0);nonzero=0;switches=0;previous=0
    qerr=Q(1,2*SCALE)
    for i,row in enumerate(trace):
        require(row['step']==i and row['suffix']==s and row['request']==t and row['remaining']==k+1)
        a=row['action'];require(a==int(sol['policy'][s,t,k]))
        if a:nonzero+=1
        if a!=previous:switches+=1
        previous=a
        sp=int(g.next[s,a]);require(row['next_suffix']==sp)
        o=observe(row['read_integers']);require(list(o)==row['observation'])
        for j in range(3):
            require(o[j] in sol['allowed'][sp][j])
            require(abs(Q(row['read_integers'][j],SCALE)-g.pred_Q[sp][j])<=r+eps+qerr)
            support_checks+=1
        require(sum(x!=0 for x in o)<=1)
        axis,sign=REQUESTS[t];hit=o[axis]==sign;require(hit==row['served'])
        age+=1;s=sp
        if hit:
            maxage=max(maxage,age);age=0;served+=1
            t=(5*served+served//7+served//13)%6;k=DEADLINE-1
        else:
            require(k>0);k-=1
        require(sol['W'][s,t,k])
    require(served==result['completed_requests'] and maxage==result['maximum_request_delay_ticks'])
    require(Q(result['certified_true_target_signed_output_at_every_acknowledgement'])==ANALOG_THRESHOLD-r)
    require(hashlib.sha256((P/'TRANSCRIPT.json').read_bytes()).hexdigest()==result['transcript_sha256'])
    # Explicit source-certificate induction at the shipped precision.
    u=Q(1,1<<80);L=Q(model['lead'])
    Ev=12*u/L;Ex=16*u/L
    require((1-L/2)*Ev+Q(11,2)*u<=Ev)
    require(Q(3,16)*Ev+Q(77,8)*u/L<=Ex)
    require(Ex<1 and Ev<1)
    port_error=16*Ex+qerr
    require(port_error+Q(1,1<<35)<Q(1,1<<30))
    audit={'status':'PASS','policy':v,'counterstrategy':lv,
           'critical_radius':critical['critical_radius'],'adc_threshold':ANALOG_THRESHOLD,
           'native_uniform_error_induction':'PASS','model_support_scalar_checks':support_checks,
           'transcript_steps':len(trace),'completed_requests':served,'maximum_delay_ticks':maxage,
           'nonzero_command_intervals':nonzero,'deployment_command_changes':switches,
           'deployment_command_squared_effort':nonzero*Q(model['h']),
           'post_loop_command_is_nonzero':bool(previous),'transcript_sha256':result['transcript_sha256']}
    (P/'VERIFICATION.json').write_text(json.dumps(encode(audit),indent=2,sort_keys=True)+'\n')
    print(json.dumps(encode({k:v for k,v in audit.items() if k not in ('policy','counterstrategy')}),indent=2))

if __name__=='__main__':main()
