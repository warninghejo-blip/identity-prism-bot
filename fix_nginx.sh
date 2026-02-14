#!/bin/bash
# Remove broken reputation location block and re-add it properly
sed -i '/location \/api\/reputation/,/^    }/d' /etc/nginx/sites-enabled/identityprism

# Insert proper block before /api/market
sed -i '/location \/api\/market {/i\
    location /api/reputation {\
        proxy_pass http://127.0.0.1:8787;\
        proxy_set_header Host $host;\
        proxy_set_header X-Forwarded-Proto $scheme;\
        proxy_set_header X-Forwarded-Host $host;\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\
    }\
' /etc/nginx/sites-enabled/identityprism

nginx -t && systemctl reload nginx && echo "OK" || echo "FAIL"
