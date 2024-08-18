const axios = require('axios');
const cheerio = require('cheerio');

const fetchUpcomingReleases = async () => {
    try {
        const { data } = await axios.get('https://www.goat.com/sneakers/coming-soon');
        const $ = cheerio.load(data);

        let upcomingReleases = [];

        $('div.grid-product-card').each((index, element) => {
            const shoeName = $(element).find('h2.grid-product-card__title').text();
            const releaseDate = $(element).find('div.grid-product-card__release-date').text();
            const brand = $(element).find('div.grid-product-card__brand').text();
            const imageUrl = $(element).find('img.grid-product-card__image').attr('src');

            upcomingReleases.push({
                shoeName: shoeName.trim(),
                releaseDate: releaseDate.trim(),
                brand: brand.trim(),
                imageUrl: imageUrl.trim(),
            });
        });

        return upcomingReleases;
    } catch (error) {
        console.error('Error fetching upcoming releases:', error);
        return [];
    }
};

const express = require('express');
const app = express();
const bodyParser = require('body-parser');

// Enable CORS for all routes
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    next();
});

app.use(bodyParser.json());

app.get('/get-upcoming-releases', async (req, res) => {
    const upcomingReleases = await fetchUpcomingReleases();
    if (upcomingReleases.length > 0) {
        res.json(upcomingReleases);
    } else {
        res.status(404).send('No upcoming releases found');
    }
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
