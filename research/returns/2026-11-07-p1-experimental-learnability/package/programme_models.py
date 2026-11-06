"""Bounded simulation and certified coefficients for the learnability reduction.

This evaluator never decides non-halting. It simulates at most p steps and
returns a certified interval of width at most 2^(-p). The underlying model
coefficient is 1/2 + 2^(-(t+2)) if the supplied binary-tape machine halts
at step t, and 1/2 otherwise. Every coefficient is rational, but the input
is its evaluation programme rather than its explicit rational value.

Only finite, known fixtures are executed in run.py. The undecidability
claim is the mathematical reduction in RESULT.txt, not a finite test.
"""
from fractions import Fraction as Q


def require(condition,message='Invalid machine or argument'):
    if not condition:
        raise ValueError(message)


def validate(machine):
    states=machine['states'];start=machine['start'];table=machine['transitions']
    require(isinstance(states,int) and states>=0)
    require(start=='HALT' or (isinstance(start,int) and 0<=start<states))
    require(len(table)==states)
    for row in table:
        require(len(row)==2)
        for write,move,next_state in row:
            require(write in (0,1) and move in (-1,1))
            require(next_state=='HALT' or
                    (isinstance(next_state,int) and 0<=next_state<states))
    require(all(symbol in (0,1) for symbol in machine.get('tape',[])))


def bounded_halt_time(machine,budget):
    """Return an observed halt time <=budget, or None (not a non-halting claim)."""
    validate(machine)
    require(isinstance(budget,int) and budget>=0)
    state=machine['start'];head=0
    tape={i:s for i,s in enumerate(machine.get('tape',[])) if s}
    for time in range(budget+1):
        if state=='HALT':
            return time
        if time==budget:
            return None
        write,move,state=machine['transitions'][state][tape.get(head,0)]
        if write:
            tape[head]=write
        else:
            tape.pop(head,None)
        head+=move


def coefficient_interval(machine,p):
    require(isinstance(p,int) and p>=0)
    t=bounded_halt_time(machine,p)
    if t is not None:
        a=Q(1,2)+Q(1,1<<(t+2))
        return a,a
    # Any first halt not yet observed has t>=p+1.
    return Q(1,2),Q(1,2)+Q(1,1<<(p+3))


def evaluate(machine,which,x,p,quantity='gradient'):
    """Certified interval for value/gradient/equilibrium at rational input.

    which=0 is V=x^2/2. which=1 adds a*x. Precision overhead for
    potential values is explicitly charged through extra simulation steps.
    """
    require(which in (0,1) and isinstance(p,int) and p>=0)
    x=Q(x)
    require(quantity in ('potential','gradient','equilibrium'))
    extra=max(0,abs(x.numerator).bit_length()) if quantity=='potential' else 0
    a,b=(Q(0),Q(0)) if which==0 else coefficient_interval(machine,p+extra)
    if quantity=='gradient':
        return x+a,x+b
    if quantity=='equilibrium':
        return -b,-a
    ends=[x*x/2+a*x,x*x/2+b*x]
    return min(ends),max(ends)


def loop_machine():
    # State remains 0 after each transition: this specific machine never halts.
    return {'states':1,'start':0,'tape':[],
            'transitions':[[[0,1,0],[1,1,0]]]}


def delayed_halt_machine(t):
    require(isinstance(t,int) and t>=0)
    if t==0:
        return {'states':0,'start':'HALT','tape':[],'transitions':[]}
    table=[]
    for state in range(t):
        following='HALT' if state==t-1 else state+1
        table.append([[0,1,following],[1,1,following]])
    return {'states':t,'start':0,'tape':[],'transitions':table}


def common_report(x,p,beta):
    """One common report for offsets 0 and 1/2+beta, if this choice works.

    Native error is 1/4; the additional rounding allowance is q/2.
    Choose the first q-grid point strictly above the zero-beta left edge.
    This realizes the finite-bit lower-bound construction in RESULT.txt.
    A failure here is not a proof that no other common report exists.
    """
    x=Q(x);beta=Q(beta);q=Q(1,1<<p)
    require(p>=0 and beta>=0)
    left=x+Q(1,4)-q/2
    j=(left/q).numerator//(left/q).denominator+1
    y=j*q;eta=Q(1,4)+q/2
    if abs(y-x)<=eta and abs(y-(x+Q(1,2)+beta))<=eta:
        return y
    return None
