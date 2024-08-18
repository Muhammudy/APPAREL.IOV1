const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const SneaksAPI = require('sneaks-api');
const sneaks = new SneaksAPI();

app.use(bodyParser.json());

// Enable CORS for all routes
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
    next();
});

// Endpoint to get most popular sneakers
app.get('/get-most-popular', (req, res) => {
    sneaks.getMostPopular((err, products) => {
        if (err) {
            console.error(err);
            return res.status(500).send({ error: 'Failed to fetch data from API' });
        } else {
            // Include additional details such as release date, retail price, and image
            const detailedProducts = products.map(product => ({
                shoeName: product.shoeName,
                brand: product.brand,
                styleID: product.styleID,
                description: product.description,
                retailPrice: product.retailPrice,
                releaseDate: product.releaseDate,
                imageUrl: product.thumbnail
            }));
            res.json(detailedProducts);
        }
    });
});

// Placeholder for sales data
const salesData = {};

// Endpoint to record a sale
app.post('/record-sale', (req, res) => {
    const { date, amount } = req.body;

    if (!salesData[date]) {
        salesData[date] = 0;
    }

    salesData[date] += amount;
    res.status(200).send({ message: 'Sale recorded successfully' });
});

// Endpoint to get sales data for a specific day
app.get('/get-daily-sales/:date', (req, res) => {
    const date = req.params.date;
    const sales = salesData[date] || 0;
    res.status(200).send({ date, sales });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
