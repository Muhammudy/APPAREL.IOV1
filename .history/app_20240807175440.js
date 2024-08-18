const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const app = express();
const bodyParser = require('body-parser');

// Enable CORS for all routes
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
    next();
});

app.use(bodyParser.json());

// Scrape upcoming releases from GOAT
app.post('/get-upcoming-releases', async (req, res) => {
    try {
        const response = await axios.get('https://www.goat.com/sneakers');
        const html = response.data;
        const $ = cheerio.load(html);

        const upcomingReleases = [];
        $('.product-card').each((index, element) => {
            const shoeName = $(element).find('.product-card__title').text().trim();
            const brand = $(element).find('.product-card__brand').text().trim();
            const releaseDate = $(element).find('.product-card__release-date').text().trim();
            const imageUrl = $(element).find('img').attr('src');
            
            if (shoeName && brand && releaseDate && imageUrl) {
                upcomingReleases.push({ shoeName, brand, releaseDate, imageUrl });
            }
        });

        res.json(upcomingReleases);
    } catch (error) {
        console.error('Error fetching upcoming releases from GOAT:', error);
        res.status(500).send({ error: 'Failed to fetch data from GOAT' });
    }
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
