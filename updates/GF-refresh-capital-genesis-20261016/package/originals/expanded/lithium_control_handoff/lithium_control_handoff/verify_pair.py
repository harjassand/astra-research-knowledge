"""Validate independently decoded traces against released workbook exports."""
from recover_mpr_pair import *

workbook = openpyxl.load_workbook(ROOT/'figure 04/analysis/raw data.xlsx', read_only=True, data_only=True)
rows = list(workbook['Figure 4c'].values)
for label, columns in [('CC', (33,34,0,1)), ('P4-8', (45,46,19,20))]:
    data = parse(BASE/FILES[label])
    times = data['time_s']
    assert len(times) > 1 and np.isfinite(times).all()
    assert np.all(np.diff(times) > 0), 'Times must be strictly increasing'
    interval = np.diff(times, prepend=np.nan)
    current = data['dq_mAh'] * 3600 / interval
    print('\n', label)
    for kind, (time_column, value_column) in [('I', columns[:2]), ('V', columns[2:])]:
        pairs = [(r[time_column], r[value_column]) for r in rows
                 if len(r)>value_column and isinstance(r[time_column], (int,float))
                 and isinstance(r[value_column], (int,float))]
        assert pairs, 'No workbook comparison points'
        expected = np.array(pairs)
        indices = np.abs(times[:,None] - expected[:,0]).argmin(axis=0)
        series = current if kind == 'I' else data['Ewe_V']
        time_error = np.max(abs(times[indices] - expected[:,0]))
        value_error = np.max(abs(series[indices] - expected[:,1]))
        assert np.isfinite(time_error) and time_error < 1e-8
        assert np.isfinite(value_error) and value_error < 1e-6
        print(kind, len(pairs), 'max time error', time_error, 'max value error', value_error)
        print('examples (expected pair, decoded value)', list(zip(expected[:6].tolist(), series[indices[:6]].tolist())))
print('PASS: all exported voltage and current points agree within asserted tolerances.')
