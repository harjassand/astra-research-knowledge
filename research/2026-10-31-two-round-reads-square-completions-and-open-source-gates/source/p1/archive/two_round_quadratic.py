"""Two-round linear measurement of Gaussian quadratic targets.

The mathematical theorem is separate from this floating implementation. The
source model is acquired through explicitly counted scalar evaluations. A
linear read is a unit-direction scalar response, with optional IID Gaussian
readout noise. Dense direction construction and inner-product work are paid.
"""
from dataclasses import dataclass
from pathlib import Path
import json
import math
import time
import numpy as np


class ModelOracle:
    def __init__(self, matrix, linear, constant, error_bound=0.0, seed=17):
        self._matrix = np.asarray(matrix)
        self._linear = np.asarray(linear)
        self._constant = constant
        self.error_bound = error_bound
        self.rng = np.random.default_rng(seed)
        self.calls = 0
        self.submitted_coordinates = 0

    def __call__(self, x):
        self.calls += 1
        self.submitted_coordinates += len(x)
        value = x @ self._matrix @ x + self._linear @ x + self._constant
        return value + self.rng.uniform(-self.error_bound, self.error_bound)


def acquire_quadratic(oracle, n):
    """Promised quadratic; chosen real inputs, all scalar calls charged."""
    zero = np.zeros(n)
    c = oracle(zero)
    plus, minus = np.zeros(n), np.zeros(n)
    for i in range(n):
        x = zero.copy(); x[i] = 1
        plus[i] = oracle(x)
        x[i] = -1
        minus[i] = oracle(x)
    b = (plus-minus)/2
    a = np.diag((plus+minus-2*c)/2)
    for i in range(n):
        for j in range(i+1, n):
            x = zero.copy(); x[i] = x[j] = 1
            a[i, j] = a[j, i] = (oracle(x)-plus[i]-plus[j]+c)/2
    return a, b, c


class LinearSensor:
    def __init__(self, latent, noise_variance, rng):
        self._latent = latent
        self.noise_variance = noise_variance
        self.rng = rng
        self.reads = 0
        self.inner_product_coordinates = 0

    def read(self, unit_vector):
        if not np.isclose(unit_vector @ unit_vector, 1, atol=1e-10):
            raise ValueError('Each measurement direction must have unit norm.')
        self.reads += 1
        self.inner_product_coordinates += len(unit_vector)
        return (unit_vector @ self._latent
                + math.sqrt(self.noise_variance)*self.rng.normal())


@dataclass
class TwoRoundPlan:
    matrix: np.ndarray
    linear: np.ndarray
    constant: float
    budget_parameter: int

    def __post_init__(self):
        a, b, k = self.matrix, self.linear, self.budget_parameter
        n = len(b)
        values, vectors = np.linalg.eigh(a)
        positive = sorted((i for i, v in enumerate(values) if v > 0),
                          key=lambda i: -values[i])
        negative = sorted((i for i, v in enumerate(values) if v < 0),
                          key=lambda i: values[i])
        count = min(k, len(positive), len(negative))
        columns = []
        for j in range(count):
            ip, im = positive[j], negative[j]
            lam, mu = values[ip], -values[im]
            columns.append((math.sqrt(lam)*vectors[:, ip]
                            - math.sqrt(mu)*vectors[:, im])/math.sqrt(lam+mu))
        for indices in (positive, negative):
            columns.extend(vectors[:, i] for i in indices[count:k])
        self.first = np.column_stack(columns) if columns else np.zeros((n, 0))
        self.h = self.first.T @ a @ self.first
        au = a @ self.first
        self.cross = au-self.first @ self.h
        self.b_first = self.first.T @ b
        self.b_rest = b-self.first @ self.b_first
        self.compressed = (a-au @ self.first.T-self.first @ au.T
                           +self.first @ self.h @ self.first.T)
        self.compressed = (self.compressed+self.compressed.T)/2
        self.trace_rest = np.trace(self.compressed)
        self.signed_tail_bound = 2*sum(values[i]**2
                                     for i in positive[k:]+negative[k:])
        self.compression_energy = 2*np.sum(self.compressed**2)
        self.orthogonality_residual = np.linalg.norm(
            self.first.T @ self.first-np.eye(self.first.shape[1]))
        self.inertia = (len(positive), len(negative), n-len(positive)-len(negative))

    def predict(self, sensor):
        """Read through the sensor only; does not inspect latent coordinates."""
        s = sensor.noise_variance
        alpha = 1/(1+s)
        first_y = np.array([sensor.read(u) for u in self.first.T])
        mean_y = alpha*first_y
        base = (self.constant+mean_y @ self.h @ mean_y
                +(1-alpha)*np.trace(self.h)+self.b_first @ mean_y
                +self.trace_rest)
        t = self.b_rest+2*self.cross @ mean_y
        norm = np.linalg.norm(t)
        if norm <= 1e-13:
            return base
        direction = t/norm
        z = sensor.read(direction)
        rayleigh = direction @ self.compressed @ direction
        return (base+alpha*norm*z
                +alpha**2*rayleigh*(z*z-(1+s)))


def coefficient_l2_error(a, b, c, fitted):
    ah, bh, ch = fitted
    da, db, dc = a-ah, b-bh, c-ch
    return float(2*np.sum(da*da)+db@db+(np.trace(da)+dc)**2)


def acquired_dense_fixture():
    rng = np.random.default_rng(31654)
    n, k, nu = 32, 16, 1e-6
    q = np.linalg.qr(rng.normal(size=(n, n)))[0]
    values = np.r_[np.linspace(.4, 1.3, k), -np.linspace(.5, 1.6, k)]
    a = (q*values) @ q.T
    a /= math.sqrt(2*np.sum(a*a))
    b = rng.normal(size=n)/math.sqrt(10*n)
    c = .27
    oracle = ModelOracle(a, b, c, error_bound=nu)
    start = time.perf_counter()
    fitted = acquire_quadratic(oracle, n)
    acquisition_seconds = time.perf_counter()-start
    assert oracle.calls == (n+1)*(n+2)//2
    tau2 = coefficient_l2_error(a, b, c, fitted)
    tau2_bound = (12*n*n+5*n+1)*nu*nu
    assert tau2 <= tau2_bound
    start = time.perf_counter()
    plan = TwoRoundPlan(*fitted, budget_parameter=k)
    planning_seconds = time.perf_counter()-start
    assert plan.first.shape[1] == k
    assert plan.compression_energy < 1e-20
    records = []
    for noise in (0.0, .01):
        count = 8000
        errors = []
        actual_reads = 0
        coordinate_work = 0
        start = time.perf_counter()
        for _ in range(count):
            x = rng.normal(size=n)
            sensor = LinearSensor(x, noise, rng)
            predicted = plan.predict(sensor)
            target = x @ a @ x+b @ x+c
            errors.append((target-predicted)**2)
            actual_reads += sensor.reads
            coordinate_work += sensor.inner_product_coordinates
        seconds = time.perf_counter()-start
        ah, bh, _ = fitted
        alpha = 1/(1+noise)
        ideal_fitted_risk = (2*(1-alpha*alpha)*np.sum(ah*ah)
                            +(1-alpha)*(bh@bh))
        true_risk_upper = (math.sqrt(max(0,ideal_fitted_risk))
                           +math.sqrt(tau2_bound))**2
        observed, se = float(np.mean(errors)), float(np.std(errors, ddof=1)/math.sqrt(count))
        assert observed <= true_risk_upper+5*se+1e-12
        records.append({'noise_variance':noise,'deployments':count,
                        'scalar_reads_total':actual_reads,
                        'scalar_reads_per_deployment':actual_reads/count,
                        'dense_inner_product_coordinates_total':coordinate_work,
                        'mse':observed,'mse_standard_error':se,
                        'fitted_model_exact_risk_formula':float(ideal_fitted_risk),
                        'true_model_risk_upper_using_acquisition_error':true_risk_upper,
                        'wall_seconds_including_validation_target_evaluation':seconds})
    return {'n':n,'first_batch':k,'scalar_model_evaluations':oracle.calls,
            'dense_submitted_model_coordinates':oracle.submitted_coordinates,
            'scalar_model_error_bound':nu,'actual_model_L2_squared_error':tau2,
            'certified_coefficient_error_bound_squared':tau2_bound,
            'acquisition_wall_seconds':acquisition_seconds,
            'planning_wall_seconds':planning_seconds,
            'fitted_inertia':plan.inertia,'compression_energy':float(plan.compression_energy),
            'orthogonality_residual':float(plan.orthogonality_residual),
            'deployment':records,
            'scope':'Synthetic bounded-error source acquisition and floating eigensolve. Error certificate is algebraic under the supplied bounded-readout contract; no unknown quadratic promise or noise model is learned.'}


def noisy_inner_product_fixture():
    rng = np.random.default_rng(74191)
    m, s, count, batch = 128, .01, 40000, 1000
    alpha = 1/(1+s)
    error_lists = [[], [], []]
    start = time.perf_counter()
    for offset in range(0, count, batch):
        size = min(batch,count-offset)
        u = rng.normal(size=(size,m)); v = rng.normal(size=(size,m))
        target = np.sum(u*v,axis=1)/math.sqrt(m)
        y = u+math.sqrt(s)*rng.normal(size=(size,m))
        norm = np.linalg.norm(y,axis=1)
        last = np.sum(y*v,axis=1)/norm+math.sqrt(s)*rng.normal(size=size)
        adaptive = alpha**2*norm*last/math.sqrt(m)
        yp=(u+v)/math.sqrt(2)+math.sqrt(s)*rng.normal(size=(size,m))
        ym=(u-v)/math.sqrt(2)+math.sqrt(s)*rng.normal(size=(size,m))
        scale=alpha**2/(2*math.sqrt(m))
        fixed_partial=scale*(np.sum(yp*yp-(1+s),axis=1)-(ym[:,0]**2-(1+s)))
        fixed_full=scale*(np.sum(yp*yp,axis=1)-np.sum(ym*ym,axis=1))
        for out,prediction in zip(error_lists,(adaptive,fixed_partial,fixed_full)):
            out.extend((target-prediction)**2)
    theoretical=(1-alpha**2,1-(m+1)*alpha**2/(2*m),1-alpha**2)
    records=[]
    for label,reads,errors,formula in zip(('two_round','optimal_fixed_same_budget','full_fixed'),
                                        (m+1,m+1,2*m),error_lists,theoretical):
        mean=float(np.mean(errors));se=float(np.std(errors,ddof=1)/math.sqrt(count))
        assert abs(mean-formula)<=5*se
        records.append({'method':label,'reads_per_input':reads,'MSE_formula':formula,
                        'MSE_observed':mean,'MSE_standard_error':se,
                        'total_scalar_reads':reads*count})
    return {'m':m,'latent_dimension':2*m,'noise_variance_every_read':s,
            'deployments_per_method':count,'records':records,
            'dynamic_direction_coefficients_per_input':m,
            'wall_seconds_all_methods_and_reference':time.perf_counter()-start,
            'scope':'Monte Carlo consistency check of proved risks; latent generation and validation access are separate from the restricted measurement algorithms. No end-to-end runtime dominance claimed.'}


if __name__ == '__main__':
    result={'acquired_dense_model':acquired_dense_fixture(),
            'all_noisy_comparison':noisy_inner_product_fixture(),
            'status':'PASS'}
    Path(__file__).with_name('two_round_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
