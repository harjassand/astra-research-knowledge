"""Construct finite rational identity-background witnesses from exact family cuts."""
from compile_witness import *
norm2={tuple(2 if j==i else 0 for j in range(4)):Q(1) for i in range(4)}
qpoly={(1,0,0,1):Q(1),(0,1,1,0):Q(-1)}
xpoly={(2,0,0,0):Q(1),(0,0,2,0):Q(1),(0,2,0,0):Q(-1),(0,0,0,2):Q(-1)}
A=tuple(map(Q,(1,0,0,1)));RM=tuple(map(Q,(1,0,0,-2)))
def polar_c2(poly,r,a):
    return (evaluate(poly,add(r,a))+evaluate(poly,add(r,scale(-1,a)))-2*evaluate(poly,r)-2*evaluate(poly,a))/2
result={}
for m in [Q(197),Q(198),Q(256),Q(1000),Q(1000000)]:
    beta=(m*m-1)/(m*m+1)
    poly=plus(plus(mul(norm2,norm2),times(Q(12),mul(qpoly,qpoly))),times(4*beta,mul(qpoly,xpoly)))
    rp=(Q(0),m,Q(-1),Q(0));fp=evaluate(poly,rp)
    assert dot(derivative(poly,rp),A)==0
    upper=polar_c2(poly,rp,A)/det(rp)
    lower=(polar_c2(poly,RM,A)-dot(derivative(poly,RM),A)**2/(4*evaluate(poly,RM)))/det(RM)
    assert upper==24+16*m/(m*m+1)
    assert lower==2*(297*beta**2+603*beta+268)/(24*beta+73)
    gap=lower-upper
    assert gap>0
    tp=Q(1);bound=min(Q(1),det(rp)*gap/(2*fp))
    while tp>bound:tp/=2
    tm=-dot(derivative(poly,RM),A)/(2*evaluate(poly,RM))
    witness=compile_pair(poly,A,scale(tp,rp),scale(tm,RM))
    witness.update(parameter=m,beta=beta,upper_cut=upper,lower_cut=lower,increment_scales=(tp,tm))
    result[str(m)]=witness
    print('m',m,'gap',float(gap),'J',float(witness['jensen_defect']),'maxbits',witness['largest_output_bit_length'])
Path(__file__).with_name('EXACT_FAMILY_WITNESSES.json').write_text(json.dumps(encode(result),indent=2)+'\n')
