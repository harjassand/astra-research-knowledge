"""Challenge the cold-readout obstruction with post-gate smoothing and homodyne.

Uses the same passive collision convention as warm_bus_observation_probe.py, but
never edits that file. Only new cold output modes are measured; intrinsic hot output
modes remain inaccessible. Force is zero during the optional post-gate observation.
The finite collision model has a discretization residual: limits must be ordered.
"""
import json
import numpy as np


def collision_model(steps=80, duration=2., post_steps=0,
                    kh=.3, kc=1., phase=.1):
    dt = duration / steps
    ch, cc = np.exp(-kh*dt/2), np.exp(-kc*dt/2)
    sh, sc = np.sqrt(1-ch*ch), np.sqrt(1-cc*cc)
    decay = ch*cc
    total = steps+post_steps
    modes = 1+2*total
    passive = np.eye(modes)
    displacement = np.zeros(modes, complex)
    phi = 0.
    path = ((np.exp(2j*np.pi*np.arange(steps+1)/steps)-1)
            *np.sqrt(phase/(2*np.pi)))
    for j in range(total):
        increment = path[j+1]-decay*path[j] if j < steps else 0.
        phi += np.imag(increment*np.conj(displacement[0]))
        displacement[0] += increment
        for mode, c, s in ((1+2*j,ch,sh),(2+2*j,cc,sc)):
            old_bus, old_mode = passive[0].copy(), passive[mode].copy()
            passive[0] = c*old_bus+s*old_mode
            passive[mode] = -s*old_bus+c*old_mode
            x, y = displacement[0], displacement[mode]
            displacement[0], displacement[mode] = c*x+s*y, -s*x+c*y
    hot_indices = np.r_[0,np.arange(1,modes,2)]
    cold_indices = np.arange(2,modes,2)
    hot_frame = np.kron(passive[:,hot_indices],np.eye(2))
    selected = np.ravel(np.c_[2*cold_indices,2*cold_indices+1])
    observation = np.eye(2*modes)[selected]
    linear_phase = np.c_[np.sqrt(2)*displacement.imag,
                        -np.sqrt(2)*displacement.real].ravel()
    omega = np.kron(np.eye(modes),[[0,1],[-1,0]])
    return hot_frame, observation, linear_phase, omega, float(phi)


def analyse(steps, post_steps):
    hot, obs, linear, omega, phi = collision_model(steps,post_steps=post_steps)
    # This chooses the best possible linear hot-phase reconstruction, with no
    # heterodyne-noise penalty. Its coefficient can also be measured as ONE
    # collective homodyne quadrature, avoiding simultaneous Q/P measurement.
    operator = hot.T @ obs.T
    target = hot.T @ linear
    gain = np.linalg.lstsq(operator,target,rcond=1e-12)[0]
    residual = target-operator@gain
    corrected_phase = phi-.5*linear@omega@obs.T@gain
    # A single collective quadrature uses the same real vector obs.T@gain;
    # its external measurement-noise contribution can ideally be zero. The hot
    # residual and phase are unchanged by choosing this homodyne implementation.
    return dict(steps=steps,post_steps=post_steps,phi=phi,
                corrected_phase=float(corrected_phase),
                hot_residual_squared=float(residual@residual),
                gain_norm_squared=float(gain@gain))


if __name__ == '__main__':
    results = [analyse(n,p) for n,p in [(20,0),(40,0),(80,0),(160,0),
                                       (40,40),(40,120),(80,80)]]
    print(json.dumps(results,indent=2))
