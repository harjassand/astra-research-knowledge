"""Paid raw positive pair-quartic aggregation and actual diagonal-mobility price."""
from fractions import Fraction as F
import positive_integrals as p
base=p.base;Unknown=p.Unknown;fs=p.fs

def acquire(raw,*,max_dimension=1024,max_terms=100000,max_coefficient_bits=4096,max_exponent_entries=64000000,max_total_coefficient_bits=32000000,max_rational_bits=1000000):
 budgets=locals().copy();budgets.pop('raw')
 for k,v in budgets.items():base.strict_int(v,k)
 if type(raw)is not dict or set(raw)!={'dimension','energy_terms','mobility_program'}:raise Unknown('complete actual pair-quartic/diagonal-mobility raw schema')
 m=base.strict_int(raw['dimension'],'dimension')
 if m>max_dimension or m>max_exponent_entries or m%4 or m<16:raise Unknown('dimension/integer-alpha/exponent budget before allocations')
 ts=raw['energy_terms']
 if type(ts)is not list or not 1<=len(ts)<=max_terms or len(ts)*m>max_exponent_entries:raise Unknown('literal term/exponent-entry budget')
 prog=raw['mobility_program']
 if type(prog)is not dict:raise Unknown('actual constant mobility schema')
 if set(prog)=={'kind','value'} and prog['kind']=='constant_isotropic':
  a=base.raw_frac(prog['value'],max_coefficient_bits);mu=[a]*m;mobility_bits=a.numerator.bit_length()+a.denominator.bit_length();mobility_entries=1
 elif set(prog)=={'kind','entries'} and prog['kind']=='constant_diagonal':
  if type(prog['entries'])is not list or len(prog['entries'])!=m:raise Unknown('actual diagonal mobility dimension')
  mu=[base.raw_frac(x,max_coefficient_bits)for x in prog['entries']];mobility_bits=sum(x.numerator.bit_length()+x.denominator.bit_length()for x in mu);mobility_entries=m
 else:raise Unknown('actual constant isotropic/diagonal mobility required')
 if any(x<=0 for x in mu):raise Unknown('actual strictly positive mobility entries')
 rb=base.RationalBudget(max_rational_bits);aggregated={};read_bits=mobility_bits;raw_zero_terms=0;duplicate_terms=0
 for item in ts:
  if type(item)is not dict or set(item)!={'powers','coefficient'}:raise Unknown('complete literal energy term')
  powers=item['powers']
  if type(powers)is not list or len(powers)!=m:raise Unknown('literal exponent vector dimension')
  if any(type(x)is not int or x not in (0,2,4)for x in powers)or sum(powers)!=4:raise Unknown('actual homogeneous pure/pair quartic grammar')
  coef=base.raw_frac(item['coefficient'],max_coefficient_bits)
  if coef<0:raise Unknown('negative energy atom not admitted')
  read_bits+=coef.numerator.bit_length()+coef.denominator.bit_length()
  if read_bits>max_total_coefficient_bits:raise Unknown('total literal energy/mobility coefficient bits')
  key=tuple(powers)
  if key in aggregated:duplicate_terms+=1;aggregated[key]=rb.add(aggregated[key],coef)
  else:aggregated[key]=rb.keep(coef)
  if coef==0:raw_zero_terms+=1
 pure=[F(0)]*m;pairs=[];canonical_terms=[]
 for powers,coef in aggregated.items():
  if not coef:continue
  if max(coef.numerator.bit_length(),coef.denominator.bit_length())>max_coefficient_bits:raise Unknown('normalized aggregate coefficient bit budget')
  support=[(i,x)for i,x in enumerate(powers)if x]
  if len(support)==1 and support[0][1]==4:pure[support[0][0]]=coef
  elif len(support)==2 and all(x==2 for _,x in support):pairs.append((support[0][0],support[1][0],coef))
  else:raise Unknown('pure/pair support acquisition')
  canonical_terms.append({'powers':list(powers),'coefficient':fs(coef)})
 if any(x<=0 for x in pure):raise Unknown('all actual aggregated pure quartics must be positive')
 c=[rb.mul(F(12),rb.mul(mu[i],pure[i]))for i in range(m)]
 for i,j,g in pairs:
  c[j]=rb.add(c[j],rb.mul(F(2),rb.mul(mu[i],g)));c[i]=rb.add(c[i],rb.mul(F(2),rb.mul(mu[j],g)))
 H=F(0)
 for x in c:H=rb.add(H,rb.mul(x,x))
 canonical={'dimension':m,'energy_terms':canonical_terms,'mobility_program':prog}
 info={'actual_raw_sha256':base.canonical_hash(raw),'normalized_raw_sha256':base.canonical_hash(canonical),'m':m,'alpha':m//4,'literal_terms_read':len(ts),'literal_exponent_entries_read':len(ts)*m,'literal_coefficient_bits_read_including_mobility':read_bits,'mobility_entries_read':mobility_entries,'duplicate_terms_aggregated':duplicate_terms,'zero_terms_read':raw_zero_terms,'normalized_positive_terms':len(canonical_terms),'pure_coefficient_min':fs(min(pure)),'actual_mobility_floor':fs(min(mu)),'actual_Hessian_trace_coefficients':[fs(x)for x in c],'Hessian_trace_coefficient_norm_squared':fs(H),'aggregation_and_derivative_rational_operations':rb.operations,'max_stored_rational_bits':rb.max_stored_bits,'model_equivalence':'literal nonnegative terms summed exactly; no negative/SOS/rotated-oracle extension'}
 return canonical,info,H,min(pure),m//4
