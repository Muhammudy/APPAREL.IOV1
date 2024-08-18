const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const SneaksAPI = require('sneaks-api');
const sneaks = new SneaksAPI();

// Enable CORS for all routes
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
    next();
});

app.use(bodyParser.json());

app.post('/get-sneaker-data', (req, res) => {
    const { category, info } = req.body;

    sneaks.getProducts(info, 10, function(err, products) {
        if (err) {
            console.error(err);
            return res.status(500).send({ error: 'Failed to fetch data from API' });
        } else {
            if (category.toLowerCase() === 'streetwear') {
                products = products.filter(product => {
                    const name = product.shoeName.toLowerCase();
                    return !name.includes('jordan') && !name.includes('supreme') && (
                        name.includes('fear of god') ||
                        name.includes('bape') ||
                        name.includes('hoodie') ||
                        name.includes('t-shirt') ||
                        name.includes('hell') ||
                        name.includes('denim') ||
                        name.includes('tears') ||
                        name.includes('fleece')
                    );
                });
            } else if (category.toLowerCase() === 'sneakers') {
                products = products.filter(product => {
                    const name = product.shoeName.toLowerCase();
                    return !(
                        name.includes('fear of god') ||
                        name.includes('bape') ||
                        name.includes('hoodie') ||
                        name.includes('t-shirt') ||
                        name.includes('fleece')
                    ) && (
                        name.includes('sneaker') ||
                        name.includes('shoe') ||
                        name.includes('yeezy') ||
                        name.includes('jordan') ||
                        name.includes('nike') ||
                        name.includes('adidas') ||
                        name.includes('supreme')
                    );
                });
            }
            
            const result = products.map(product => ({
                shoeName: product.shoeName,
                brand: product.brand,
                styleID: product.styleID,
                description: product.description,
                imageUrl: product.thumbnail,
            }));

            res.json(result);
        }
    });
});

app.post('/get-upcoming-releases', (req, res) => {
    const { daysAhead } = req.body;

    sneaks.getUpcomingReleases(function(err, products) {
        if (err) {
            console.error(err);
            return res.status(500).send({ error: 'Failed to fetch data from API' });
        } else {
            const result = products.map(product => ({
                shoeName: product.shoeName,
                brand: product.brand,
                releaseDate: product.releaseDate,
                imageUrl: product.thumbnail,
            }));
            res.json(result);
        }
    });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
