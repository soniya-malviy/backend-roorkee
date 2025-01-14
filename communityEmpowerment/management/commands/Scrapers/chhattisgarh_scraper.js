const puppeteer = require('puppeteer')
const { v4: uuidv4 } = require('uuid');
const fs = require('fs')

async function scrapeChhattisgarhProgramUrls(){
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    await page.goto('https://sw.cg.gov.in/en', { timeout: 120000 })
    const result = await page.evaluate(()=>{
        const urlNodes = document.querySelectorAll('.menu li')
        const urlList = []
        urlNodes.forEach((url)=>{
            const extractedUrl = url.querySelector('a').href
            urlList.push(extractedUrl)
        })
        return urlList
    })
    await browser.close()
    console.log(result)
    return result
    
}

async function scrapeChhattisgarhSchemeUrlsEnglish(){
    const programUrls = await scrapeChhattisgarhProgramUrls()
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    const programSchemeUrlsEnglish = []
    for (const programUrl of programUrls){
        await page.goto(programUrl, { timeout: 120000 })
        const result = await page.evaluate(()=>{
            const schemeUrlsEnglish = []
            const schemeUrlNodes = document.querySelectorAll('.field-item ul li')
            schemeUrlNodes.forEach((url)=>{
                const extractedUrl = url.querySelector('a').href
                schemeUrlsEnglish.push(extractedUrl)
            })
            return schemeUrlsEnglish
        })
        console.log("ye haiiii: ", result)
        programSchemeUrlsEnglish.push(result)

    }
    await browser.close()
    return programSchemeUrlsEnglish
}

async function scrapeChhattisgarhSchemeDetails(){
    const schemeUrlList = await scrapeChhattisgarhSchemeUrlsEnglish()
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    const schemeList = []
    for (const schemeUrls of schemeUrlList){
        for (const schemeUrl of schemeUrls){
        if (schemeUrl){
            console.log(schemeUrl)
        await page.goto(schemeUrl,{ timeout: 120000 })
        const result = await page.evaluate((schemeUrl) => {
            // Safely get the textContent of the title node
            // const title = document.querySelector('.h1classhindi')?.textContent || 'No title available';
            const splittedTitle = schemeUrl.split('/')
            const title = splittedTitle.at(-1).replace(/-/g," ").replace(/\b\w/g, char => char.toUpperCase());
        
            // Safely get the textContent of the description node
            const description = document.querySelector('.rteindent1')?.textContent || 'No description available';
        
            // Safely collect criteria data
            const criteria = [];
            const criteriaNode = document.querySelectorAll('.lstnum li');
            criteriaNode?.forEach((criteriaElement) => {
                const criteriaData = criteriaElement?.textContent || 'No criteria data';
                criteria.push(criteriaData);
            });
        
            // Safely get the textContent of benefits and procedure
            const benefits = document.querySelector('.field-item :nth-child(6) li')?.textContent || 'No benefits data available';
            const procedure = document.querySelector('.field-item :nth-child(8) li')?.textContent || 'No procedure data available';
        
            // Create the scheme object

            const scheme = {
                title: title,
                description: description,
                criteria: criteria,
                benefits: benefits,
                procedure: procedure,
                schemeUrl: schemeUrl
            };
        
            return scheme;
        },schemeUrl);
        const generateUUID = () => uuidv4();
        const schemeData = {
            id: generateUUID(),
            ...result
        }
        console.log("ye hai single scheme: ", schemeData)
        schemeList.push(schemeData)
    }
    
    }}
    await browser.close()
    console.log("Ye hai schemeList: ",schemeList)
    const targetDir = path.join(__dirname, '..','..','scrapedData');
    const filePath = path.join(targetDir, 'chhattisgarh.json');
    fs.writeFileSync(filePath, JSON.stringify(schemeList, null, 2), 'utf-8');

    console.log('Data has been saved to chhatisgarhSchemes.json');
}

scrapeChhattisgarhSchemeDetails()
