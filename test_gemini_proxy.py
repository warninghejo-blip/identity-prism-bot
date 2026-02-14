import os
os.chdir('/opt/identityprism-bot')
from dotenv import load_dotenv
load_dotenv()
proxy = os.getenv('GEMINI_PROXY', '')
print('GEMINI_PROXY:', repr(proxy))
if proxy:
    os.environ['HTTPS_PROXY'] = proxy
    os.environ['HTTP_PROXY'] = proxy
from google import genai
c = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
r = c.models.generate_content(model='gemini-2.5-flash', contents='Say hi in 5 words')
print('OK:', r.text)
