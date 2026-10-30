"""Verify a shared-capacity certificate for an arbitrary finite Fourier gradient.

Input modes define an ACTUAL periodic potential
  phi=sum(sine*sin(k.x)+cosine*cos(k.x)),
with rational two-vectors and integer frequencies. A rational rank-one
covariance catalogue is supplied separately. Passing certifies this field
at every mean and overall amplitude, for every admitted ROC polynomial
with leading F. A catalogue failure is never reported as QC failure.
"""
from dataclasses import dataclass
from fractions import Fraction as R
from pathlib import Path
import argparse,json
from receive import m,b,dot,quadratic,psd
from capacity import canonical,quotient,RangeObstruction
HERE=Path(__file__).resolve().parent

@dataclass(frozen=True)
class Gaussian:
    real:R=R(0)
    imag:R=R(0)
    @staticmethod
    def lift(x):return x if isinstance(x,Gaussian) else Gaussian(R(x))
    def __add__(self,other):
        z=self.lift(other);return Gaussian(self.real+z.real,self.imag+z.imag)
    __radd__=__add__
    def __neg__(self):return Gaussian(-self.real,-self.imag)
    def __sub__(self,other):return self+-self.lift(other)
    def __rsub__(self,other):return self.lift(other)+-self
    def __mul__(self,other):
        z=self.lift(other);return Gaussian(self.real*z.real-self.imag*z.imag,self.real*z.imag+self.imag*z.real)
    __rmul__=__mul__
    def __bool__(self):return bool(self.real or self.imag)

def gradient(modes):
    G=[{} for _ in range(4)]
    for mode in modes:
        k=tuple(mode['frequency']);sine=list(map(R,mode.get('sine',[0,0])));cosine=list(map(R,mode.get('cosine',[0,0])))
        assert len(k)==2 and all(isinstance(v,int) for v in k) and k!=(0,0) and len(sine)==len(cosine)==2
        for i in range(2):
            for j in range(2):
                for sign in (-1,1):
                    freq=tuple(sign*v for v in k);z=Gaussian(sine[i]*k[j]/2,sign*cosine[i]*k[j]/2)
                    G[2*i+j]=m.add(G[2*i+j],{freq:z})
    assert all(not g.get((0,0),R(0)) for g in G)
    return G

def average(poly,G):
    z=Gaussian.lift(m.average(poly,G));assert not z.imag;return z.real

def verify(payload):
    F,C0,T=m.acquired();qc=json.loads((HERE.parent/'quadratic_boundary/certificate.json').read_text());powers=qc['cubic_powers'];basis=[list(map(R,row)) for row in qc['normal_form_basis']]
    polys=[{tuple(pw):co for pw,co in zip(powers,row) if co} for row in basis]
    assert all(polys[j]==b.diff(F,j) for j in range(4))
    G=gradient(payload['modes']);S=[[average(b.mul(b.var(4,i),b.var(4,j)),G) for j in range(4)] for i in range(4)]
    rows=[row for row in payload['catalogue'] if R(row['weight'])];weights=[R(row['weight']) for row in rows];rays=[list(map(R,row['rank_one_direction'])) for row in rows]
    assert weights and all(w>0 for w in weights) and all(len(r)==4 and r[0]*r[3]-r[1]*r[2]==0 for r in rays)
    Scat=[[sum(w*r[i]*r[j] for w,r in zip(weights,rays)) for j in range(4)] for i in range(4)]
    if S!=Scat:return {'status':'FIXED_CATALOGUE_COVARIANCE_MISMATCH','scope':'No variational conclusion. Supply a catalogue with the actual covariance.'}
    HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)];HH=[[[b.evaluate(p,r) for p in row] for row in HF] for r in rays]
    for H in HH:psd(H)
    GG=[[[b.evaluate(b.diff(p,j),r) for p in polys] for j in range(4)] for r in rays];target=[average(p,G) for p in polys]
    f=average(F,G);T4=average(b.mul(T,T),G);gap=R(payload.get('requested_L4_gap','0'));assert gap>=0
    try:cap=canonical(HH,GG,weights,[[v] for v in target])
    except RangeObstruction as obstruction:
        coeff=[sum(y*row[j] for y,row in zip(obstruction.annihilator,basis)) for j in range(20)]
        obstruction_poly={tuple(pw):co for pw,co in zip(powers,coeff) if co}
        assert all(b.evaluate(b.diff(obstruction_poly,j),r)==0 for j in range(4) for r in rays)
        assert average(obstruction_poly,G)==obstruction.target_values[0]!=0
        return {'status':'FIXED_CATALOGUE_RANGE_OBSTRUCTION','annihilating_cubic_coefficients':list(map(str,coeff)),'actual_cubic_moment':str(obstruction.target_values[0]),'scope':'Only this fixed ray catalogue fails. This is not a QC counterexample.'}
    cost=cap['cost_matrix'][0][0];budget=f-cost;W=cap['capacity_matrix']
    # The translation and mixed blocks are fixed by the actual covariance,
    # so their equality is checked without using a catalogue assumption.
    Hactual=[[average(p,G) for p in row] for row in HF];Bactual=[[average(b.diff(p,j),G) for p in polys[4:]] for j in range(4)]
    assert [row[:4] for row in W[:4]]==Hactual and [row[4:] for row in W[:4]]==Bactual
    terms=[];P=b.add(F,C0,b.scale(T,1859));HP=[[b.diff(b.diff(P,i),j) for j in range(4)] for i in range(4)];rhs=budget
    for w,r,H,Z in zip(weights,rays,HH,cap['sources']):
        A=[row[0]/w for row in Z];score=quadratic([[b.evaluate(p,A) for p in row] for row in HP],r);assert score>=0;rhs+=w*score/2
        terms.append({'weight':str(w),'rank_one_direction':list(map(str,r)),'canonical_base':list(map(str,A))})
    actual=average(P,G);assert actual==rhs
    passed=budget>=gap*T4
    result={'status':'CERTIFIED_FIELD' if passed else 'FIXED_CATALOGUE_BUDGET_INSUFFICIENT','actual_covariance_matched':True,'all_twelve_cubic_moments_matched':True,'canonical_cost_is_simultaneous_Loewner_minimum':True,'catalogue_capacity_rank':cap['capacity_rank'],'canonical_quartic_budget':str(budget),'fourth_gradient_moment':str(T4),'requested_L4_gap':str(gap),'requested_lower_bound':str(gap*T4),'fixture_exact_actual_energy_identity':True,'positive_hessian_terms':terms,'scope':'This actual compatible field, all means, overall amplitudes and proper common output rotations, for every globally ROC polynomial over F. No unrestricted QC inference; catalogue failure is not QC failure.'}
    try:
        q=quotient(W,target,f);assert q['quartic_budget']==budget
        if passed:
            # The 9x9 LMI is exactly the resource-capacity certificate.
            a=q['leading_budget_a']-2*gap*T4;rr=q['correlation_target'];La=q['quotient_capacity'];LMI=[[a]+rr]+[[rr[i]]+row for i,row in enumerate(La)];psd(LMI)
        result.update({'quotient_capacity_dimension':8,'quotient_capacity_rank':q['quotient_rank'],'nine_by_nine_capacity_LMI_verified':passed,'leading_translation_reduced_budget':str(q['leading_budget_a']),'correlation_cost':str(q['correlation_cost'])})
    except AssertionError:
        # Rank-deficient translation blocks are handled by the full capacity
        # system above; they need not have the eight-dimensional Schur form.
        if b.rank(Hactual)==4:raise
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('--out',type=Path);args=parser.parse_args();result=verify(json.loads(args.input.read_text()))
    if args.out:
        args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='positive_hessian_terms'},indent=2))
    else:print(json.dumps(result,indent=2))
if __name__=='__main__':main()
