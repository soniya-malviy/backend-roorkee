const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Replace with the URL you want to scrape
    await page.goto('http://esomsa.hp.gov.in/?q=schemes-3');

    const schemes = await page.evaluate(() => {
        const rows = Array.from(document.querySelectorAll('.table-responsive .table-bordered tbody'));
        const schemesData = [];

        rows.forEach(row => {
            const scheme = {
                name: null,
                objective: null,
                assistance: null,
                eligibility: null,
                process: null,
                contactOfficer: null,
                formDownloadLink: null,
                applyOnlineLink: null
            };

            // Extracting Scheme Name
            const schemeName = row.querySelector('tr:nth-child(1) td').innerText.trim();
            scheme.name = schemeName;

            const dataRows = row.querySelectorAll('tr');

            dataRows.forEach((dataRow) => {
                const keyElement = dataRow.querySelector('td:nth-child(1)');
                const valueElement = dataRow.querySelector('td:nth-child(2)');

                if (keyElement && valueElement) {
                    const key = keyElement.innerText.trim();
                    const value = valueElement.innerText.trim();

                    switch (key) {
                        case 'उद्देश्य':
                            scheme.objective = value;
                            break;
                        case 'सहायता':
                            scheme.assistance = value;
                            break;
                        case 'पात्रता':
                            scheme.eligibility = value;
                            break;
                        case 'प्रक्रिया':
                            scheme.process = value;
                            break;
                        case 'सम्पर्क अधिकारी':
                            scheme.contactOfficer = value;
                            break;
                        case 'डाउनलोड करने योग्य फॉर्म':
                            const formLink = valueElement.querySelector('a');
                            if (formLink) {
                                scheme.formDownloadLink = formLink.href;
                            }
                            break;
                        case 'Apply Online through':
                            const applyOnlineLink = valueElement.querySelector('a');
                            if (applyOnlineLink) {
                                scheme.applyOnlineLink = applyOnlineLink.href;
                            }
                            break;
                        default:
                            break;
                    }
                }
            });

            schemesData.push(scheme);
        });

        return schemesData;
    });

    await browser.close();
    const targetDir = path.join(__dirname, '..','..','scrapedData');
    const filePath = path.join(targetDir, 'himachalPradesh.json');
    fs.writeFileSync(filePath, JSON.stringify(schemes, null, 2), 'utf-8');
    console.log('Data saved to himachalPradesh.json');
})();