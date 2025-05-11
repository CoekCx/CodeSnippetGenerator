const express = require('express');
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs').promises;

const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(express.json({ limit: '10mb' }));

const OUTPUT_DIR = '/output';

async function ensureOutputDir() {
    try {
        await fs.mkdir(OUTPUT_DIR, { recursive: true });
        console.log(`Output directory ensured: ${OUTPUT_DIR}`);
    } catch (err) {
        console.error('Failed to create output directory:', err);
    }
}

app.post('/convert', async (req, res) => {
    console.log('Received convert request');
    const { html, destPath, filename } = req.body;

    if (!html || !destPath || !filename) {
        console.error('Missing required fields:', { html: !!html, destPath: !!destPath, filename: !!filename });
        return res.status(400).json({ error: 'Missing required fields: html, destPath, filename' });
    }

    
    const safeDestPath = path.normalize(destPath).replace(/^(\.\.[\/\\])+/, '').replace(/\\/g, '/');
    const fullDirPath = path.join(OUTPUT_DIR, safeDestPath);
    const fullFilePath = path.join(fullDirPath, filename);
    
    console.log('Paths generated:', {
        safeDestPath,
        fullDirPath,
        fullFilePath
    });

    if (!/^[a-zA-Z0-9_\- ]+\.(png|jpg|jpeg)$/.test(filename)) {
        console.error('Invalid filename:', filename);
        return res.status(400).json({ error: 'Invalid filename. Use alphanumeric characters, spaces, _, -, and .png/.jpg/.jpeg extension' });
    }

    try {
        console.log('Creating directory:', fullDirPath);
        await fs.mkdir(fullDirPath, { recursive: true });

        console.log('Launching browser...');
        const browser = await puppeteer.launch({
            headless: "new",
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        console.log('Browser launched successfully');

        const page = await browser.newPage();
        console.log('New page created');

        // Set viewport to a large size initially with higher DPR for better quality
        await page.setViewport({
            width: 2048,
            height: 1536,
            deviceScaleFactor: 2, // Increase for better quality
        });
        console.log('Viewport set');

        console.log('Setting page content...');
        await page.setContent(html, { waitUntil: 'networkidle0' });
        
        // Wait for any fonts to load
        await page.evaluateHandle('document.fonts.ready');
        
        // Get the exact dimensions of the code container
        console.log('Looking for code container element...');
        const element = await page.$('.code-container');
        if (!element) {
            throw new Error('Could not find code container element');
        }
        console.log('Code container element found');

        // Get the bounding box of the element
        console.log('Getting element dimensions...');
        const boundingBox = await element.boundingBox();
        if (!boundingBox) {
            throw new Error('Could not get element dimensions');
        }
        console.log('Element dimensions:', boundingBox);

        // Add padding and ensure we capture the full element
        const padding = 4; // Increased padding
        const screenshotOptions = {
            path: fullFilePath,
            clip: {
                x: Math.max(0, boundingBox.x - padding),
                y: Math.max(0, boundingBox.y - padding),
                width: boundingBox.width + (padding * 2),
                height: boundingBox.height + (padding * 2)
            },
            omitBackground: true // Make background transparent
        };

        // Wait a bit for everything to settle
        await page.waitForTimeout(100);

        console.log('Taking screenshot...');
        await page.screenshot(screenshotOptions);
        console.log('Screenshot taken');

        console.log('Closing browser...');
        await browser.close();
        console.log('Browser closed');

        // Verify if file exists
        try {
            const stats = await fs.stat(fullFilePath);
            console.log('File saved successfully:', {
                path: fullFilePath,
                size: stats.size + ' bytes'
            });
        } catch (statErr) {
            console.error('File not found after save attempt:', statErr);
            throw new Error('File was not saved successfully');
        }

        res.json({ message: 'Image saved successfully', path: fullFilePath });
    } catch (err) {
        console.error('Conversion error:', err);
        console.error('Error stack:', err.stack);
        res.status(500).json({ error: 'Failed to convert HTML to image', details: err.message });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
    ensureOutputDir();
});