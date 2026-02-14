"""Post a one-time announcement tweet about the Reputation API launch."""
import os, sys, time, random
from dotenv import load_dotenv
load_dotenv()

from twitterapi_io_client import TwitterApiIoClient
from config import (
    TWITTERAPI_IO_API_KEY, TWITTERAPI_IO_PROXIES,
    TWITTERAPI_IO_USERNAME, TWITTERAPI_IO_EMAIL,
    TWITTERAPI_IO_PASSWORD, TWITTERAPI_IO_TOTP_SECRET,
)

client = TwitterApiIoClient(
    api_key=TWITTERAPI_IO_API_KEY,
    proxies=TWITTERAPI_IO_PROXIES,
    username=TWITTERAPI_IO_USERNAME,
    email=TWITTERAPI_IO_EMAIL,
    password=TWITTERAPI_IO_PASSWORD,
    totp_secret=TWITTERAPI_IO_TOTP_SECRET,
)

tweet_text = """We just shipped the Identity Prism Reputation API.

Any Solana wallet. Instant reputation score, tier & badges.

Try it now:
https://identityprism.xyz/api/reputation?address=YOUR_WALLET

What's inside:
- Score 0-1400 based on on-chain activity
- Celestial tiers: Mercury to Sun
- Badges: OG, Whale, Collector, Titan & more
- Compare wallets, batch queries
- Free & open for any dApp to integrate

Your wallet tells a story. We just made it readable.

#Solana #OnChainIdentity #ReputationAPI #IdentityPrism"""

print(f"Posting tweet ({len(tweet_text)} chars)...")
try:
    result = client.create_tweet(tweet_text)
    print(f"Success! Tweet ID: {result}")
except Exception as e:
    print(f"Failed: {e}")
    sys.exit(1)
