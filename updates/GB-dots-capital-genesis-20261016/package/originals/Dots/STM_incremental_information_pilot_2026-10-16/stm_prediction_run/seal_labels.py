"""Separately root-authorized raw-byte seal. No outcome decoding or summaries."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import train
from prediction_stage import require

def seal_labels(sanitized,output,approval):
    require(approval=='ROOT_LABEL_HASH_ONLY_APPROVED','Separate root hash-only label seal approval required')
    path=Path(sanitized).resolve().parent/'sealed'/'test_labels.jsonl'
    require(stat.S_IMODE(path.stat().st_mode)==0o400,'Sealed labels must remain mode 0400')
    # Hash raw bytes only: no text decoding, JSON parsing, counting or outcome inspection.
    raw=path.read_bytes()
    seal={'version':'hash-only-label-seal-v1','label_path':str(path),'label_sha256':hashlib.sha256(raw).hexdigest(),'operation':'raw-byte hashing only; no decoding or outcomes inspected'}
    train.save_new(output,seal)
    return train.digest(output)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for arg in ('sanitized','output','approval'): p.add_argument('--'+arg,required=True)
    print(json.dumps({'seal_artifact_sha256':seal_labels(**vars(p.parse_args()))}))
