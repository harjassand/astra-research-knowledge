"""Paid coefficient acquisition and finite-control cubic sensing experiment.

The declared model layout is known; its coefficients are hidden during model
acquisition. Every calibration call evaluates the dense feature vector. During
deployment the protocol observes noisy U, sends r quantizer indices, generates
M actuator weights, and obtains one noisy aggregate of V. Dense actuator and
projection work is charged. Ground truth is used only by the experiment scorer.
"""
from dataclasses import dataclass
from math import ceil, erf, erfc, exp, log2, pi, sqrt
from pathlib import Path
from time import perf_counter
import json
import numpy as np


def layout(r):
    return np.triu_indices(r,k=1)


def features(u,off):
    return np.concatenate(((u*u-1)/sqrt(2),u[...,off[0]]*u[...,off[1]]),axis=-1)


@dataclass
class FunctionOracle:
    r:int
    hidden_coefficients:np.ndarray
    calls:int=0
    feature_entries:int=0
    target_products:int=0

    def evaluate(self,u,v):
        m=len(self.hidden_coefficients)
        phi=features(u,layout(self.r))
        self.calls+=1
        self.feature_entries+=m
        self.target_products+=2*m
        return float(np.dot(phi*self.hidden_coefficients,v)/sqrt(m))


def acquire(oracle,nu,rng):
    r=oracle.r; m=r*(r+1)//2; off=layout(r)
    u=np.zeros(r); v=np.zeros(m); acquired=np.zeros(m)
    for j in range(m):
        u.fill(0); v.fill(0); v[j]=1
        if j>=r:
            i,k=off[0][j-r],off[1][j-r]
            u[i]=u[k]=1
        response=oracle.evaluate(u,v)+nu*rng.choice((-1.0,1.0))
        acquired[j]=(-sqrt(2*m) if j<r else sqrt(m))*response
    return acquired


def normal_density(x):
    return exp(-x*x/2)/sqrt(2*pi)


def normal_cdf(x):
    return erfc(-x/sqrt(2))/2


def quantizer_moments(h,threshold):
    levels=round(threshold/h)
    assert abs(levels*h-threshold)<1e-12
    q2=q4=gq=g2q2=0.0
    for j in range(levels):
        a=j*h; b=(j+1)*h; q=j*h
        mass=normal_cdf(b)-normal_cdf(a)
        first=normal_density(a)-normal_density(b)
        second=mass+a*normal_density(a)-b*normal_density(b)
        q2+=2*q*q*mass
        q4+=2*q**4*mass
        gq+=2*q*first
        g2q2+=2*q*q*second
    tail=erfc(threshold/sqrt(2))/2
    density=normal_density(threshold)
    q2+=2*threshold**2*tail
    q4+=2*threshold**4*tail
    gq+=2*threshold*density
    g2q2+=2*threshold**2*(threshold*density+tail)
    tail4=2*((threshold**3+3*threshold)*density+3*tail)
    return dict(q2=q2,q4=q4,gq=gq,g2q2=g2q2,
                uniform_feature_mse_bound=4*h*h+4*tail4,
                bits_per_coordinate=ceil(log2(2*levels+1)),levels=levels)


def exact_coefficient_error(c,acquired,r,moments):
    diag_second=(moments["q4"]-2*moments["q2"]+1)/2
    diag_cross=(moments["g2q2"]-moments["q2"])/2
    off_second=moments["q2"]**2
    off_cross=moments["gq"]**2
    diagonal=np.sum(c[:r]**2-2*c[:r]*acquired[:r]*diag_cross+acquired[:r]**2*diag_second)
    off=np.sum(c[r:]**2-2*c[r:]*acquired[r:]*off_cross+acquired[r:]**2*off_second)
    return float((diagonal+off)/len(c))


def pack_control(message,levels,bits):
    unsigned=(message.astype(np.int32)+levels).astype(np.uint16)
    binary=((unsigned[...,None]>>np.arange(bits,dtype=np.uint16))&1).astype(np.uint8)
    return np.packbits(binary.reshape(len(message),-1),axis=1,bitorder="little")


def unpack_control(packet,r,levels,bits):
    binary=np.unpackbits(packet,axis=1,count=r*bits,bitorder="little").reshape(len(packet),r,bits)
    unsigned=np.sum(binary.astype(np.int32)*(1<<np.arange(bits)),axis=-1)
    return (unsigned-levels).astype(np.int16)


def run_case(r,seed,trials=8192,noise=0.01,h=0.01,threshold=6.0,nu=1e-7):
    rng=np.random.default_rng(seed)
    m=r*(r+1)//2; off=layout(r); alpha=1/(1+noise)
    hidden=rng.uniform(0.9,1.1,size=m)
    oracle=FunctionOracle(r,hidden)
    start=perf_counter(); acquired=acquire(oracle,nu,rng)
    preparation_seconds=perf_counter()-start
    tau=float(np.mean((hidden-acquired)**2))
    tau_bound=(m+r)*nu*nu
    assert oracle.calls==m
    assert tau<=tau_bound*(1+1e-6)+1e-20
    moments=quantizer_moments(h,threshold)
    coefficient_error=exact_coefficient_error(hidden,acquired,r,moments)
    variance=float(np.mean(hidden*hidden))
    risk=(1-alpha**3)*variance+alpha**3*coefficient_error
    certificate=(sqrt(tau)+float(np.max(np.abs(acquired)))*sqrt(moments["uniform_feature_mse_bound"]))**2
    assert coefficient_error<=certificate+1e-10
    errors=[]; start=perf_counter()
    for first in range(0,trials,256):
        count=min(256,trials-first)
        u=rng.normal(size=(count,r)); v=rng.normal(size=(count,m))
        truth=np.sum(features(u,off)*hidden*v,axis=1)/sqrt(m)
        # These are the only context observations provided to the controller.
        y=u+sqrt(noise)*rng.normal(size=(count,r))
        standardized=y/sqrt(1+noise)
        message=np.sign(standardized)*np.minimum(np.floor(np.abs(standardized)/h),moments["levels"])
        message=message.astype(np.int16)
        # Actually serialize the finite control message; no float context crosses.
        packet=pack_control(message,moments["levels"],moments["bits_per_coordinate"])
        decoded=unpack_control(packet,r,moments["levels"],moments["bits_per_coordinate"])
        assert np.array_equal(message,decoded)
        assert packet.shape[1]==ceil(r*moments["bits_per_coordinate"]/8)
        # The actuator receives only the packed indices and the prepared model.
        quantized=decoded.astype(float)*h
        a=alpha*features(quantized,off)*acquired/sqrt(m)
        norms=np.linalg.norm(a,axis=1)
        directions=np.divide(a,norms[:,None],out=np.zeros_like(a),where=norms[:,None]!=0)
        # One native aggregate; its M multiplications are charged in the ledger.
        last=np.sum(directions*v,axis=1)+sqrt(noise)*rng.normal(size=count)
        prediction=alpha*norms*last
        errors.extend((truth-prediction)**2)
    elapsed=perf_counter()-start
    errors=np.array(errors)
    empirical=float(np.mean(errors)); se=float(np.std(errors,ddof=1)/sqrt(trials))
    assert abs(empirical-risk)<6*se+1e-10
    lower=max(0.0,variance-3*float(np.max(hidden*hidden))*alpha*(r+1)/m)
    result=dict(r=r,M=m,input_dimension=r+m,trials=trials,noise_variance=noise,
                calibration_calls=oracle.calls,calibration_feature_entries=oracle.feature_entries,
                calibration_dense_target_products=oracle.target_products,
                calibration_absolute_error_budget=nu,
                calibration_coefficient_L2_error=tau,calibration_error_bound=tau_bound,
                preparation_seconds=preparation_seconds,
                static_model_bytes=int(acquired.nbytes),static_model_transfer_bits=64*m,
                online_scalar_reads=r+1,online_control_bits=r*moments["bits_per_coordinate"],
                packed_control_bytes_per_input=ceil(r*moments["bits_per_coordinate"]/8),
                actuator_feature_entries_per_input=m,actuator_dense_pattern_entries=m,
                dense_projection_multiplications_per_input=m,
                target_variance=variance,exact_model_and_quantization_coefficient_error=coefficient_error,
                coefficient_error_certificate=certificate,
                predicted_adaptive_MSE=risk,measured_adaptive_MSE=empirical,MSE_standard_error=se,
                full_fixed_orthonormal_noisy_MSE=(1-alpha**3)*variance,
                all_fixed_same_count_MSE_lower_bound=lower,
                experiment_seconds_including_ground_truth_generation=elapsed,
                ordinary_direct_target_oracle="Equivalent ordinary implementation if a native V·phi(U) evaluator exists; no runtime speedup claimed")
    return result,acquired,moments


def main():
    results=[]
    for r in (8,16,32,64):
        case,acquired,moments=run_case(r,20261101+r)
        results.append(case)
    out=dict(status="PASS",cases=results,
             quantizer=dict(step=0.01,threshold=6.0,levels=2*moments["levels"]+1,
                            bits_per_coordinate=moments["bits_per_coordinate"],
                            dimension_uniform_feature_MSE_bound=moments["uniform_feature_mse_bound"]),
             scope="Known feature layout; unknown coefficients acquired by actual function values. Software source simulation charges dense projection work. Fixed comparator is a universal lower bound, not an empirically optimized policy.")
    directory=Path(__file__).parent
    (directory/"learn_quantized_cubic_results.json").write_text(json.dumps(out,indent=2)+"\n")
    np.savez(directory/"learned_cubic_model.npz",coefficients=acquired,r=np.array(64),
             quantizer_step=np.array(0.01),quantizer_threshold=np.array(6.0),noise_variance=np.array(0.01))
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
