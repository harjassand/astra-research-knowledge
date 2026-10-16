#!/usr/bin/env python3
"""Conventional waveform-matched filter on a published actual IQ recording.

This demonstrates usable public bytes and a primary incumbent's basic analysis
operation. Peaks do not identify physical paths: emitted repetitions, unknown
receiver response, multipath and demodulation distortion all matter.
"""
import argparse
import json
import pathlib
import time
import wave
import numpy as np
from audit_iq import read_kiwi


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--iq", type=pathlib.Path,
                   default=pathlib.Path("published_data/20211115T190749Z_15000000_N6GNrm_iq.wav"))
    p.add_argument("--reference", type=pathlib.Path,
                   default=pathlib.Path("published_data/test.wav"))
    p.add_argument("--reference-start-s", type=float, default=24)
    p.add_argument("--reference-duration-s", type=float, default=.05)
    p.add_argument("--output", type=pathlib.Path, default=pathlib.Path("MATCHED_CHIRP_BASELINE_v0001.json"))
    args = p.parse_args()
    tic = time.perf_counter()
    _, fmt, blocks = read_kiwi(args.iq)
    iq = np.concatenate([b for _, b in blocks]).astype(np.float64)
    # AM envelope is an explicit supplied demodulation choice, not a calibrated
    # complex transfer-function estimate.
    y = np.hypot(iq[:, 0], iq[:, 1])
    rate = fmt[2]
    with wave.open(str(args.reference)) as w:
        ref_rate = w.getframerate()
        if w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise ValueError("Expected int16 mono source reference")
        w.setpos(round(args.reference_start_s * ref_rate))
        ref = np.frombuffer(w.readframes(round(args.reference_duration_s * ref_rate)), dtype="<i2").astype(float)
    nref = round(len(ref) * rate / ref_rate)
    reference = np.interp(np.arange(nref) / rate,
                          np.arange(len(ref)) / ref_rate, ref)
    reference -= reference.mean()
    nfft = 1 << (len(y) + nref - 2).bit_length()
    convolution = np.fft.irfft(np.fft.rfft(y, nfft) *
                              np.fft.rfft(reference[::-1], nfft), nfft)
    dots = convolution[nref - 1:len(y)]
    c = np.concatenate(([0.], np.cumsum(y)))
    c2 = np.concatenate(([0.], np.cumsum(y * y)))
    sums = c[nref:] - c[:-nref]
    variance = np.maximum(0., c2[nref:] - c2[:-nref] - sums * sums / nref)
    denominator = np.sqrt(variance * np.dot(reference, reference))
    score = np.divide(dots, denominator, out=np.zeros_like(dots), where=denominator > 0)
    remaining = score.copy()
    peaks = []
    exclusion = round(.08 * rate)
    for _ in range(12):
        i = int(np.argmax(remaining))
        peaks.append({"recording_relative_s": i / rate,
                      "normalized_correlation": float(score[i])})
        remaining[max(0, i - exclusion):i + exclusion + 1] = -np.inf
    result = {"iq_file": str(args.iq), "supplied_reference_file": str(args.reference),
              "reference_segment_start_s": args.reference_start_s,
              "reference_segment_duration_s": args.reference_duration_s,
              "recording_sample_rate_header_Hz": rate,
              "reference_sample_rate_Hz": ref_rate,
              "reference_resampling": "linear interpolation, charged preprocessing",
              "operation": "ordinary normalized time-domain matched filtering implemented by FFT",
              "top_peaks": peaks,
              "physical_path_count": "UNKNOWN",
              "absolute_propagation_delay": "UNKNOWN",
              "novelty": "Known incumbent operation, no novelty claim",
              "scope": "Published source-reported physical recording. Waveform alignment only; source timing, receiver calibration, noise law, and path attribution remain unresolved.",
              "analysis_wall_s": time.perf_counter() - tic}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
