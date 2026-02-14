const puppeteer = require('puppeteer');
const fs = require('fs');

const twitterCookies = JSON.parse(fs.readFileSync('/opt/identityprism-bot/cookies.json', 'utf8'));
console.log(`Loaded ${twitterCookies.length} cookies`);

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/usr/bin/chromium-browser',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900 });

  // Set Twitter cookies
  const xCookies = twitterCookies.map(c => ({
    name: c.name, value: String(c.value),
    domain: c.domain || '.x.com', path: c.path || '/',
    httpOnly: c.httpOnly ?? true, secure: c.secure ?? true,
  }));
  await page.setCookie(...xCookies);
  await page.setCookie(...xCookies.map(c => ({...c, domain: '.twitter.com'})));

  // Intercept ALL requests to find the OAuth initiation
  page.on('request', req => {
    const url = req.url();
    if (url.includes('auth') || url.includes('login') || url.includes('oauth') || url.includes('callback')) {
      console.log(`   [REQ] ${req.method()} ${url}`);
    }
  });
  page.on('response', resp => {
    const url = resp.url();
    if (url.includes('auth') || url.includes('login') || url.includes('oauth') || url.includes('callback')) {
      console.log(`   [RESP] ${resp.status()} ${url}`);
      if (resp.status() >= 300 && resp.status() < 400) {
        console.log(`   [REDIRECT] Location: ${resp.headers()['location'] || '?'}`);
      }
    }
  });

  // Go to Colosseum
  console.log('1. Loading Colosseum...');
  await page.goto('https://colosseum.com/agent-hackathon/', { waitUntil: 'networkidle2', timeout: 30000 });

  // Click Sign in
  console.log('2. Clicking Sign in button...');
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      if (b.innerText.trim() === 'Sign in') { b.click(); return true; }
    }
    return false;
  });
  await new Promise(r => setTimeout(r, 1500));

  // Now try to find the actual href/action for "Sign in with X"
  // The button might trigger a fetch/form submission, not navigation
  const signInInfo = await page.evaluate(() => {
    const results = [];
    for (const el of document.querySelectorAll('button, a, form')) {
      const text = (el.innerText || '').trim();
      if (text.includes('Sign in with X') || text.includes('Twitter')) {
        results.push({
          tag: el.tagName,
          text: text.substring(0, 50),
          href: el.href || '',
          action: el.action || '',
          onclick: el.getAttribute('onclick') || '',
          formaction: el.getAttribute('formaction') || '',
          'data-*': Array.from(el.attributes).filter(a => a.name.startsWith('data-')).map(a => `${a.name}=${a.value}`),
          parentForm: el.closest('form')?.action || '',
        });
      }
    }
    // Also check for any forms on the page
    for (const form of document.querySelectorAll('form')) {
      results.push({
        tag: 'FORM',
        action: form.action,
        method: form.method,
        innerHTML: form.innerHTML.substring(0, 200),
      });
    }
    return results;
  });
  console.log('   Sign in elements:', JSON.stringify(signInInfo, null, 2));

  // Try clicking the button and intercepting the form submission
  console.log('3. Clicking Sign in with X and tracking requests...');
  
  // Use page.waitForNavigation or waitForResponse
  const responsePromise = page.waitForResponse(
    resp => resp.url().includes('auth') || resp.url().includes('oauth') || resp.url().includes('twitter'),
    { timeout: 10000 }
  ).catch(() => null);

  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button, a')) {
      if ((b.innerText || '').includes('Sign in with X')) { 
        b.click();
        return true;
      }
    }
    return false;
  });

  const authResp = await responsePromise;
  if (authResp) {
    console.log('   Auth response:', authResp.status(), authResp.url());
    if (authResp.status() >= 300 && authResp.status() < 400) {
      const loc = authResp.headers()['location'];
      console.log('   Redirect to:', loc);
    }
  }

  await new Promise(r => setTimeout(r, 3000));
  console.log('4. Final URL:', page.url());
  await page.screenshot({ path: '/tmp/col4_final.png' });

  // Check all pages
  const pages = await browser.pages();
  for (let i = 0; i < pages.length; i++) {
    console.log(`   Tab ${i}: ${pages[i].url()}`);
  }

  await browser.close();
})();
