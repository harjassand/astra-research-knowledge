"""Bound clipping effect on the saved-point trapezoidal collision diagnostic.
This is not a temporal quadrature or physical surface-loss bound.
"""
import numpy as np,json
from pathlib import Path
R=Path(__file__).resolve().parent;z=np.load(R/'heater_H4_signed_T11_blow_10.npz');N=int(z['N']);H=int(z['NH']);M=2*N+H;ids=np.r_[np.arange(N),np.arange(N+H,M)];q=z['state'][:6*M].reshape(6,M,-1);a=q[[4,5]][:,ids];neg=np.maximum(-a,0);mw=np.array([.030006,.046005]);speed=np.sqrt(8.31446261815324*3500/(2*np.pi*mw));v=np.sum(neg/mw[:,None,None]*speed[:,None,None],axis=(0,1))*6*.6/.009525*(.1/N);bound=float(np.trapezoid(v,z['t']));d=json.loads((R/'surface_exposure_diagnostic.json').read_text());r={'scope':__doc__,'maximum_negative_NOx_density_kg_m3':float(neg.max()),'collision_mol_m2_clipping_effect_upper_bound_on_saved_trapezoid':bound,'relative_to_reported_collision_exposure':bound/d['integrated_NOx_collision_mol_m2'],'temperature_upper_bound_used_K':3500};(R/'surface_clipping_bound.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
