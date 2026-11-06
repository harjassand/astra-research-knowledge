"""Private, paid native source for the executable port-control experiment.

The controller imports no object from this module other than the port interface.
The two source fixtures are exactly the retained 256-state components. All
exponential coefficients have rational enclosures; binary64 propagation has
a checked uniform error budget. No ODE solver or hidden optimization oracle.
"""
from fractions import Fraction as Q
from math import sqrt
import numpy as np
from exact import require, psd, exp_minus, sqrt_up, qbits


def fixture(which):
    n=256; r=3
    multiplier,offset=[(73,19),(117,43)][which]
    values=[Q((multiplier*i+offset)%n,n) for i in range(n)]
    rates=[Q(1)+(v if which==0 else v*v) for v in values]
    B=[[Q(1,16),Q(1 if i%2==0 else -1,16),
        Q(1 if (i//2)%2==0 else -1,16)] for i in range(n)]
    gram=[[sum((row[u]*row[v] for row in B),Q(0)) for v in range(r)] for u in range(r)]
    require(gram==[[Q(int(u==v)) for v in range(r)] for u in range(r)])
    A=[[sum((lam*row[u]*row[v] for lam,row in zip(rates,B)),Q(0))
        for v in range(r)] for u in range(r)]
    second=[[sum((lam*lam*row[u]*row[v] for lam,row in zip(rates,B)),Q(0))
             for v in range(r)] for u in range(r)]
    variance=[[second[u][v]-sum((A[u][j]*A[j][v] for j in range(r)),Q(0))
               for v in range(r)] for u in range(r)]
    require(min(rates)>=1 and max(rates)<=2 and len(set(rates))==n)
    require(psd([[2*int(i==j)-A[i][j] for j in range(r)] for i in range(r)]))
    require(psd([[Q(int(i==j),4)-variance[i][j] for j in range(r)] for i in range(r)]))
    return rates,B


def gamma(n):
    u=Q(1,1<<53)
    return n*u/(1-n*u)


def rounded_interval(lo,hi):
    v=float((lo+hi)/2); q=Q.from_float(v)
    return v,max(abs(q-lo),abs(q-hi))


class PortSource:
    def __init__(self,plan):
        self._n=512; self._r=6; self._plan=plan
        self._p=plan['fixed_point_fraction_bits']; self._scale=1<<self._p
        parts=[fixture(0),fixture(1)]
        self._rates=parts[0][0]+parts[1][0]
        rows=[row+[Q(0)]*3 for row in parts[0][1]]+[[Q(0)]*3+row for row in parts[1][1]]
        self._B=np.array([[float(v) for v in row] for row in rows],dtype=np.float64)
        target=plan['target']; cw=plan['write_command']
        # An opposite-pattern preparation with an unobserved port-orthogonal part.
        # w=e_0-B B^T e_0, in component A. Its addition changes no port readout.
        w=[Q(int(i==0))-sum((rows[i][j]*rows[0][j] for j in range(6)),Q(0)) for i in range(512)]
        x0=[-sum((b*z for b,z in zip(row,target)),Q(0))+v for row,v in zip(rows,w)]
        require(sum((v*v for v in x0),Q(0))<=plan['initial_state_norm_bound']**2)
        require(sum((v*v for v in cw),Q(0))<=plan['initial_actuator_norm_bound']**2)
        require(all(sum((rows[i][j]*w[i] for i in range(512)),Q(0))==0 for j in range(6)))
        self._x=np.array([float(v) for v in x0],dtype=np.float64)
        self._v=np.array([-float(v) for v in cw],dtype=np.float64)
        require(all(Q.from_float(float(z))==q for z,q in zip(self._x,x0)))
        require(all(Q.from_float(float(z))==-q for z,q in zip(self._v,cw)))
        self._tau=plan['actuator_time_constant']; self._dt=plan['sample_interval']
        self._coefficient_count=0;self._terms=0;self._squares=0;self._series_bits=0
        self._short,self._short_error=self._coefficients(self._dt)
        self._long,self._long_error=self._coefficients(plan['write_duration'])
        self._error_certificate=self._validate_native_error()
        self._steps=0;self._reads=0;self._initial_squared_norm=sum((v*v for v in x0),Q(0))
        self._actuation_bias=Q(1,1<<20)
        require(sqrt_up(6*self._actuation_bias**2)<plan['actuator_error_L2'])
        self._read_bias=Q(1,1<<24)
        self._source_bits=max(qbits(x) for x in self._rates+[v for row in rows for v in row])
        self._initial_maxbits=max(qbits(x) for x in x0)

    def _exponential(self,x):
        lo,hi,cost=exp_minus(x,96)
        self._coefficient_count+=1;self._terms+=cost['taylor_terms'];self._squares+=cost['squarings']
        self._series_bits=max(self._series_bits,cost['series_coefficient_bits_max'])
        return lo,hi

    def _coefficients(self,T):
        tl,tu=self._exponential(T/self._tau)
        at,ate=rounded_interval(tl,tu); bt,bte=rounded_interval(1-tu,1-tl)
        AA=[];BB=[];GG=[];max_xerr=Q(0)
        # A priori caps used only for numerical fidelity: true/approximate state
        # and vector commands are all <=8 on the proved physical region.
        Rcap=Vcap=Ccap=Q(8); u=Q(1,1<<53)
        Uc=Q(3,16)*Ccap; Ut=Q(3,16)*(Vcap+Ccap)
        dc=gamma(6)*Uc
        dtail=gamma(6)*Ut*(1+u)+Q(3,16)*u*(Vcap+Ccap)
        for lam in self._rates:
            al,au=self._exponential(lam*T)
            av,ae=rounded_interval(al,au)
            bv,be=rounded_interval((1-au)/lam,(1-al)/lam)
            denom=1/self._tau-lam
            require(denom>0)
            gv,ge=rounded_interval((al-tu)/denom,(au-tl)/denom)
            AA.append(av);BB.append(bv);GG.append(gv)
            aq,bq,gq=map(Q.from_float,(av,bv,gv))
            err=Rcap*ae+Uc*be+Ut*ge+abs(bq)*dc+abs(gq)*dtail
            err+=gamma(5)*(abs(aq)*Rcap+abs(bq)*(Uc+dc)+abs(gq)*(Ut+dtail))
            err+=Q(1,1<<1000) # dominates all gradual-underflow absolute errors
            max_xerr=max(max_xerr,err)
        v_error=Vcap*ate+Ccap*bte+gamma(3)*(abs(Q.from_float(at))*Vcap+abs(Q.from_float(bt))*Ccap)
        v_error+=Q(1,1<<1000)
        decay_upper=self._exponential(T)[1]
        errors={'state_step_L2':sqrt_up(512*max_xerr**2,100),
                'actuator_step_L2':sqrt_up(6*v_error*v_error,100),
                'actuator_decay_upper':tu,
                'state_decay_upper':decay_upper}
        return (np.array(AA),np.array(BB),np.array(GG),at,bt),errors

    def _validate_native_error(self):
        sh,lo=self._short_error,self._long_error
        ve=lo['actuator_step_L2']+sh['actuator_step_L2']/(1-sh['actuator_decay_upper'])
        xe=lo['state_step_L2']+(sh['state_step_L2']+self._dt*ve)/(1-sh['state_decay_upper'])
        read_sum=sqrt_up(Q(6))*gamma(512)*8
        bias=sqrt_up(Q(6))*Q(1,1<<24)
        quant=sqrt_up(Q(6))*Q(1,2*self._scale)
        bias_add=sqrt_up(Q(6))*Q(8,1<<53)
        total=xe+read_sum+bias+quant+bias_add
        require(total<self._plan['measurement_error_L2'])
        require(xe<Q(1,1000) and ve<Q(1,1000))
        # Physical-region bounds plus numerical deviations remain below the caps.
        require(max(self._plan['write_state_radius_upper'],self._plan['retention_state_norm_upper'])+xe<8)
        require(max(self._plan['write_state_radius_upper'],self._plan['retention_state_norm_upper'])+xe+read_sum+bias+quant<8)
        require(max(self._plan['write_force_bound'],self._plan['retention_actuator_norm_upper'])+ve<8)
        require(self._plan['retention_ideal_command_norm_upper']+self._plan['control_evaluation_error_L2']+self._plan['actuator_error_L2']<8)
        return {'status':'PASS','state_error_uniform':xe,'actuator_error_uniform':ve,
                'read_dot_roundoff_L2':read_sum,'deliberate_read_bias_L2':bias,
                'read_quantization_L2':quant,'bias_addition_roundoff_L2':bias_add,
                'complete_read_error_L2':total,'declared_read_error_L2':self._plan['measurement_error_L2'],
                'short_step':sh,'long_step':lo,
                'arithmetic_contract':'IEEE binary64 round-to-nearest, gradual underflow, no overflow; sum/dot error <= gamma_n; all exponential centres checked against rational intervals',
                'scope':'exact linear source and first-order actuator driven by the SAME emitted command record; native errors enter the port-read budget'}

    def _advance(self,cmd,coeff,step):
        c=np.array([v/self._scale for v in cmd],dtype=np.float64)
        # Deterministic bounded disturbances are intentionally not averaged.
        bias=np.array([float(self._actuation_bias)*(1 if (step+3*j)%7<3 else -1) for j in range(6)])
        d=c+bias # exact dyadic addition at these sizes
        A,b,g,at,bt=coeff
        uc=self._B@d; ut=self._B@(self._v-d)
        self._x=A*self._x+b*uc+g*ut
        self._v=at*self._v+bt*d
        self._steps+=1

    def write(self,command):
        self._advance(command,self._long,-1)

    def read(self,k):
        y=self._B.T@self._x
        bias=np.array([float(self._read_bias)*(1 if (k+2*j)%11<5 else -1) for j in range(6)])
        y=y+bias
        self._reads+=1
        return tuple(int(round(float(v)*self._scale)) for v in y)

    def advance(self,command,k):
        self._advance(command,self._short,k)

    def audit(self):
        # Diagnostic readback is not returned to the controller or used to choose commands.
        return {'native_state_norm':float(np.linalg.norm(self._x)),
                'native_actuator_norm':float(np.linalg.norm(self._v)),
                'native_ports':[float(v) for v in self._B.T@self._x]}

    def costs(self):
        return {'source_dimension':512,'ports':6,'source_coefficient_scalars':2048,
            'initial_private_state_assignments':512,'initial_actuator_assignments':6,
            'initial_source_squared_norm':self._initial_squared_norm,'initial_state_bits_max':self._initial_maxbits,
            'source_coefficient_bits_max':self._source_bits,'complete_read_certificate':self._error_certificate,
            'exact_source_moment_weighted_terms':13824,'exact_variance_matrix_inner_products':54,
            'exact_initial_preparation_and_orthogonality_weighted_terms':9216,
            'exponential_enclosures':self._coefficient_count,'exponential_taylor_terms':self._terms,
            'exponential_squarings':self._squares,'elementary_series_bits_max':self._series_bits,
            'native_coefficient_float_scalars':2*(3*512+2),
            'native_state_coordinate_updates':512*self._steps,'native_actuator_coordinate_updates':6*self._steps,
            'native_input_dot_weighted_terms':2*512*6*self._steps,
            'native_port_dot_weighted_terms':512*6*self._reads,
            'post_execution_diagnostic_state_norm_evaluations':2,
            'post_execution_diagnostic_actuator_norm_evaluations':2,
            'post_execution_diagnostic_port_weighted_terms':2*512*6,
            'native_floating_operation_upper_bound':
                4*512*6*self._steps+2*512*6*self._reads+6*512*self._steps+5*6*self._steps+100*self._reads+10000,
            'online_port_vector_reads':self._reads,'scalar_port_readouts':6*self._reads,
            'source_steps':self._steps,'hidden_reads_used_to_choose_commands':0,
            'reset_between_write_and_retention':False}
