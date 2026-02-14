import socket, random

prefix = '2a13:4ac0:20:16'
b = random.getrandbits(64)
ipv6 = f'{prefix}:{(b>>48)&0xFFFF:04x}:{(b>>32)&0xFFFF:04x}:{(b>>16)&0xFFFF:04x}:{b&0xFFFF:04x}'
print('Testing bind to', ipv6)

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.settimeout(10)
s.bind((ipv6, 0, 0, 0))
print('Bind OK')

try:
    infos = socket.getaddrinfo('ifconfig.co', 443, socket.AF_INET6, socket.SOCK_STREAM)
    print('AAAA:', infos[0][4])
    s.connect(infos[0][4])
    print('IPv6 Connect OK!')
except Exception as e:
    print('IPv6 Connect FAIL:', e)
finally:
    s.close()

# Test with the real assigned IPv6
print()
print('Testing with assigned IPv6...')
s2 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s2.settimeout(10)
s2.bind(('2a13:4ac0:20:16:f816:3eff:fe1c:5a73', 0, 0, 0))
try:
    infos = socket.getaddrinfo('ifconfig.co', 443, socket.AF_INET6, socket.SOCK_STREAM)
    s2.connect(infos[0][4])
    print('Assigned IPv6 Connect OK!')
except Exception as e:
    print('Assigned IPv6 Connect FAIL:', e)
finally:
    s2.close()

# Test plain IPv6 without bind
print()
print('Testing plain IPv6 (no bind)...')
s3 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s3.settimeout(10)
try:
    infos = socket.getaddrinfo('google.com', 443, socket.AF_INET6, socket.SOCK_STREAM)
    print('google.com AAAA:', infos[0][4])
    s3.connect(infos[0][4])
    print('Plain IPv6 Connect OK!')
except Exception as e:
    print('Plain IPv6 Connect FAIL:', e)
finally:
    s3.close()
