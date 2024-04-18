import { createRequire } from 'module';
const require = createRequire(import.meta.url);

const PDFDocument = require('pdfjs-dist');
const fs = require('fs');

const pdfPath1 = './pdfs/LeadSafeCertification.pdf';

// function to get the questions from the pdf
async function extractQuestions(pdf) {
    // array for the extracted questions to be mapped
    const questions = [];
    for (let i=1; i <= pdf.numPages; i++) {
        //grab page then text 
        const page = await pdf.getPage(i + 1);
        const text = await page.getTextContent();
        const pageText = text.items.map( item => item.str).join(' ');

        // grabs questions from pdf by matching with certain expression and maps into main array
        const regex = /Questions: (.+?)(?=(?:Questions:|$))/g;
        let match;
        while ((match = regex.exec(pageText)) !== null) {
            questions.push(match[1]);
        }
    }
    // exec prompt utilizing the finished array
    promptQuestions(questions);
}

// function for prompting
function promptQuestions(questions) {
    console.log("Answer the following questions: ");

    questions.forEach((question, index) => {
        const answer = prompt(`Question ${ index + 1 }: ${question}`);
        console.log(`Answer received: ${ answer } for ${ index + 1 }`);
    });
}

fs.readFile(pdfPath1, async (err, data) => {
    
    // reading PDF
    if (err) {
        console.error('Error reading PDF: ', err)
        return;
    }

    // parsing PDF
    try {
        const pdfDoc = await PDFDocument.load(data);
        await extractQuestions(pdfDoc)
    } catch (error) {
        console.error('ERROR PARSING PDF: ', error);
    }
})
