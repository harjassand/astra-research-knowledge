"""NumPy batch evaluator for the source-pinned six-species seven-reaction model.

Species axis is 0: Y.shape == (6, N), T.shape == (N,). SI units use kmol for
reaction progress: mass_production kg/m3/s; rho kg/m3; cp J/kg/K;
h_species J/kg; viscosity Pa*s; conductivity W/m/K. Domain: 200–3500 K,
1 atm. This is a numerical replacement, not validation of the source mechanism.
"""
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent


class Kernel:
    def __init__(self, cache_dir=ROOT, verify=True):
        root = Path(cache_dir)
        self.manifest = json.loads((root / 'manifest.json').read_text())
        if verify and hashlib.sha256((root / 'cache.npz').read_bytes()).hexdigest() != self.manifest['cache_sha256']:
            raise ValueError('Pinned cache SHA-256 mismatch')
        with np.load(root / 'cache.npz', allow_pickle=False) as data:
            for key in data.files:
                setattr(self, key, data[key].copy())
        self.W = self.molecular_weights
        self.nu = self.products - self.reactants
        self.delta_nu = self.nu.sum(axis=0)
        c = self.manifest['constants']
        self.R, self.A, self.P0 = c['R_J_kmol_K'], c['avogadro_per_kmol'], c['reference_pressure_Pa']
        self.species_names = tuple(self.manifest['species'])
        if self.species_names != ('N2', 'O2', 'N', 'O', 'NO', 'NO2'):
            raise ValueError('Wrong pinned species order')
        self.third_body_efficiencies = np.array([[1., 1., 2.2, 2.2, 1., 1.],
                                                 [.25, 1., 3.5, 3.5, 1., 1.],
                                                 [1., 1., 1., 1., 1., 1.]])
        self._wilke_mass_quarter = (self.W[None, :] / self.W[:, None]) ** .25
        self._wilke_denominator = np.sqrt(8. * (1. + self.W[:, None] / self.W[None, :]))

    def _state(self, T, Y, P, strict):
        T, Y = np.asarray(T, dtype=float), np.asarray(Y, dtype=float)
        if T.ndim > 1 or Y.ndim not in (1, 2):
            raise ValueError('Expected T scalar/(N,) and Y (6,)/(6,N)')
        T = np.atleast_1d(T)
        if Y.ndim == 1:
            Y = Y[:, None]
        if Y.shape[0] != 6 or not T.size or not Y.shape[1]:
            raise ValueError('Expected six species and a nonempty batch')
        n = max(T.size, Y.shape[1])
        T = np.broadcast_to(T, (n,))
        Y = np.broadcast_to(Y, (6, n))
        P = np.broadcast_to(np.asarray(P, dtype=float), (n,))
        if not (np.isfinite(T).all() and np.isfinite(Y).all() and np.isfinite(P).all()):
            raise ValueError('Nonfinite T, Y or P is invalid; no clipping of nonfinite inputs')
        if np.any((T < 200.) | (T > 3500.)):
            raise ValueError('Outside validated/tabulated domain 200–3500 K; no extrapolation')
        if np.any(P != self.P0):
            raise ValueError('This pinned evaluator is scoped to P = 101325 Pa')
        if strict and (np.any(Y < 0.) or np.any(np.abs(Y.sum(axis=0) - 1.) > 1e-12)):
            raise ValueError('Strict mode requires nonnegative Y and unit mass sum within 1e-12')
        clipped = np.maximum(Y, 0.)
        total = clipped.sum(axis=0)
        if np.any(total <= 0.) or not np.isfinite(total).all():
            raise ValueError('A composition must have finite positive mass after clipping')
        yn = clipped / total
        diagnostics = {'raw_min_Y': Y.min(axis=0), 'raw_sum_Y': Y.sum(axis=0),
                       'negative_input': np.any(Y < 0., axis=0),
                       'normalization_max_change': np.max(np.abs(yn - Y), axis=0)}
        return T, yn, P, diagnostics

    def thermochemistry(self, T):
        """NASA7 Cp/R, h/RT, s/R; Cantera uses low branch at T == Tmid."""
        T = np.atleast_1d(np.asarray(T, dtype=float))
        if T.ndim != 1 or not np.isfinite(T).all() or np.any((T < 200.) | (T > 3500.)):
            raise ValueError('T must be a finite scalar/1D array within 200–3500 K')
        a = np.where(T[None, None, :] <= self.nasa[:, 0, None, None],
                     self.nasa[:, 8:15, None], self.nasa[:, 1:8, None])
        t = T[None, :]
        t2, t3, t4 = t*t, t*t*t, t*t*t*t
        cp_R = a[:, 0] + a[:, 1]*t + a[:, 2]*t2 + a[:, 3]*t3 + a[:, 4]*t4
        h_RT = a[:, 0] + a[:, 1]*t/2 + a[:, 2]*t2/3 + a[:, 3]*t3/4 + a[:, 4]*t4/5 + a[:, 5]/t
        s_R = a[:, 0]*np.log(t) + a[:, 1]*t + a[:, 2]*t2/2 + a[:, 3]*t3/3 + a[:, 4]*t4/4 + a[:, 6]
        return cp_R, h_RT, s_R

    def pure_transport(self, T):
        T = np.atleast_1d(np.asarray(T, dtype=float))
        if T.ndim != 1 or not np.isfinite(T).all() or np.any((T < 200.) | (T > 3500.)):
            raise ValueError('T must be a finite scalar/1D array within 200–3500 K')
        lt = np.log(T)
        ix = np.clip(np.searchsorted(self.log_temperature, lt, side='right') - 1,
                     0, len(self.log_temperature) - 2)
        d = (lt - self.log_temperature[ix])[:, None]
        def interp(coeff):
            a = coeff[:, ix, :]
            return np.exp(((a[0]*d + a[1])*d + a[2])*d + a[3]).T
        return interp(self.mu_coeff), interp(self.conductivity_coeff)

    def evaluate(self, T, Y, P=101325., strict=False, return_rates=False):
        T, Y, P, diagnostics = self._state(T, Y, P, strict)
        invw = Y / self.W[:, None]
        meanw = 1. / invw.sum(axis=0)
        X = invw * meanw
        rho = P * meanw / (self.R * T)
        C = invw * rho
        cp_R, h_RT, s_R = self.thermochemistry(T)
        h_species = h_RT * (self.R*T) / self.W[:, None]
        cp_species = cp_R * self.R / self.W[:, None]
        cp = (Y * cp_species).sum(axis=0)
        g_RT = h_RT - s_R
        log_Kc = -self.nu.T @ g_RT + self.delta_nu[:, None] * np.log(self.P0 / (self.R*T))
        lt, A = np.log(T), self.A
        log_k = np.stack([
            np.log(5e-14*A) - 113200./T + np.log(-np.expm1(-3354./T)),
            np.log(3.7e-14*A) - 59380./T + np.log(-np.expm1(-2238./T)),
            np.log(3e-16*A) - 38000./T,
            np.log(9.7e-21*A) + 1.01*lt - 3120./T,
            np.log(2.4e-15*A) - 74700./T,
            np.log(4.9e-16*A) - .4*lt,
            np.log(5.5e-18*A) + 188./T])
        third = self.third_body_efficiencies @ C
        log_k[0] += np.log(third[0])
        log_k[1] += np.log(third[1])
        log_k[4] += np.log(third[2])
        log_Pr = np.log(9.2e-40*A*A) - 1.6*lt + np.log(third[2]) - log_k[5]
        # log(Pr/(1+Pr)), evaluated without overflow or loss at small Pr.
        log_k[5] -= np.logaddexp(0., -log_Pr)
        with np.errstate(divide='ignore'):
            lc = np.log(C)
        log_reactants = np.stack([lc[0], lc[1], lc[0]+lc[3], lc[1]+lc[2], lc[4], lc[4]+lc[3], lc[5]+lc[3]])
        log_products = np.stack([2*lc[2], 2*lc[3], lc[4]+lc[2], lc[4]+lc[3], lc[2]+lc[3], lc[5], lc[4]+lc[1]])
        lf, lr = log_k + log_reactants, log_k - log_Kc + log_products
        # A signed expm1 difference avoids ordinary subtraction of nearly equal
        # fluxes. Exact equality (including -inf, -inf) is an exact zero.
        q = np.zeros_like(lf)
        pos, neg = lf > lr, lf < lr
        q[pos] = np.exp(lf[pos]) * (-np.expm1(lr[pos] - lf[pos]))
        q[neg] = -np.exp(lr[neg]) * (-np.expm1(lf[neg] - lr[neg]))
        mass_production = (self.nu @ q) * self.W[:, None]
        mu, lam = self.pure_transport(T)
        phi = (1. + np.sqrt(mu[:, None, :] / mu[None, :, :]) * self._wilke_mass_quarter[:, :, None])**2 / self._wilke_denominator[:, :, None]
        viscosity = np.sum(X * mu / np.einsum('ijn,jn->in', phi, X), axis=0)
        conductivity = .5 * ((X*lam).sum(axis=0) + 1. / (X/lam).sum(axis=0))
        result = {'mass_production': mass_production, 'rho': rho, 'cp': cp,
                  'h_species': h_species, 'enthalpy': (Y*h_species).sum(axis=0),
                  'viscosity': viscosity, 'conductivity': conductivity,
                  'T': T, 'Y': Y, 'X': X, 'diagnostics': diagnostics}
        if return_rates:
            result.update(net_rates_of_progress=q, forward_rates_of_progress=np.exp(lf),
                          reverse_rates_of_progress=np.exp(lr), log_Kc=log_Kc,
                          cp_species=cp_species, h_RT=h_RT, s_R=s_R)
        if any(not np.isfinite(v).all() for v in result.values() if isinstance(v, np.ndarray)):
            raise FloatingPointError('Nonfinite evaluator output; state rejected')
        return result

    def temperature_from_enthalpy(self, h, Y, P=101325., T_guess=None,
                                  strict=False, trial_clamp=False,
                                  atol=1e-6, rtol=2e-13, max_iter=80):
        """Safeguarded, branch-aware HPY inversion, returning T plus diagnostics.

        Default rejects out-of-domain h and gaps at the NASA splice. Only the
        explicit trial_clamp=True option (in non-strict mode) clamps h; both the
        original and effective residuals are returned. Source NASA fits have a
        small 1000 K enthalpy jump. If h admits two roots, T_guess selects the
        branch; absent a guess the low branch wins. This ambiguity is reported.
        No extrapolation beyond 200–3500 K is performed.
        """
        if (not np.isscalar(atol) or not np.isscalar(rtol)
                or not np.isfinite(atol) or not np.isfinite(rtol)
                or atol < 0. or rtol < 0.):
            raise ValueError('HP atol and rtol must be finite nonnegative scalars')
        if isinstance(max_iter, (bool, np.bool_)) or not isinstance(max_iter, (int, np.integer)) or max_iter < 1:
            raise ValueError('HP max_iter must be a positive integer')
        if strict and trial_clamp:
            raise ValueError('trial_clamp is not allowed in strict accepted-state mode')
        h = np.asarray(h, dtype=float)
        if h.ndim > 1:
            raise ValueError('Enthalpy must be scalar or shape (N,)')
        h = np.atleast_1d(h)
        yy = np.asarray(Y, dtype=float)
        n = max(h.size, yy.shape[1] if yy.ndim == 2 else 1)
        h = np.broadcast_to(h, (n,))
        if not np.isfinite(h).all():
            raise ValueError('Nonfinite target enthalpy')
        _, Y, _, diagnostics = self._state(np.full(n, 300.), Y, P, strict)
        if T_guess is not None:
            guess = np.broadcast_to(np.asarray(T_guess, dtype=float), (n,))
            if not np.isfinite(guess).all():
                raise ValueError('Nonfinite temperature guess')
        else:
            guess = None
        def thermo(t):
            cp_R, h_RT, _ = self.thermochemistry(t)
            cp = (Y * (cp_R * self.R / self.W[:, None])).sum(axis=0)
            hh = (Y * (h_RT * (self.R*t) / self.W[:, None])).sum(axis=0)
            if np.any(cp <= 0.) or not np.isfinite(cp).all():
                raise FloatingPointError('Nonpositive/nonfinite cp encountered in HP inversion')
            return hh, cp
        a, mid, right, b = 200., 1000., np.nextafter(1000., np.inf), 3500.
        ha, _ = thermo(np.full(n, a)); hl, _ = thermo(np.full(n, mid))
        hr, _ = thermo(np.full(n, right)); hb, _ = thermo(np.full(n, b))
        tol = atol + rtol * np.maximum(1., np.abs(h))
        if not np.isfinite(tol).all():
            raise ValueError('HP residual tolerance overflowed')
        # Feasibility is independent of the caller's solver tolerance. Only a
        # float64 roundoff allowance may soften the domain or NASA-gap boundary.
        domain_tol = 32*np.finfo(float).eps*np.maximum(1., np.abs(h))
        outside = (h < ha-domain_tol) | (h > hb+domain_tol)
        gap = (h > hl+domain_tol) & (h < hr-domain_tol)
        infeasible = outside | gap
        if np.any(infeasible) and not trial_clamp:
            indices = np.flatnonzero(infeasible)[:10].tolist()
            raise ValueError(f'Enthalpy outside 200–3500 K domain or in NASA splice gap at indices {indices}; explicit nonstrict trial_clamp required to clip')
        target = np.clip(h, ha, hb)
        nearest_low = abs(target-hl) <= abs(target-hr)
        target = np.where(gap, np.where(nearest_low, hl, hr), target)
        ambiguous = (hr <= hl) & (target >= hr-domain_tol) & (target <= hl+domain_tol)
        low = target <= hl+domain_tol
        if guess is not None:
            low = np.where(ambiguous, guess <= mid, low)
        lo = np.where(low, a, right)
        hi = np.where(low, mid, b)
        h_lo = np.where(low, ha, hr)
        h_hi = np.where(low, hl, hb)
        # Tiny roundoff-only excursions near branch endpoints are snapped within
        # the stated residual tolerance, without hiding the original residual.
        target = np.clip(target, h_lo, h_hi)
        t = lo + (hi-lo)*(target-h_lo)/(h_hi-h_lo) if guess is None else np.clip(guess, lo, hi)
        done = np.zeros(n, dtype=bool)
        iterations = np.zeros(n, dtype=int)
        residual = np.full(n, np.inf)
        for _ in range(max_iter):
            hh, cp = thermo(t)
            residual = hh-target
            active = ~done
            iterations[active] += 1
            done |= abs(residual) <= tol
            if done.all():
                break
            lo = np.where((residual < 0.) & ~done, t, lo)
            hi = np.where((residual >= 0.) & ~done, t, hi)
            trial = t-residual/cp
            safe = np.isfinite(trial) & (trial > lo) & (trial < hi)
            trial = np.where(safe, trial, .5*(lo+hi))
            t = np.where(done, t, trial)
        else:
            bad = np.flatnonzero(~done)[:10].tolist()
            raise RuntimeError(f'HP inversion failed residual tolerance at indices {bad}; no state returned')
        diagnostics.update({'enthalpy_clamped': infeasible,
                            'enthalpy_roundoff_snap': (~infeasible) & (target != h),
                            'enthalpy_target_original': h,
                            'enthalpy_target_effective': target,
                            'enthalpy_residual_original_J_kg': residual + target-h,
                            'enthalpy_residual_effective_J_kg': residual,
                            'NASA_splice_ambiguous': ambiguous,
                            'NASA_splice_gap_input': gap,
                            'NASA_splice_jump_J_kg': hr-hl,
                            'HP_iterations': iterations})
        return {'T': t, 'Y': Y, 'diagnostics': diagnostics}

    def evaluate_hpy(self, h, Y, P=101325., T_guess=None, strict=False,
                     trial_clamp=False, return_rates=False):
        """HPY convenience wrapper. See temperature_from_enthalpy diagnostics."""
        inverse = self.temperature_from_enthalpy(h, Y, P, T_guess, strict, trial_clamp)
        result = self.evaluate(inverse['T'], inverse['Y'], P, strict=True, return_rates=return_rates)
        result['diagnostics'].update(inverse['diagnostics'])
        return result
