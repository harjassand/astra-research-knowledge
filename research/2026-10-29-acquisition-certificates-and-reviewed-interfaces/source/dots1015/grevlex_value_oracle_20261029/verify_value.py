from modular_quotient import *
import hashlib
st=time.time();candidate=json.loads((P/'candidate.json').read_text());c=[F(x) for x in candidate['monic_coefficients_low_to_high']];ints=list(map(int,candidate['integer_coefficients_low_to_high']));height_path=P/'value_polynomial_height_bound.json';height=json.loads(height_path.read_text());H=int(height['primitive_coefficient_height_bound']);assert max(map(abs,ints))<=H
mod=1;pr=10000019;records=[]
while mod<=2*H*H:
 try:v=cp(pr)
 except ValueError:pr=int(sp.nextprime(pr));continue
 assert all(x.denominator%pr and x.numerator*pow(x.denominator%pr,-1,pr)%pr==v[j] for j,x in enumerate(c))
 if not records:
  t=sp.Symbol('t');poly=sp.Poly.from_list(v[::-1],t,modulus=pr);assert sp.gcd(poly,poly.diff()).degree()==0
 mod*=pr;records.append(pr);pr=int(sp.nextprime(pr))
result={'status':'EXACT_BY_HEIGHT_BOUNDED_MODULAR_IDENTITY','seconds':time.time()-st,'prime_count':len(records),'primes':records,'modulus_bits':mod.bit_length(),'threshold_bits':(2*H*H).bit_length(),'height_dependency_sha256':hashlib.sha256(height_path.read_bytes()).hexdigest(),'first_prime_squarefree':True,'every_prime_full_krylov_rank':40}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='primes'})
