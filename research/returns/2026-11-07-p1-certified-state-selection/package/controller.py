"""Standalone fixed-point controller. No native-source imports or state access."""
from fractions import Fraction as Q


class FixedController:
    def __init__(self,plan):
        self.p=plan['fixed_point_fraction_bits'];self.scale=1<<self.p
        self.n=plan['n_ports']
        self.K=[[int(x*self.scale) for x in row] for row in plan['K_fixed']]
        self.beta=[int(x*self.scale) for x in plan['beta_fixed']]
        self.h=[int(x*self.scale) for x in plan['field_fixed']]
        self.write_command=tuple(int(x*self.scale) for x in plan['write_command'])
        self.calls=0;self.max_integer_bits=0

    def retention_command(self,y):
        p=self.p; ans=[]
        for i in range(self.n):
            linear=sum(self.K[i][j]*y[j] for j in range(self.n))
            cubic=self.beta[i]*y[i]*y[i]*y[i]
            numerator=(linear<<(2*p))-cubic+(self.h[i]<<(3*p))
            # nearest, with ties toward +infinity; absolute error <= 2^(-p-1)
            value=(numerator+(1<<(3*p-1)))>>(3*p)
            self.max_integer_bits=max(self.max_integer_bits,abs(linear).bit_length(),
                                      abs(cubic).bit_length(),abs(numerator).bit_length())
            ans.append(value)
        self.calls+=1
        return tuple(ans)

    def ledger(self):
        return {'calls':self.calls,'integer_multiplications':self.calls*(self.n*self.n+3*self.n),
                'fixed_fraction_bits':self.p,'observed_integer_bits_max':self.max_integer_bits,
                'mechanism':'integer products, sums, shifts; final nearest rounding; no solver call'}
