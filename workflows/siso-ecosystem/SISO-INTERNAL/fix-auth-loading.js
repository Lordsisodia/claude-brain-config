const { chromium } = require('playwright');

(async () => {
  console.log('🔍 Debugging SISO-CORE Authentication Issue\n');
  
  const browser = await chromium.launch({ 
    headless: false,  // Run with UI to see what's happening
    args: ['--no-sandbox']
  });
  
  try {
    const context = await browser.newContext({
      viewport: { width: 1200, height: 800 },
      // Store auth state
      storageState: {
        cookies: [],
        origins: []
      }
    });
    
    const page = await context.newPage();
    
    // Enable console logging
    page.on('console', msg => {
      if (msg.type() === 'error' || msg.type() === 'warning') {
        console.log(`Browser ${msg.type()}:`, msg.text());
      }
    });
    
    // Log network requests
    page.on('request', request => {
      if (request.url().includes('auth') || request.url().includes('supabase')) {
        console.log('→ Request:', request.method(), request.url());
      }
    });
    
    page.on('response', response => {
      if (response.url().includes('auth') || response.url().includes('supabase')) {
        console.log('← Response:', response.status(), response.url());
      }
    });
    
    const baseUrl = 'http://localhost:5174';
    
    console.log('1️⃣ Going to home page...');
    await page.goto(baseUrl, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    
    // Check if redirected to auth
    const currentUrl = page.url();
    console.log('Current URL:', currentUrl);
    
    if (currentUrl.includes('/auth')) {
      console.log('\n2️⃣ On auth page, attempting login...');
      
      // Clear any existing data
      await page.evaluate(() => {
        localStorage.clear();
        sessionStorage.clear();
      });
      
      await page.waitForTimeout(1000);
      
      // Try to login
      await page.fill('input[name="email"], input[type="email"]', 'Fuzeheritage123456789@gmail.com');
      await page.fill('input[name="password"], input[type="password"]', 'Million2025@SISO');
      
      console.log('3️⃣ Submitting login form...');
      await page.click('button:has-text("Sign In")');
      
      // Wait for response
      await page.waitForTimeout(5000);
      
      // Check auth state
      const authState = await page.evaluate(() => {
        const supabaseKey = Object.keys(localStorage).find(key => key.includes('supabase'));
        const session = supabaseKey ? JSON.parse(localStorage.getItem(supabaseKey)) : null;
        return {
          hasSupabaseKey: !!supabaseKey,
          hasSession: !!session?.session,
          currentUrl: window.location.href,
          localStorage: Object.keys(localStorage),
          cookies: document.cookie
        };
      });
      
      console.log('\n📊 Auth State Check:');
      console.log('Has Supabase key:', authState.hasSupabaseKey);
      console.log('Has session:', authState.hasSession);
      console.log('Current URL:', authState.currentUrl);
      console.log('LocalStorage keys:', authState.localStorage);
      
      if (!authState.hasSession) {
        console.log('\n❌ Login failed - checking for errors...');
        
        const errorText = await page.evaluate(() => {
          const errors = document.querySelectorAll('.error, .alert, [role="alert"]');
          return Array.from(errors).map(e => e.textContent).join(' ');
        });
        
        if (errorText) {
          console.log('Error message:', errorText);
        }
      }
    }
    
    console.log('\n4️⃣ Trying to navigate directly to LifeLock...');
    await page.goto(`${baseUrl}/admin/life-lock`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    // Final check
    const finalUrl = page.url();
    const pageContent = await page.evaluate(() => ({
      url: window.location.href,
      hasContent: document.body.innerText.length > 100,
      isLoading: !!document.querySelector('.loading, .spinner, [class*="load"]'),
      bodyPreview: document.body.innerText.substring(0, 200)
    }));
    
    console.log('\n📍 Final State:');
    console.log('URL:', finalUrl);
    console.log('Has content:', pageContent.hasContent);
    console.log('Still loading:', pageContent.isLoading);
    console.log('Content preview:', pageContent.bodyPreview);
    
    console.log('\n💡 Keep this browser open to debug further.');
    console.log('Press Ctrl+C to close when done.');
    
    // Keep browser open
    await new Promise(() => {});
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
  }
})();