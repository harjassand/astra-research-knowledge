"""Read the delivered assay metadata without loading its expression matrix."""
import argparse, json
from collections import Counter
from pathlib import Path
import h5py

def strings(values):
    return [v.decode() if isinstance(v,bytes) else str(v) for v in values]

def column(obj):
    if isinstance(obj,h5py.Dataset):
        return strings(obj[:])
    cats=strings(obj['categories'][:])
    return [cats[i] if i>=0 else '<missing>' for i in obj['codes'][:]]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,required=True)
    args=p.parse_args()
    with h5py.File(args.input,'r') as f:
        result={'shape':[int(v) for v in f['X'].attrs['shape']],
                'matrix_encoding':str(f['X'].attrs['encoding-type']),
                'nonzero_entries':int(f['X/data'].shape[0]),
                'obs_fields':list(f['obs'].keys()),'obsm_fields':list(f['obsm'].keys()),
                'var_fields':list(f['var'].keys()),'selected_metadata':{}}
        for key in ['perturbation','CRISPRcas13_Array','10X_lane','HTO','cell_line','perturbation_type']:
            vals=column(f['obs'][key]);c=Counter(vals)
            result['selected_metadata'][key]={'unique':len(c),'counts':dict(sorted(c.items()))}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
