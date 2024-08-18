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

// Helper function to create a filter function from a list of keywords
const createFilter = (keywords, include = true) => {
    return product => {
        const name = product.shoeName.toLowerCase();
        return keywords.some(keyword => include ? name.includes(keyword) : !name.includes(keyword));
    };
};

const streetwearKeywords = ['sneaker', 'shoe', 'yeezy', 'jordan', 'nike', 'adidas'];
const sneakerKeywords = ['sneaker', 'shoe', 'yeezy', 'jordan', 'nike', 'adidas'];

app.post('/get-sneaker-data', (req, res) => {
    const { category, info } = req.body;

    sneaks.getProducts(info, 10, function(err, products) {
        if (err) {
            console.error(err);
            res.status(500).send({ error: 'Failed to fetch data from API' });
        } else {
            let filteredProducts;
            if (category === 'streetwear') {
                filteredProducts = products.filter(createFilter(streetwearKeywords, false));
            } else {
                filteredProducts = products.filter(createFilter(sneakerKeywords, true));
            }

            res.json(filteredProducts);
        }
    });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
