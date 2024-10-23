const puppeteer = require('puppeteer');
const fs = require('fs');

async function main() {
    const browser = await puppeteer.launch({
        headless: false
    });
    const page = await browser.newPage();

    await page.goto('https://famdev.ro');

    await page.evaluate(() => {
        const form = document.querySelector('#contactForm');
        form.scrollIntoView({ behavior: 'smooth' });
    });

    await new Promise(resolve => setTimeout(resolve, 1000));
    await page.type('#name', 'Nume');

    await new Promise(resolve => setTimeout(resolve, 1000));
    await page.type('#email', 'email@example.com');

    await new Promise(resolve => setTimeout(resolve, 1000));
    await page.type('#message', 'Mesaj');

    await new Promise(resolve => setTimeout(resolve, 1000));
    // TODO: call api for solving captcha 
    await page.type('#captcha', '1234');

    const imageBase64 = await page.evaluate(() => {
        const captchaElement = document.querySelector('#captchaImg');
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = captchaElement.width;
        canvas.height = captchaElement.height;
        ctx.drawImage(captchaElement, 0, 0);
        return canvas.toDataURL('image/png').split(',')[1];
    });

    if (imageBase64) {
        const buffer = Buffer.from(imageBase64, 'base64');
        fs.writeFileSync('captcha-image.png', buffer);
        console.log('Image saved as captcha-image.png');
    } else {
        console.log('Image not found or failed to extract.');
    }

    await new Promise(resolve => setTimeout(resolve, 200000));
    await page.click('#submitBtn');

    await page.waitForSelector('#succesMsg', { visible: true });

    console.log(await page.$eval('#succesMsg', el => el.textContent));

    await browser.close();
}

main();



