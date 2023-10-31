const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto('https://docs.prismacloud.io/en/enterprise-edition/use-cases/secure-the-infrastructure/tailor-prisma-cloud-to-match-your-security-needs');

  // You may need to wait for specific elements to load
  await page.waitForSelector('body > main > div > div.article-wrapper > div > article > div.content.hidden-not-found.contain > div > div > div > div > div');

  // Save the page as HTML
  const htmlContent = await page.content();

  // Write the HTML content to a file
  const fs = require('fs');
  fs.writeFileSync('webpage.html', htmlContent, 'utf8');

  await browser.close();
})();

