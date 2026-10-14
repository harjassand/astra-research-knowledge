"""Portable scratch-output wrapper for the preserved independent echo audit."""
import argparse
import importlib.util
import json
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    script=Path(__file__).with_name('independent_echo_audit.py')
    spec=importlib.util.spec_from_file_location('fd_echo_independent',script)
    audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
    audit.SOURCE=args.source_dir.resolve()
    result=dict(exact_conditional_certificate=audit.exact_certificate(),
                exact_twirl_checks=audit.exact_twirl_checks(),
                independent_matrix_tests=audit.matrix_tests())
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'INDEPENDENT_ECHO_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',scope='Internal exact/finite checks only; no hardware or universal proof certification.',
                         counts=result['independent_matrix_tests']['counts'])))

if __name__=='__main__':main()
