"""Compile a rational nine-coefficient input to the exact support SDP.

Output uses unscaled upper Gram entries (diagonal coefficient1,
off-diagonal2), so every affine equation is rational. No solve or QC claim
is performed by compilation. Polynomial/SOS completeness is proved in
POLYCONVEX_PROOF.md§5.
"""
import argparse,json
from pathlib import Path
from poly_support import build

def compile_interface(coefficients):
    _,_,terms,monoms,target,multipliers,z=build(coefficients)
    rows={e:{} for e in monoms}
    for col,(i,j,term) in enumerate(terms):
        for e,c in term.terms():rows[e][col]=str(c*(1 if i==j else 2))
    for j,term in enumerate(multipliers):
        for e,c in term.terms():rows[e][len(terms)+j]=str(c)
    right=dict(target.terms())
    labels=['u-v','q'] if len(multipliers)==2 else ['u','v','w','q']
    return {
        'status':'EXACT_AFFINE_SOS_SUPPORT_INTERFACE_NOT_FEASIBILITY_OR_QC',
        'input_nine_coefficients':[str(c) for c in coefficients],
        'input_basis':['u^2','v^2','uv','w^2','uw','vw','qu','qv','qw'],
        'matrix_variables':26,'symmetric_gram_variables':351,
        'multiplier_basis':labels,'total_variables':351+len(labels),
        'variable_order':[[i,j] for i,j,_ in terms]+['multiplier:'+q for q in labels],
        'monomial_order':'A0,A1,A2,A3,X0,X1,X2,X3',
        'rows':[{'exponent':list(e),'entries':[[j,c] for j,c in sorted(rows[e].items())],
                 'rhs':str(right.get(e,0))} for e in monoms],
        'cone':'The351 Gram entries form a26-by26 symmetric PSD matrix',
        'completeness_scope':'All polynomial SOS minor-support selectors for this homogeneous invariant quartic',
        'not_characterized':['all polyconvex functions','all quasiconvex functions','the rank-one-convex cone'],
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--coefficients',default='["1","1","16","-13","0","0","4","-4","0"]')
    parser.add_argument('--output',default='EXACT_SUPPORT_INTERFACE.json')
    args=parser.parse_args();record=compile_interface(json.loads(args.coefficients))
    Path(args.output).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ['rows','variable_order']},indent=2))
    print('equations',len(record['rows']))

if __name__=='__main__':main()
