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
            res.status(500).send({ error: 'Failed to fetch data from API' });
        } else {

            res.json(products);
        }
    });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
