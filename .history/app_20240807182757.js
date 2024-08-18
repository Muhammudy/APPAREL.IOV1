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
            // Include release date, retail price, and image URL in the response
            const result = products.map(product => ({
                shoeName: product.shoeName,
                brand: product.brand,
                styleID: product.styleID,
                description: product.description,
                imageUrl: product.thumbnail,  // Assuming 'thumbnail' is the key for the image URL
                releaseDate: product.releaseDate,
                retailPrice: product.retailPrice,
                img: product.imageLinks[0]  // Assuming 'imageLinks' contains the image URLs
            }));
            res.json(result);
        }
    });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
