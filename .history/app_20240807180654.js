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

// Endpoint to get most popular sneakers
app.get('/get-most-popular', (req, res) => {
    sneaks.getMostPopular(20, (err, products) => {
        if (err) {
            console.error(err);
            return res.status(500).send({ error: 'Failed to fetch data from API' });
        } else {
            res.json(products);
        }
    });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
