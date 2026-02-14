import socket, subprocess, time, random

prefix = '2a13:4ac0:20:16'

# Test 1: Add a specific IPv6 to the interface, then connect
test_ip = f'{prefix}:dead:beef:cafe:1234'
print(f'Adding {test_ip}/64 to ens3...')
subprocess.run(['ip', '-6', 'addr', 'add', f'{test_ip}/64', 'dev', 'ens3'], capture_output=True)
time.sleep(1)

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.settimeout(10)
s.bind((test_ip, 0, 0, 0))
print('Bind OK')
try:
    infos = socket.getaddrinfo('google.com', 443, socket.AF_INET6, socket.SOCK_STREAM)
    print(f'Connecting to {infos[0][4]} from {test_ip}')
    s.connect(infos[0][4])
    print('TEST 1 - Added IP: Connect OK!')
except Exception as e:
    print(f'TEST 1 - Added IP: Connect FAIL: {e}')
finally:
    s.close()
    subprocess.run(['ip', '-6', 'addr', 'del', f'{test_ip}/64', 'dev', 'ens3'], capture_output=True)

# Test 2: Try with ip_nonlocal_bind (no add, just bind)
print()
rand_ip = f'{prefix}:{random.randint(1,0xFFFF):04x}:{random.randint(1,0xFFFF):04x}:{random.randint(1,0xFFFF):04x}:{random.randint(1,0xFFFF):04x}'
print(f'Test nonlocal bind to {rand_ip} (NOT added to interface)...')
s2 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s2.settimeout(10)
s2.bind((rand_ip, 0, 0, 0))
print('Bind OK')
try:
    infos = socket.getaddrinfo('google.com', 443, socket.AF_INET6, socket.SOCK_STREAM)
    s2.connect(infos[0][4])
    print('TEST 2 - Nonlocal bind: Connect OK!')
except Exception as e:
    print(f'TEST 2 - Nonlocal bind: Connect FAIL: {e}')
finally:
    s2.close()

# Test 3: Gemini via IPv6 (assigned address)
print()
print('Test 3: Gemini API via IPv6 (assigned addr, no proxy)...')
import urllib.request
try:
    req = urllib.request.Request(
        'https://generativelanguage.googleapis.com/v1beta/models?key=AIzaSyB8QBvk40TeiadlPDxG3a9XZt69ZlKdMyc',
    )
    resp = urllib.request.urlopen(req, timeout=10)
    print(f'TEST 3 - Gemini via default IPv6: HTTP {resp.status}')
except Exception as e:
    print(f'TEST 3 - Gemini via default: FAIL: {e}')
