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
            if (category === 'streetwear') {
                // Filtering for streetwear category
                products = products.filter(product => {
                    // Exclude products that contain any of these keywords in their shoeName
                    return !product.shoeName.toLowerCase().includes('sneaker') && // Excludes "sneaker" from names like "Nike Sneaker"
                           !product.shoeName.toLowerCase().includes('shoe') &&    // Excludes "shoe" from names like "Running Shoe"
                           !product.shoeName.toLowerCase().includes('yeezy') &&   // Excludes "yeezy" from names like "Adidas Yeezy"
                           !product.shoeName.toLowerCase().includes('nike') &&    // Excludes "nike" from names like "Nike Air Max"
                           !product.shoeName.toLowerCase().includes('adidas');    // Excludes "adidas" from names like "Adidas Superstar"
                });
            } else {
                // Filtering for sneaker category
                products = products.filter(product => {
                    // Include only products that contain any of these keywords in their shoeName
                    return product.shoeName.toLowerCase().includes('sneaker') || // Includes "sneaker" from names like "Nike Sneaker"
                           product.shoeName.toLowerCase().includes('shoe') ||    // Includes "shoe" from names like "Running Shoe"
                           product.shoeName.toLowerCase().includes('yeezy') ||   // Includes "yeezy" from names like "Adidas Yeezy"
                           product.shoeName.toLowerCase().includes('jordan') ||  // Includes "jordan" from names like "Air Jordan"
                           product.shoeName.toLowerCase().includes('nike') ||    // Includes "nike" from names like "Nike Air Max"
                           product.shoeName.toLowerCase().includes('adidas');    // Includes "adidas" from names like "Adidas Superstar"
                });
            }
            
            }
            res.json(products);
        }
    });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
