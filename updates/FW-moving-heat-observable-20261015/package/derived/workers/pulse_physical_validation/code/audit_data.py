"""Audit the original Zenodo MATs without inventing an acquired current channel."""
from pathlib import Path
from fractions import Fraction
import hashlib, json, platform
import numpy as np
from scipy.io import loadmat

BASE = Path(__file__).resolve().parents[1]
EXPECTED = {
    'impedance.mat': '73d6c64790063f076f24b47d4781a1c7',
    'pocv.mat': '6193e6355e9d845f77b4decf691afa38',
    'pulse.mat': '035611fc459b22e26daf64423145fe01',
}

def load():
    return tuple(loadmat(BASE/'data'/name, simplify_cells=True)[key]
                 for name, key in [('impedance.mat','impedance'),
                                   ('pulse.mat','pulse'), ('pocv.mat','pocv')])

def pulse_info(pulse, sign, cell=0):
    t = pulse[sign+'_time'][:,cell]
    v = pulse[sign+'_voltage'][:,cell]
    # Arrays are rectangular exports; some shorter traces have trailing zeros.
    # A zero voltage is padding in this 2.5--4.2 V cell experiment.
    valid=np.isfinite(t)&np.isfinite(v)&(v>2)&(t>=0)
    t=t[valid]; v=v[valid]
    assert len(t)>100 and np.all(np.diff(t)>0), (sign,cell)
    direction = 1 if sign == 'pos' else -1
    dv = direction*np.diff(v)
    ion = int(np.argmax(dv)) + 1
    ioff = int(np.argmin(dv)) + 1
    # Step locations are intervals inferred from voltage, not acquired current.
    on_bracket = [float(t[ion-1]),float(t[ion])]
    off_bracket = [float(t[ioff-1]),float(t[ioff])]
    # Last two samples repeat a voltage near the end of the commanded pulse.
    # Retain last distinct sample, and assume off follows the duplicated sample.
    end = ioff-2
    off_assumed = float(t[ioff-1] + .001)
    on_assumed = off_assumed - 10.
    baseline = float(np.median(v[:ion]))
    return {'t':t, 'v':v, 'direction':direction, 'on_index':ion, 'off_index':ioff,
            'end_index':end, 'baseline_V':baseline,
            'on_bracket_s':on_bracket, 'off_bracket_s':off_bracket,
            'valid_trace_samples':int(len(t)), 'padding_samples_removed':int((~valid).sum()),
            'assumed_on_s':on_assumed, 'assumed_off_s':off_assumed,
            'endpoint_delta_mV':float(direction*(v[end]-baseline)*1000),
            'pre_pulse_range_mV':float(np.ptp(v[:ion])*1000),
            'final_baseline_delta_mV':float(direction*(v[-1]-baseline)*1000)}

def main():
    z,p,o = load()
    ledger=[]
    for name,md5 in EXPECTED.items():
        b=(BASE/'data'/name).read_bytes()
        got=hashlib.md5(b).hexdigest()
        assert got==md5, (name,got,md5)
        ledger.append({'file':name, 'bytes':len(b), 'md5':got,
                       'md5_matches_published':True,
                       'sha256':hashlib.sha256(b).hexdigest(),
                       'url':f'https://zenodo.org/records/8369275/files/{name}?download=1'})
    supplied=BASE.parents[1]/'sources/astra_pulse_observable/data/cell_001_eis.csv'
    d=np.loadtxt(supplied,delimiter=',',skiprows=1)
    original=np.column_stack([z['f'][0],z['Z_real'][0],z['Z_imag'][0]])
    assert np.array_equal(d,original)
    np.savetxt(BASE/'data/cell_001_eis_acquired.csv',original,delimiter=',',
               header='frequency_Hz,Z_real_Ohm,Z_imag_Ohm',comments='')
    rows=[]
    for cell in range(92):
        pi=pulse_info(p,'pos',cell); ni=pulse_info(p,'neg',cell)
        vals={'cell_one_based':cell+1,
              'charge_endpoint_rise_mV':pi['endpoint_delta_mV'],
              'discharge_endpoint_fall_mV':ni['endpoint_delta_mV'],
              'directional_endpoint_gap_mV':pi['endpoint_delta_mV']-ni['endpoint_delta_mV'],
              'charge_baseline_V':pi['baseline_V'], 'discharge_baseline_V':ni['baseline_V']}
        ds=.5*10/3600
        for branch in ['ch','dc']:
            curve=o[branch][:,cell]; soc=o['soc']
            center=np.interp(.5,soc,curve)
            up=np.interp(.5+ds,soc,curve)-center
            down=center-np.interp(.5-ds,soc,curve)
            vals[branch+'_forced_OCV_rise_mV']=1000*up
            vals[branch+'_forced_OCV_fall_from_half_SOC_mV']=1000*down
            vals[branch+'_POCV_at_half_SOC_V']=center
        rows.append(vals)
    keys=list(rows[0]); np.savetxt(BASE/'results/paired_endpoints_all_92.csv',
        [[r[k] for k in keys] for r in rows], delimiter=',',header=','.join(keys),comments='')
    details={}
    for sign in ['pos','neg']:
        info=pulse_info(p,sign)
        details[sign]={k:v for k,v in info.items() if k not in ['t','v']}
        np.savetxt(BASE/f'data/cell_001_{sign}_trace.csv',np.column_stack([info['t'],info['v']]),
                   delimiter=',',header='time_s,voltage_V',comments='')
    gaps=np.array([r['directional_endpoint_gap_mV'] for r in rows])
    meta={'status':'ORIGINAL_DATA_ACQUIRED; CURRENT_INTERFACE_INCOMPLETE',
          'original_data_files':ledger,'original_data_total_bytes':sum(r['bytes'] for r in ledger),
          'mat_keys':{'impedance':list(z),'pulse':list(p),'pocv':list(o)},
          'acquired_current_trace':False,'acquired_capacity_reference_Ah':False,
          'supplied_first_EIS_row_exactly_matches_original':True,
          'pulse_columns_are_cells_EIS_rows_are_cells':True,
          'pulse_cell_001':details,'cell_001_endpoint_and_OCV':rows[0],
          'all_92_directional_gap_mV':{'min':float(gaps.min()),'median':float(np.median(gaps)),
              'max':float(gaps.max()),'positive_count':int((gaps>0).sum())},
          'python':platform.python_version(), 'numpy':np.__version__,
          'assumption_warning':'Switch times inferred from voltage brackets. Rectangular 10 s current is a protocol assumption; absolute amplitude and actual waveform are not acquired. POCV branches measured at C/20 are not an equilibrium OCV certificate.'}
    (BASE/'results/acquisition_audit.json').write_text(json.dumps(meta,indent=2))
    order_rows=[]
    for cell in range(92):
        f=z['f'][cell]; rr=z['Z_real'][cell]
        d=rr[:,None]-rr[None,:]
        d[np.arange(70)[:,None]>=np.arange(70)[None,:]]=-np.inf
        i,j=np.unravel_index(np.argmax(d),d.shape)
        exact=(Fraction(float(rr[i]))-Fraction(float(rr[j])))/2
        order_rows.append({'cell_one_based':cell+1,'higher_frequency_Hz':float(f[i]),
            'lower_frequency_Hz':float(f[j]),'higher_frequency_real_mOhm':float(rr[i]*1000),
            'lower_frequency_real_mOhm':float(rr[j]*1000),
            'minimum_uniform_real_error_mOhm':float(exact*1000),
            'minimum_uniform_real_error_Ohm_exact_rational':str(exact)})
    ordering={'status':'CONTINUUM_MONOTONICITY_REJECTION', 'cell_001':order_rows[0],
        'all_92_positive_count':sum(r['minimum_uniform_real_error_mOhm']>0 for r in order_rows),
        'rows':order_rows,'meaning':'Positive-RC real part is nonincreasing with frequency. Each displayed pair forces uniform real-component error at least half its reversed-order gap. Exact rational arithmetic over acquired IEEE values. Instrument accuracy remains unknown.'}
    (BASE/'results/fullband_ordering.json').write_text(json.dumps(ordering,indent=2))
    print(json.dumps(meta,indent=2))

if __name__=='__main__': main()
