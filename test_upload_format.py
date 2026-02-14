"""Test curl_cffi multipart upload formats for 0.14.0"""
from curl_cffi import requests as r
import inspect

# Check what request() accepts
sig = inspect.signature(r.Session.request)
print("Session.request params:", list(sig.parameters.keys()))

# Try to find the correct multipart format
from curl_cffi.requests import Session
s = Session()
# Check if 'files' or 'multipart' is the correct kwarg
src = inspect.getsource(s.request)
for keyword in ['multipart', 'files', 'data']:
    if keyword in src:
        print(f"  '{keyword}' found in request() source")
