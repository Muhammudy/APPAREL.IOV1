const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const SneaksAPI = require('sneaks-api');
const sneaks = new SneaksAPI();

// Middleware to handle CORS for all routes
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
    next();
});

app.use(bodyParser.json());

// Endpoint to get sneaker data based on category and search info
app.post('/get-sneaker-data', (req, res) => {
    const { category, info } = req.body;

    sneaks.getProducts(info, 10, function(err, products) {
        if (err) {
            console.error(err);
            return res.status(500).send({ error: 'Failed to fetch data from API' });
        }

        let filteredProducts = products;

        if (category.toLowerCase() === 'streetwear') {
            filteredProducts = products.filter(product => {
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
            filteredProducts = products.filter(product => {
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

        // Return the filtered products with necessary details
        const result = filteredProducts.map(product => ({
            shoeName: product.shoeName,
            brand: product.brand,
            styleID: product.styleID,
            description: product.description,
            imageUrl: product.thumbnail,  // Assuming 'thumbnail' is the key for the image URL
        }));

        res.json(result);
    });
});

// Endpoint to get the most popular sneakers
app.get('/get-most-popular', (req, res) => {
    sneaks.getMostPopular(20, (err, products) => {
        if (err) {
            console.error(err);
            return res.status(500).send({ error: 'Failed to fetch data from API' });
        }

        // Return the most popular products with additional details
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
    });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
