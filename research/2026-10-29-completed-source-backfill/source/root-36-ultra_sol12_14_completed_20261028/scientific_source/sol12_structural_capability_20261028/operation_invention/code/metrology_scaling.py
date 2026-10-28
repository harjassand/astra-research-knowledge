"""Conditional physical scaling, not an acquired sensing or electrode budget."""
from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[1]

def main():
    eps0=8.8541878128e-12
    rho=2700.0
    # These are the existing source's field and nominal material assumptions.
    # Amplitudes below are reduced to match its two quadratic field budgets.
    E0=1e6;g0=1e9;N=4096
    Ea=math.sqrt(2/3)*E0;ga=math.sqrt(2/3)*g0
    response=9*eps0/rho
    acceleration=Ea*ga*response/2
    relative_noise_goal=0.00046  # Source illustration only, not coverage.
    rows=[]
    for duration in (0.001,0.01,0.1):
        beat=17/duration
        displacement=acceleration/(2*math.pi*beat)**2
        rows.append({
            'observation_seconds':duration,
            'beat_hz':beat,
            'highest_drive_carrier_hz':274/duration,
            'highest_declared_force_band_hz':540/duration,
            'sample_rate_hz':N/duration,
            'target_displacement_amplitude_m':displacement,
            'allowed_independent_position_sample_noise_m':
                relative_noise_goal*displacement*math.sqrt(N/2)})
    out={
        'status':'CONDITIONAL_SCALING_ONLY',
        'field_amplitudes_quadratic_budget_matched':{'uniform_V_per_m':Ea,'gradient_V_per_m2':ga},
        'reference_density_kg_per_m3':rho,
        'reference_PEC_trace_per_mass_SI':response,
        'target_acceleration_amplitude_m_per_s2':acceleration,
        'samples':N,
        'illustrative_relative_random_error_goal':relative_noise_goal,
        'rows':rows,
        'scope':('Known phase harmonic, independent identical position noise, supplied PEC sphere '
                 'response, negligible model/transfer errors. All are assumptions. Initial-motion '
                 'and other-frequency regression, sampling photon cost, drive peak/slew, material '
                 'response, actual pose/torque and coverage are not acquired.')}
    (ROOT/'results/metrology_scaling.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
