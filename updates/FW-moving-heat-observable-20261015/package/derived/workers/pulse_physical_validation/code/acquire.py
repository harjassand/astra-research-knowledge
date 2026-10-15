"""Download only the three original measurement MATs, verifying published MD5.
Scientific data total: 6,217,033 bytes. Does not acquire a current channel.
"""
from pathlib import Path
import hashlib,json,subprocess
from audit_data import EXPECTED
BASE=Path(__file__).resolve().parents[1]
for name,md5 in EXPECTED.items():
    dest=BASE/'data'/name
    if dest.exists():
        assert hashlib.md5(dest.read_bytes()).hexdigest()==md5
        continue
    temp=dest.with_suffix(dest.suffix+'.part')
    subprocess.run(['curl','--location','--fail','--silent','--show-error',
        '--connect-timeout','15','--max-time','60','--max-filesize','5000000',
        f'https://zenodo.org/records/8369275/files/{name}?download=1',
        '--output',str(temp)],check=True)
    assert hashlib.md5(temp.read_bytes()).hexdigest()==md5
    temp.rename(dest)
print('Acquired or checked three original MATs. Current and capacity calibration remain absent.')
