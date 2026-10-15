#!/usr/bin/env python3
"""Bounded, receive-only acquisition using the pinned official Kiwi client.

Without --execute this only prints a concrete plan. Every executed request gets
new filenames and a receipt. The first acquired IQ file is never overwritten.
No account, password, admin command, RF transmission or persistent label edit
is supported by this launcher.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent
VENDOR_PIN = "4eb733e6b6147f7fbeb97ced64cdac029b202d18"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="kiwisdr.kfsdr.com")
    p.add_argument("--port", type=int, default=8073)
    p.add_argument("--frequency-kHz", type=float, default=10000)
    p.add_argument("--duration-s", type=float, default=8)
    p.add_argument("--gain-dB", type=float, default=0,
                   help="Fixed receiver digital gain; AGC is disabled")
    p.add_argument("--execute", action="store_true")
    args = p.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9.-]+", args.host):
        p.error("Expected a public receiver hostname")
    if not 1 <= args.port <= 65535 or not 1 <= args.duration_s <= 90:
        p.error("Port must be valid and duration 1 to 90 seconds")
    if not 10 <= args.frequency_kHz <= 30000 or not 0 <= args.gain_dB <= 120:
        p.error("Frequency or fixed digital gain outside supported range")
    manifest = json.loads((ROOT / "VENDOR_SNAPSHOT_MANIFEST.json").read_text())
    pin = manifest["source_commit"]
    if pin != VENDOR_PIN:
        raise SystemExit("Vendor pin differs; audit source before acquisition")
    for name, expected in manifest["files"].items():
        actual = hashlib.sha256((ROOT / "kiwiclient" / name).read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit("Vendor source differs: " + name)
    token = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = ROOT / "data" / token
    argv = [sys.executable, str(ROOT / "kiwi_route_compat.py"),
            "-s", args.host, "-p", str(args.port),
            "-f", str(args.frequency_kHz), "-m", "iq", "-w",
            "-g", str(args.gain_dB), "-u", "ScientificInterfaceAudit",
            "--station", "experiment", "--dir", str(target),
            "--tlimit", str(args.duration_s), "--connect-retries", "1",
            "--busy-retries", "1", "--socket-timeout", "8", "--log", "info"]
    receipt = {"time_utc": token, "argv": argv, "vendor_pin": pin,
               "execute_requested": args.execute,
               "scope": "Receive-only public hardware measurement control. Physical source and environment are not actuated.",
               "outer_timeout_s": args.duration_s + 20}
    if not args.execute:
        print(json.dumps(receipt, indent=2))
        return
    target.mkdir(parents=True, exist_ok=False)
    before = time.monotonic()
    with (target / "client.log").open("x") as out:
        try:
            r = subprocess.run(argv, cwd=ROOT, stdout=out,
                               stderr=subprocess.STDOUT,
                               timeout=receipt["outer_timeout_s"])
            receipt["returncode"] = r.returncode
        except subprocess.TimeoutExpired:
            receipt["external_timeout"] = True
    receipt["acquisition_wall_s"] = time.monotonic() - before
    receipt["files"] = [{"file": str(f.relative_to(ROOT)),
                         "bytes": f.stat().st_size,
                         "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
                        for f in sorted(target.glob("*.wav"))]
    receipt["status"] = "IQ_BYTES_ACQUIRED" if receipt["files"] else "NO_IQ_ACQUIRED"
    (target / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
