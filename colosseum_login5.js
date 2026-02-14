const puppeteer = require('puppeteer');
const fs = require('fs');

const twitterCookies = JSON.parse(fs.readFileSync('/opt/identityprism-bot/cookies.json', 'utf8'));

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/usr/bin/chromium-browser',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900 });

  // Set Twitter cookies on x.com and twitter.com domains
  for (const c of twitterCookies) {
    for (const domain of ['.x.com', '.twitter.com']) {
      await page.setCookie({
        name: c.name, value: String(c.value), domain,
        path: '/', httpOnly: c.httpOnly ?? true, secure: true,
      }).catch(() => {});
    }
  }

  // Log ALL requests
  page.on('request', req => {
    const u = req.url();
    if (!u.includes('.js') && !u.includes('.css') && !u.includes('.png') && !u.includes('.svg') && !u.includes('.woff')) {
      console.log(`[${req.method()}] ${u.substring(0, 150)}`);
    }
  });

  console.log('1. Loading Colosseum claim page (already claimed)...');
  await page.goto('https://colosseum.com/agent-hackathon/claim/' + 'e2da084e-f34d-4278-b97d-f2fb0cf2b56d', 
    { waitUntil: 'networkidle2', timeout: 30000 });

  // Dump full page HTML to find the sign-in form structure
  const fullHtml = await page.content();
  fs.writeFileSync('/tmp/col5_page.html', fullHtml);
  console.log('   Saved page HTML to /tmp/col5_page.html');

  // Find ALL forms and buttons
  const formInfo = await page.evaluate(() => {
    const info = [];
    for (const form of document.querySelectorAll('form')) {
      info.push({
        type: 'form',
        action: form.action,
        method: form.method,
        html: form.outerHTML.substring(0, 500),
      });
    }
    for (const btn of document.querySelectorAll('button')) {
      if (btn.innerText.includes('Sign in')) {
        const form = btn.closest('form');
        info.push({
          type: 'button',
          text: btn.innerText.trim(),
          formAction: btn.formAction || '',
          parentForm: form ? form.action : 'no form',
          parentFormMethod: form ? form.method : '',
          html: btn.outerHTML.substring(0, 300),
        });
      }
    }
    return info;
  });
  console.log('   Forms & Sign-in buttons:', JSON.stringify(formInfo, null, 2));

  // Click "Sign in with X" and wait for navigation
  console.log('2. Clicking Sign in with X...');
  const [response] = await Promise.all([
    page.waitForNavigation({ timeout: 15000 }).catch(e => { console.log('   Nav timeout'); return null; }),
    page.evaluate(() => {
      for (const btn of document.querySelectorAll('button')) {
        if (btn.innerText.includes('Sign in with X')) {
          btn.click();
          return 'clicked';
        }
      }
      // Try submitting the form directly
      for (const form of document.querySelectorAll('form')) {
        if (form.innerHTML.includes('Sign in with X')) {
          form.submit();
          return 'form submitted';
        }
      }
      return 'not found';
    }),
  ]);

  console.log('   Navigation response:', response?.url?.() || 'none');
  console.log('   Current URL:', page.url());
  await page.screenshot({ path: '/tmp/col5_after_click.png' });

  // If on Twitter OAuth page, authorize
  if (page.url().includes('twitter.com') || page.url().includes('x.com')) {
    console.log('3. On Twitter OAuth page!');
    const oauthBody = await page.evaluate(() => document.body.innerText.substring(0, 500));
    console.log('   Body:', oauthBody.substring(0, 300));
    await page.screenshot({ path: '/tmp/col5_oauth.png' });
    
    // Click authorize/allow
    await page.evaluate(() => {
      for (const btn of document.querySelectorAll('button, input[type="submit"]')) {
        const txt = (btn.innerText || btn.value || '').toLowerCase();
        if (txt.includes('authorize') || txt.includes('allow') || txt.includes('confirm')) {
          btn.click(); return;
        }
      }
    });
    await page.waitForNavigation({ timeout: 15000 }).catch(() => {});
    console.log('   After auth URL:', page.url());
  }

  await page.screenshot({ path: '/tmp/col5_final.png' });
  await browser.close();
})();
