#!/usr/bin/env python3
"""One requested metadata regression only; no benchmark or unrelated tests."""
import ast
from decimal import Decimal as D
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True

BASE=Path(__file__).resolve().parent
PRE=BASE/'snapshots/pre_scope_terminal_mass_certificate.py'
FINAL=BASE/'snapshots/final_terminal_mass_certificate.py'
EXPECTED='8263cb400c818a7d4a772044ebb0e92f89c96188716f221eb7be7d8227307c50'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def normalized_ast(path):
    tree=ast.parse(path.read_text())
    func=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='interval_certificate')
    # Remove precisely the documented scope clarification and output label.
    assert isinstance(func.body[0],ast.Expr) and isinstance(func.body[0].value,ast.Constant)
    func.body.pop(0)
    final_return=func.body[-1]
    assert isinstance(final_return,ast.Return) and isinstance(final_return.value,ast.Call)
    keyword=next(k for k in final_return.value.keywords if k.arg=='coefficient_scope')
    keyword.value=ast.Constant(value='scope_label_normalized_for_diff_check')
    return ast.dump(tree,include_attributes=False)

def main():
    assert sha(FINAL)==EXPECTED
    assert sha(PRE)=='0ab3f8f9d8e642f7cf214fb0a9c0b503afc9ac561eeb8e22f85b9821cb25f1c3'
    assert normalized_ast(PRE)==normalized_ast(FINAL), 'Change extends beyond scope docstring and label'
    spec=importlib.util.spec_from_file_location('final_scope_certificate',FINAL)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=mod
    spec.loader.exec_module(mod)
    np=mod.np
    g=mod.graph(2,[(0,1,1)],[1,1],0,1)
    g.w_bounds=[(D('2'),D('3')),(D('1'),D('1'))]
    cert=mod.interval_certificate(g,np.zeros(2),np.zeros(2),np.array([0]),50)
    assert D(cert['lower'])==2 and D(cert['upper'])==3
    assert cert['coefficient_scope']=='supplied_coefficient_bands'
    prior=json.loads((BASE/'repair_results.json').read_text())['mass_only_bands_metadata']['certificate']
    assert cert['lower']==prior['lower'] and cert['upper']==prior['upper']
    assert prior['coefficient_scope']=='exact_binary64_input_graph'
    result={'status':'PASS_FINAL_SCOPE_METADATA_FIX','final_code_sha256':sha(FINAL),
            'previous_code_sha256':sha(PRE),
            'final_proof_sha256':sha(BASE/'snapshots/final_PROOF.md'),
            'ast_diff_scope':'only interval_certificate docstring and coefficient_scope output expression',
            'counterexample':{'c':1,'nominal_source_mass':1,'source_mass_band':[2,3],
              'old_scope':prior['coefficient_scope'],'new_scope':cert['coefficient_scope'],
              'lower':cert['lower'],'upper':cert['upper'],'numerical_endpoints_unchanged':True},
            'certificate':cert,
            'full_benchmark_rerun':False,
            'unrelated_tests_rerun':False,
            'prior_audit_receipts_preserved':True}
    (BASE/'FINAL_AUDIT_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='certificate'},indent=2))

if __name__=='__main__': main()
