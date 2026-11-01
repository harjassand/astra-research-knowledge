#!/usr/bin/env python3
"""Audit real Kiwi IQ bytes without promoting them to physical truth.

Reads the vendor's RIFF extension. No resampling or interpolation is applied.
GPS time fields are reported as transmitted, without assuming a UTC offset.
"""
import argparse
import hashlib
import json
import pathlib
import struct
import time
import numpy as np


def read_kiwi(path):
    raw = pathlib.Path(path).read_bytes()
    if raw[:4] != b"RIFF" or raw[8:12] != b"WAVE":
        raise ValueError("Not a RIFF WAVE")
    pos = 12
    gps = None
    fmt = None
    chunks = []
    while pos + 8 <= len(raw):
        tag, size = struct.unpack_from("<4sI", raw, pos)
        pos += 8
        body = raw[pos:pos + size]
        if len(body) != size:
            raise ValueError("Truncated chunk")
        if tag == b"fmt ":
            fmt = struct.unpack_from("<HHIIHH", body)
        elif tag == b"kiwi":
            if size != 10:
                raise ValueError("Unexpected kiwi chunk size")
            age, reserved, sec, nsec = struct.unpack("<BBII", body)
            gps = {"last_gps_solution": age, "reserved": reserved,
                   "gpssec": sec, "gpsnsec": nsec}
        elif tag == b"data":
            if fmt is None or fmt[0] != 1 or fmt[1] != 2 or fmt[5] != 16:
                raise ValueError("Expected PCM int16 I/Q")
            a = np.frombuffer(body, dtype="<i2").reshape(-1, 2)
            chunks.append((gps, a.copy()))
        pos += size + (size & 1)
    if pos != len(raw):
        raise ValueError("Unparsed trailer")
    return raw, fmt, chunks


def audit(path):
    tic = time.perf_counter()
    raw, fmt, chunks = read_kiwi(path)
    if not chunks:
        raise ValueError("No IQ chunks")
    a = np.concatenate([z[1] for z in chunks])
    q = a[:, 0].astype(float) + 1j * a[:, 1].astype(float)
    offsets = np.cumsum([0] + [len(z[1]) for z in chunks[:-1]])
    accepted = [(i, g["gpssec"] + 1e-9 * g["gpsnsec"])
                for i, (g, _) in zip(offsets, chunks)
                if g and g["gpssec"] > 0 and g["last_gps_solution"] < 254]
    timing = {"valid_nonzero_blocks": len(accepted),
              "excluded_zero_or_stale_blocks": len(chunks) - len(accepted),
              "gps_age_codes": sorted(set(g["last_gps_solution"] for g, _ in chunks if g))}
    if len(accepted) >= 3:
        n = np.array([z[0] for z in accepted], dtype=float)
        t = np.array([z[1] for z in accepted], dtype=float)
        centered_t = t - t[0]
        fit = np.polyfit(n - n[0], centered_t, 1)
        res = centered_t - np.polyval(fit, n - n[0])
        dt = np.diff(t)
        timing.update(first_gps_seconds_of_week=float(t[0]),
                      last_gps_seconds_of_week=float(t[-1]),
                      monotone=bool(np.all(dt > 0)),
                      fitted_sample_rate_Hz=float(1 / fit[0]),
                      block_interval_min_s=float(dt.min()),
                      block_interval_max_s=float(dt.max()),
                      timing_residual_max_abs_ns=float(np.max(np.abs(res)) * 1e9))
    segment = q[len(q) // 4:]
    segment = segment - np.mean(segment)
    fft_n = min(65536, len(segment))
    segment = segment[:fft_n]
    spectrum = np.abs(np.fft.fftshift(np.fft.fft(segment * np.hanning(fft_n)))) ** 2
    freq = np.fft.fftshift(np.fft.fftfreq(fft_n, 1 / fmt[2]))
    order = np.argsort(spectrum)[::-1]
    peaks = []
    for j in order:
        f = float(freq[j])
        if all(abs(f - p["baseband_Hz"]) > 20 for p in peaks):
            peaks.append({"baseband_Hz": f,
                          "relative_power_dB": float(10 * np.log10(spectrum[j] / spectrum.max()))})
        if len(peaks) >= 8:
            break
    return {"file": str(path), "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw), "riff_length_consistent": struct.unpack_from("<I", raw, 4)[0] + 8 == len(raw),
            "header_sample_rate_Hz": fmt[2], "IQ_frames": len(a), "blocks": len(chunks),
            "duration_from_header_s": len(a) / fmt[2],
            "frames_per_block": sorted(set(len(x) for _, x in chunks)),
            "nonzero_sample_fraction": float(np.count_nonzero(a) / a.size),
            "int16_extreme_fraction": float(np.count_nonzero((a == -32768) | (a == 32767)) / a.size),
            "rms_int16": float(np.sqrt(np.mean(np.abs(q) ** 2))),
            "timing": timing, "spectral_peaks_diagnostic_only": peaks,
            "scope": "Actual received bytes and transmitted timing metadata; RF source identity, physical timing accuracy, instrument calibration, and scientific inference are not independently verified.",
            "audit_wall_s": time.perf_counter() - tic}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("files", nargs="+")
    p.add_argument("--output", type=pathlib.Path)
    args = p.parse_args()
    result = [audit(path) for path in args.files]
    s = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(s + "\n")
    print(s)
