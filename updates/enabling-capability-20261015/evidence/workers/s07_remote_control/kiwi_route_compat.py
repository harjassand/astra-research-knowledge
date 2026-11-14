#!/usr/bin/env python3
"""Vendor Kiwi recorder, using the current public WebSocket route.

Only compatibility change: the receiver's own public JavaScript, fetched from
http://kiwisdr.kfsdr.com:8073/kiwisdr.min.js on 2026-10-15, opens
``/ws/kiwi/<timestamp>/<stream>``. The pinned recorder still opens the old
``/<timestamp>/<stream>`` route. Authentication, channel admission, ordinary
receiver commands and IQ parsing remain in the vendor client. This does not
override a password, a busy response, a recording limit or receiver policy.
"""
import pathlib
import sys

VENDOR = pathlib.Path(__file__).resolve().parent / "kiwiclient"
sys.path.insert(0, str(VENDOR))
from kiwi.wsclient import ClientHandshakeProcessor
import kiwirecorder

original_handshake = ClientHandshakeProcessor.handshake


def current_public_route(self, resource):
    if not resource.startswith("/ws/"):
        resource = "/ws/kiwi" + resource
    return original_handshake(self, resource)


ClientHandshakeProcessor.handshake = current_public_route

if __name__ == "__main__":
    kiwirecorder.main()
