"""Carry statistical scope into a guarded consumer of an inferred model.
This outputs exact classical specifications, not a downstream simulation.
"""
import argparse
import json
from pathlib import Path
from learn_affine_source import verify_learning_record, SCOPE
from acquire_affine_pauli_consumer import acquire_classical_coupling


def acquire_learned_coupling(transcript, learning_record, coupling):
    if not verify_learning_record(transcript, learning_record):
        raise ValueError('The inference record or its scope failed verification.')
    result = acquire_classical_coupling(learning_record['learned_model'],
                                       learning_record['realization'], coupling)
    result['learning_transcript_digest'] = learning_record['transcript_digest']
    result['acquisition_query_count'] = len(learning_record['query_plan']['inputs'])
    result['unconditional_model_failure_upper_bound'] = learning_record['query_plan']['proved_failure_upper_bound']
    result['admitted_transcript_average_failure_upper_bound'] = learning_record['admitted_transcript_average_failure_upper_bound']
    result.update(SCOPE)
    result['downstream_simulation_executed'] = False
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('transcript', type=Path)
    parser.add_argument('learning_record', type=Path)
    parser.add_argument('coupling', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = acquire_learned_coupling(json.loads(args.transcript.read_text()),
                                      json.loads(args.learning_record.read_text()),
                                      json.loads(args.coupling.read_text()))
    output = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
