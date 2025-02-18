const puppeteer = require('puppeteer');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const path = require('path');

// Function to fetch scholarship links and titles
async function getScholarshipLinks() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('https://megeducation.gov.in/dhte/pages/scholarship_schemes.html', {
        waitUntil: 'domcontentloaded',
        timeout: 60000
    });
    
    const scholarships = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('.body_ol li a')).map(e => ({
            title: e.textContent.trim(),
            link: e.href
        }));
    });

    await browser.close();
    return scholarships;
}

// Function to fetch scholarship details
async function getScholarshipDetails(scholarships) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const allData = [];

    for (let scholarship of scholarships) {
        try {
            await page.goto(scholarship.link, { waitUntil: 'domcontentloaded', timeout: 60000 });
            const details = await page.evaluate(() => {
                const getText = (selector) => {
                    const elem = document.querySelector(selector);
                    return elem ? elem.textContent.trim() : 'Not available';
                };
                return {
                    description: document.querySelector('h4:nth-of-type(2) + p')?.textContent.trim() || '' + document.querySelector('h4:nth-of-type(2) + p')?.textContent.trim() || '' + document.querySelector('h4:nth-of-type(3) + p')?.textContent.trim() || '' + document.querySelector('p:nth-of-type(2) ')?.textContent.trim() || '',
                    eligibility: Array.from(document.querySelectorAll('h4:nth-of-type(1) + ol li'))
                        .map(li => li.textContent.trim())
                        .join(' ')+Array.from(document.querySelectorAll('h4:nth-of-type(2) + p'))
                        .map(li => li.textContent.trim())
                        .join(' ')
                };
                
            });
            allData.push({
                id: uuidv4(),
                title: scholarship.title,
                link: scholarship.link,
                description: details.description,
                eligibility: details.eligibility
            });
        } catch (error) {
            console.error(`Error scraping ${scholarship.title}:`, error.message);
        }
    }

    await browser.close();
    return allData;
}

// Function to fetch scheme details
async function getSchemes() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    let schemesArray = [];

    for (let pageNumber = 0; pageNumber < 6; pageNumber++) {
        await page.goto(`https://meghalaya.gov.in/index.php/schemes?page=${pageNumber}`);
        let schemeNames = await page.evaluate(() =>
            Array.from(document.querySelectorAll('.view-content .item-list ul li span span a'), e => e.textContent)
        );
        schemesArray = schemesArray.concat(schemeNames);
    }
    await browser.close();
    return schemesArray;
}

async function getUrls() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    let urlsArray = [];

    for (let pageNumber = 0; pageNumber < 6; pageNumber++) {
        await page.goto(`https://meghalaya.gov.in/index.php/schemes?page=${pageNumber}`);
        let schemeUrls = await page.evaluate(() =>
            Array.from(document.querySelectorAll('.view-content .item-list ul li span span a'), e => e.href)
        );
        urlsArray = urlsArray.concat(schemeUrls);
    }
    await browser.close();
    return urlsArray;
}

async function getSchemesDetail(urlsArray) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    let allData = [];

    for (let url of urlsArray) {
        await page.goto(url);
        const keys = await page.evaluate(() =>
            Array.from(document.querySelectorAll('.views-row .views-field span:first-child'), e => e.textContent)
        );
        const values = await page.evaluate(() =>
            Array.from(document.querySelectorAll('.views-row .views-field'), field => {
                const secondElement = field.querySelector(':scope > :nth-child(2)');
                return secondElement ? secondElement.textContent : null;
            }).filter(text => text != null)
        );
        keys.pop(); keys.pop();
        slicedKeys = keys.slice(-values.length + 1);
        while (slicedKeys[0] !== 'Department: ') slicedKeys.shift();
        let data = { 'ID: ': uuidv4() };
        slicedKeys.forEach((key, index) => { data[key] = values[index]; });
        data['Scheme Link: '] = url;
        allData.push(data);
    }
    await browser.close();
    return allData;
}

// Main function
async function main() {
    console.log('Fetching scholarship details...');
    const scholarships = await getScholarshipLinks();
    const scholarshipDetails = await getScholarshipDetails(scholarships);
    
    console.log('Fetching scheme details...');
    const urlsArray = await getUrls();
    const schemesDetails = await getSchemesDetail(urlsArray);
    
    const allData = { scholarships: scholarshipDetails, schemes: schemesDetails };
    const filePath = path.join(__dirname, '..', '..','scrapedData', 'meghalaya.json');
    fs.writeFileSync(filePath, JSON.stringify(allData, null, 2));
    
    console.log('Data has been scraped and saved to meghalaya.json');
}

main();
