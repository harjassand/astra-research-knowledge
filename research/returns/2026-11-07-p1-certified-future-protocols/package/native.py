"""Paid private 256-state software component, with exact integer propagation.

The learner receives only port readings and a declared channel contract.
This is the same rational spectral fixture as the retained component A.
The driver is a first-order actuator. No internal state is reset between trials.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import isqrt
from exact import exp_minus, psd, require, encode, qbits

P=80
S=1<<P
READ_BITS=40
READ_SCALE=1<<READ_BITS
LEAD=Q(1,4096)

def rnd(num,den):
    if num<0:return -rnd(-num,den)
    q,r=divmod(num,den)
    return q+int(2*r>den or (2*r==den and q%2))

def dyadic(q):return rnd(q.numerator*S,q.denominator)

class NativePort:
    def __init__(self):
        self.n=256;self.p=3
        self.rates=[Q(1)+Q((73*i+19)%256,256) for i in range(256)]
        self.signs=[(1,1 if i%2==0 else -1,1 if (i//2)%2==0 else -1) for i in range(256)]
        gram=[[sum(row[j]*row[k] for row in self.signs)/256 for k in range(3)] for j in range(3)]
        require(gram==[[int(i==j) for j in range(3)] for i in range(3)])
        A=[[sum((lam*row[j]*row[k]/256 for lam,row in zip(self.rates,self.signs)),Q(0)) for k in range(3)] for j in range(3)]
        H2=[[sum((lam*lam*row[j]*row[k]/256 for lam,row in zip(self.rates,self.signs)),Q(0)) for k in range(3)] for j in range(3)]
        V2=[[H2[i][j]-sum(A[i][k]*A[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        require(psd([[2*int(i==j)-A[i][j] for j in range(3)] for i in range(3)]))
        require(psd([[Q(int(i==j),4)-V2[i][j] for j in range(3)] for i in range(3)]))
        self.x=[S]+[0]*255
        self.v=[S//4,-S//4,S//4]
        self.t=Q(0);self.steps=0;self.reads=0
        self.exp_count=0;self.exp_terms=0;self.exp_squares=0;self.exp_bits=0
        self.max_product_bits=0;self.max_state_bits=0;self.coeff_errors=Q(0)
        self.cache={}
        self.moment_check_terms=3*256*9+27
        self.initial_assignments=259
        self._coeff(Q(2)-LEAD);self._coeff(LEAD);self._coeff(Q(30))

    def _exp(self,t):
        lo,hi,c=exp_minus(t,104)
        self.exp_count+=1;self.exp_terms+=c['taylor_terms'];self.exp_squares+=c['squarings']
        self.exp_bits=max(self.exp_bits,c['series_coefficient_bits_max'])
        return lo,hi

    def _enclose(self,lo,hi):
        z=dyadic((lo+hi)/2)
        rad=max(abs(Q(z,S)-lo),abs(Q(z,S)-hi))
        require(rad<=Q(1,S))
        self.coeff_errors=max(self.coeff_errors,rad)
        return z

    def _coeff(self,T):
        if T in self.cache:return self.cache[T]
        dl,du=self._exp(8*T)
        require(du<=1-LEAD/2)
        d=self._enclose(dl,du)
        out=[]
        for lam in self.rates:
            al,au=self._exp(lam*T)
            require(au<=1-LEAD/2)
            a=self._enclose(al,au)
            b=self._enclose((1-au)/lam,(1-al)/lam)
            gl,gu=(al-du)/(8-lam),(au-dl)/(8-lam)
            require(gl>=0 and gu<Q(1,6))
            g=self._enclose(gl,gu)
            out.append((a,b,g))
        self.cache[T]=(d,out)
        return d,out

    def advance(self,command,T):
        T=Q(T);d,coeff=self._coeff(T)
        cmd=[dyadic(Q(c)) for c in command]
        require(sum(Q(c,S)**2 for c in cmd)<=1)
        # This actual bounded error can vary adversarially each command interval.
        drive=[c+(1 if (self.steps+2*j)%5<2 else -1)*(S>>35) for j,c in enumerate(cmd)]
        vv=self.v
        xx=[]
        for row,x,(a,b,g) in zip(self.signs,self.x,coeff):
            bd=sum(s*c for s,c in zip(row,drive))
            bt=sum(s*(v-c) for s,v,c in zip(row,vv,drive))
            terms=(16*a*x,b*bd,g*bt)
            self.max_product_bits=max(self.max_product_bits,*(abs(z).bit_length() for z in terms),abs(sum(terms)).bit_length())
            xx.append(rnd(sum(terms),16*S))
        self.x=xx
        self.v=[rnd(d*v+(S-d)*c,S) for v,c in zip(vv,drive)]
        self.max_state_bits=max(self.max_state_bits,*(abs(z).bit_length() for z in self.x+self.v))
        require(max(abs(z) for z in self.x+self.v)<3*S)
        self.steps+=1;self.t+=T

    def read(self,request=None,noise_radius=Q(0)):
        sums=[sum(row[j]*x for row,x in zip(self.signs,self.x)) for j in range(3)]
        # No true-state values are returned to the learner/controller.
        raw=[rnd(z*READ_SCALE,16*S) for z in sums]
        if request is None:
            biases=[(1 if (self.reads+j)%3 else -1)*Q(1,1<<35) for j in range(3)]
        else:
            axis,sign=request
            available=max(Q(0),Q(noise_radius)-Q(1,1<<30))
            # Worst-direction target error, plus bounded errors at the other ports.
            biases=[(-sign if j==axis else (1 if (self.reads+j)%2 else -1))*available for j in range(3)]
        ans=[z+rnd(v.numerator*READ_SCALE,v.denominator) for z,v in zip(raw,biases)]
        self.reads+=1
        return tuple(ans)

    def costs(self):
        return encode({
            'native_dimension':256,'ports':3,'distinct_visible_poles':256,
            'source_coefficient_scalars':1024,'initial_private_assignments':259,
            'initial_source_norm':Q(1),'initial_actuator_norm_upper':Q(1),
            'actuator_tau':Q(1,8),'native_fractional_bits':P,'output_fractional_bits':READ_BITS,
            'coefficient_enclosure_radius_max':self.coeff_errors,
            'minimum_propagation_duration':LEAD,
            'uniform_actuator_coordinate_error':Q(12,S)/LEAD,
            'uniform_source_coordinate_error':Q(16,S)/LEAD,
            'uniform_port_numerical_error':Q(256,S)/LEAD+Q(1,1<<41),
            'declared_acquisition_read_error':Q(1,1<<30),
            'declared_actuator_error_L2':Q(1,1<<32),
            'time':self.t,'advance_calls':self.steps,'vector_reads':self.reads,
            'scalar_reads':3*self.reads,'state_coordinate_updates':256*self.steps,
            'actuator_coordinate_updates':3*self.steps,
            'source_input_signed_terms':2*3*256*self.steps,
            'source_read_signed_terms':3*256*self.reads,
            'state_integer_multiplications':3*256*self.steps,
            'actuator_integer_multiplications':2*3*self.steps,
            'source_integer_divisions':259*self.steps,
            'read_integer_divisions':6*self.reads,
            'maximum_propagation_integer_bits':self.max_product_bits,
            'maximum_state_integer_bits':self.max_state_bits,
            'exponential_enclosures':self.exp_count,'exponential_taylor_terms':self.exp_terms,
            'exponential_squarings':self.exp_squares,'series_integer_bits_max':self.exp_bits,
            'source_moment_verification_terms':self.moment_check_terms,
            'between_trial_resets':0,'hidden_reads_used_by_learner_or_controller':0,
            'scope':'deterministic software source; exact integer arithmetic with checked rational exponential enclosures; no physical experiment'
        })
