"""Offline replay of this cross-route construction; no writes outside BASE."""
import sys
sys.dont_write_bytecode = True
import os, json, hashlib, time, io, contextlib, importlib
from positive_gate import BASE


def run():
    start = time.monotonic()
    inputs = json.loads((BASE/'sources/PEER_SOURCE_SNAPSHOT.json').read_text())
    for row in inputs:
        path = BASE/'sources'/row['snapshot'].split('/')[-1]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    blob = (BASE/'sources/sse_magnet.jl').read_bytes()
    assert hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest() == '72278f25add99c718530db25bd74847417246c78'
    names = ['source_gauge_check', 'positive_gate', 'positive_transfer',
             'positive_cut_test', 'exact_cut_certificate',
             'exponential_positive_gate', 'physical_frame_barrier']
    rows = []
    for name in names:
        tick = time.monotonic(); output = io.StringIO()
        with contextlib.redirect_stdout(output):
            importlib.import_module(name).run()
        rows.append(dict(check=name, status='PASS', seconds=time.monotonic()-tick))
        print(name, 'PASS', flush=True)
    result = dict(status='ALL_SEVEN_INTERNAL_REPLAYS_PASS', checks=rows,
        peer_input_hashes_checked=True, pinned_public_code_blob_checked=True,
        no_live_network_required=True, writes_confined_to=str(BASE),
        elapsed_seconds=time.monotonic()-start,
        scope='Internal replay of stated algebra/interval-free rational checks and finite orientation diagnostics. No independent full audit or cold long-ring trace acquisition.')
    (BASE/'results/REPLAY.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
