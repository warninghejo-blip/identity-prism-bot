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

  for (const c of twitterCookies) {
    for (const domain of ['.x.com', '.twitter.com']) {
      await page.setCookie({
        name: c.name, value: String(c.value), domain,
        path: '/', httpOnly: c.httpOnly ?? true, secure: true,
      }).catch(() => {});
    }
  }

  // Track new tabs
  browser.on('targetcreated', async target => {
    console.log('NEW TARGET:', target.type(), target.url());
  });

  console.log('1. Loading claim page...');
  await page.goto('https://colosseum.com/agent-hackathon/claim/e2da084e-f34d-4278-b97d-f2fb0cf2b56d',
    { waitUntil: 'networkidle2', timeout: 30000 });

  // Use Puppeteer's native click on Sign in button (proper DOM events for Svelte)
  console.log('2. Native-clicking Sign in...');
  const signInBtn = await page.waitForSelector('[data-testid="sign-in-button"]', { timeout: 5000 });
  await signInBtn.click();
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: '/tmp/col6_02.png' });

  // Find "Sign in with X" using XPath text match and native-click it
  console.log('3. Finding and native-clicking Sign in with X...');
  
  // Wait for the button to appear after dropdown opens
  await new Promise(r => setTimeout(r, 1000));
  
  // Use XPath to find button containing "Sign in with X"
  const buttons = await page.$$('button');
  let signInWithX = null;
  for (const btn of buttons) {
    const text = await page.evaluate(el => el.innerText?.trim(), btn);
    if (text && text.includes('Sign in with X')) {
      signInWithX = btn;
      console.log('   Found button:', text);
      break;
    }
  }

  if (signInWithX) {
    // Use Promise.all to catch both popup and same-page navigation
    const [newPage] = await Promise.all([
      new Promise(resolve => {
        const handler = async (target) => {
          if (target.type() === 'page') {
            browser.off('targetcreated', handler);
            resolve(await target.page());
          }
        };
        browser.on('targetcreated', handler);
        setTimeout(() => { browser.off('targetcreated', handler); resolve(null); }, 10000);
      }),
      page.waitForNavigation({ timeout: 10000 }).catch(() => null),
      signInWithX.click(), // Puppeteer native click - triggers Svelte handlers
    ]);

    await new Promise(r => setTimeout(r, 3000));
    
    // Check all tabs
    const allPages = await browser.pages();
    console.log(`   ${allPages.length} tabs:`);
    for (let i = 0; i < allPages.length; i++) {
      console.log(`   [${i}] ${allPages[i].url()}`);
    }

    // Find the OAuth or callback page
    let authPage = null;
    for (const p of allPages) {
      const url = p.url();
      if (url.includes('twitter.com') || url.includes('x.com')) {
        authPage = p;
        break;
      }
    }

    // Also check main page
    const mainUrl = page.url();
    console.log('   Main page URL:', mainUrl);

    if (authPage) {
      console.log('4. Found Twitter OAuth page!');
      await authPage.screenshot({ path: '/tmp/col6_oauth.png' });
      const body = await authPage.evaluate(() => document.body.innerText.substring(0, 500));
      console.log('   Body:', body.substring(0, 300));

      // Find and click authorize
      const authBtns = await authPage.$$('button, input[type="submit"]');
      for (const btn of authBtns) {
        const txt = await authPage.evaluate(el => (el.innerText || el.value || '').toLowerCase(), btn);
        if (txt.includes('authorize') || txt.includes('allow') || txt.includes('confirm') || txt.includes('sign in')) {
          console.log('   Clicking auth button:', txt.substring(0, 50));
          await Promise.all([
            authPage.waitForNavigation({ timeout: 15000 }).catch(() => null),
            btn.click(),
          ]);
          break;
        }
      }
      await new Promise(r => setTimeout(r, 3000));
      
      // Check where we ended up
      const finalPages = await browser.pages();
      for (const p of finalPages) {
        if (p.url().includes('colosseum')) {
          console.log('5. Back on Colosseum:', p.url());
          await p.screenshot({ path: '/tmp/col6_loggedin.png' });
          // Check if logged in
          const loggedInBody = await p.evaluate(() => document.body.innerText.substring(0, 500));
          console.log('   Body:', loggedInBody.substring(0, 300));
        }
      }
    } else if (mainUrl.includes('colosseum') && !mainUrl.includes('claim')) {
      console.log('4. Redirected on Colosseum:', mainUrl);
      await page.screenshot({ path: '/tmp/col6_redirect.png' });
    } else {
      console.log('4. No OAuth redirect happened');
      await page.screenshot({ path: '/tmp/col6_noredirect.png' });
    }
  } else {
    console.log('   Sign in with X button not found!');
  }

  await browser.close();
})();
