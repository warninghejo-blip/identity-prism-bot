import socket, ssl

ASSIGNED_IPV6 = '2a13:4ac0:20:16:f816:3eff:fe1c:5a73'

# Test 1: Google via assigned IPv6
print(f'Test 1: Connect to google.com:443 from {ASSIGNED_IPV6}')
infos = socket.getaddrinfo('google.com', 443, socket.AF_INET6, socket.SOCK_STREAM)
print(f'  Target: {infos[0][4]}')
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.settimeout(10)
s.bind((ASSIGNED_IPV6, 0, 0, 0))
try:
    s.connect(infos[0][4])
    print('  RESULT: OK')
except Exception as e:
    print(f'  RESULT: FAIL - {e}')
finally:
    s.close()

# Test 2: Gemini API via assigned IPv6
print(f'\nTest 2: Gemini API from {ASSIGNED_IPV6}')
infos = socket.getaddrinfo('generativelanguage.googleapis.com', 443, socket.AF_INET6, socket.SOCK_STREAM)
print(f'  Target: {infos[0][4]}')
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.settimeout(10)
s.bind((ASSIGNED_IPV6, 0, 0, 0))
try:
    s.connect(infos[0][4])
    ctx = ssl.create_default_context()
    ss = ctx.wrap_socket(s, server_hostname='generativelanguage.googleapis.com')
    req = b'GET /v1beta/models?key=test HTTP/1.1\r\nHost: generativelanguage.googleapis.com\r\n\r\n'
    ss.send(req)
    resp = ss.recv(2048).decode(errors='replace')
    first_line = resp.split('\r\n')[0]
    print(f'  HTTP response: {first_line}')
    print(f'  RESULT: Connection OK (HTTP layer reached)')
except Exception as e:
    print(f'  RESULT: FAIL - {e}')
finally:
    s.close()

# Test 3: x.com via assigned IPv6
print(f'\nTest 3: x.com from {ASSIGNED_IPV6}')
infos = socket.getaddrinfo('x.com', 443, socket.AF_INET6, socket.SOCK_STREAM)
print(f'  Target: {infos[0][4]}')
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.settimeout(10)
s.bind((ASSIGNED_IPV6, 0, 0, 0))
try:
    s.connect(infos[0][4])
    print('  RESULT: OK')
except Exception as e:
    print(f'  RESULT: FAIL - {e}')
finally:
    s.close()

# Test 4: ifconfig.co — check what IP they see
print(f'\nTest 4: What IP does ifconfig.co see?')
infos = socket.getaddrinfo('ifconfig.co', 443, socket.AF_INET6, socket.SOCK_STREAM)
print(f'  Target: {infos[0][4]}')
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.settimeout(10)
s.bind((ASSIGNED_IPV6, 0, 0, 0))
try:
    s.connect(infos[0][4])
    ctx = ssl.create_default_context()
    ss = ctx.wrap_socket(s, server_hostname='ifconfig.co')
    ss.send(b'GET / HTTP/1.1\r\nHost: ifconfig.co\r\nAccept: text/plain\r\nConnection: close\r\n\r\n')
    resp = ss.recv(4096).decode(errors='replace')
    body = resp.split('\r\n\r\n', 1)[-1].strip()
    print(f'  Visible IP: {body}')
except Exception as e:
    print(f'  RESULT: FAIL - {e}')
finally:
    s.close()
