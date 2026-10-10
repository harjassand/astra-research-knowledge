"""Pinned-source loading and evidence serialization; standard library only."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PILOT = Path(__file__).resolve().parent
REVISION = "90bd835a23d3ecdd8815b84ad2be8660389449b2"
SOURCE = ROOT / ("updates/CS/package/Astra_Global_Coupling_Proofs_2026-10-10_0708/"
                 "independent_programme/additive_projection_gate_20261010")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def source_sampler():
    path = SOURCE / "fpt_sampler.py"
    expected = "091070aa6a54adcb472871a68cad56b06120928414ff543364e82cd31042bbc2"
    if sha(path) != expected:
        raise RuntimeError("source sampler differs from the pinned audited bytes")
    spec = importlib.util.spec_from_file_location("n629_original_sampler", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Sampler
