import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function captureLifeLockPage() {
  let browser;
  try {
    console.log('🚀 Starting browser for LifeLock capture...');
    
    browser = await puppeteer.launch({
      headless: true, // Headless for faster execution
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--use-fake-ui-for-media-stream',
        '--use-fake-device-for-media-stream',
        '--allow-running-insecure-content',
        '--disable-web-security',
        '--disable-dev-shm-usage'
      ]
    });

    const page = await browser.newPage();

    // Emulate iPhone 14 Pro
    await page.emulate({
      name: 'iPhone 14 Pro',
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
      viewport: {
        width: 393,
        height: 852,
        deviceScaleFactor: 3,
        isMobile: true,
        hasTouch: true,
        isLandscape: false,
      },
    });

    // Grant microphone permissions
    const context = browser.defaultBrowserContext();
    await context.overridePermissions('http://localhost:5173', ['microphone']);

    console.log('🌐 Navigating to localhost...');
    await page.goto('http://localhost:5173', { 
      waitUntil: 'networkidle0',
      timeout: 15000 
    });

    // Take initial screenshot
    const initialPath = path.join(__dirname, 'screenshots', 'lifelock-initial-mobile.png');
    await page.screenshot({
      path: initialPath,
      fullPage: true
    });
    console.log('📸 Initial screenshot saved to:', initialPath);

    // Try to bypass auth by directly navigating to the admin page
    console.log('🔑 Attempting to access admin page directly...');
    try {
      await page.goto('http://localhost:5173/admin/life-lock', { 
        waitUntil: 'networkidle0',
        timeout: 10000 
      });

      const directAccessPath = path.join(__dirname, 'screenshots', 'lifelock-direct-access.png');
      await page.screenshot({
        path: directAccessPath,
        fullPage: true
      });
      console.log('📸 Direct access screenshot saved to:', directAccessPath);
    } catch (error) {
      console.log('⚠️ Direct access failed, trying other approaches...');
    }

    // Try to find and interact with any visible microphone elements
    console.log('🎤 Searching for microphone elements...');
    
    // Look for microphone-related elements
    const micElements = await page.evaluate(() => {
      const elements = document.querySelectorAll('*[class*="microphone"], *[class*="mic"], *[data-testid*="mic"], svg[class*="mic"]');
      return Array.from(elements).map(el => ({
        tagName: el.tagName,
        className: el.className,
        textContent: el.textContent?.substring(0, 50),
        visible: el.offsetWidth > 0 && el.offsetHeight > 0,
        position: {
          x: el.getBoundingClientRect().x,
          y: el.getBoundingClientRect().y,
          width: el.getBoundingClientRect().width,
          height: el.getBoundingClientRect().height
        }
      }));
    });

    // Look for FAB buttons
    const fabElements = await page.evaluate(() => {
      const elements = document.querySelectorAll('*[class*="fixed"], *[class*="fab"], *[class*="floating"]');
      return Array.from(elements).map(el => ({
        tagName: el.tagName,
        className: el.className,
        textContent: el.textContent?.substring(0, 50),
        visible: el.offsetWidth > 0 && el.offsetHeight > 0,
        position: {
          x: el.getBoundingClientRect().x,
          y: el.getBoundingClientRect().y,
          width: el.getBoundingClientRect().width,
          height: el.getBoundingClientRect().height
        }
      }));
    });

    console.log('🎤 Microphone elements found:', micElements);
    console.log('🎯 FAB elements found:', fabElements);

    // Take final screenshot
    const finalPath = path.join(__dirname, 'screenshots', 'lifelock-final-analysis.png');
    await page.screenshot({
      path: finalPath,
      fullPage: true
    });
    console.log('📸 Final screenshot saved to:', finalPath);

    return {
      screenshots: [initialPath, finalPath],
      micElements,
      fabElements,
      success: true
    };

  } catch (error) {
    console.error('❌ Error during capture:', error);
    return {
      error: error.message,
      success: false
    };
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// Run the capture
captureLifeLockPage()
  .then(result => {
    console.log('🎉 LifeLock capture completed!');
    if (result.success) {
      console.log('📸 Screenshots:', result.screenshots);
      console.log('🎤 Microphone elements:', result.micElements?.length || 0);
      console.log('🎯 FAB elements:', result.fabElements?.length || 0);
    } else {
      console.log('❌ Error:', result.error);
    }
  })
  .catch(error => {
    console.error('💥 Capture failed:', error);
  });