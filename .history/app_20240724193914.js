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
                // streetwear
                products = products.filter(product => {
                    return product.shoeName.toLowerCase().includes('fear of god') ||
                           product.shoeName.toLowerCase().includes('bape') ||
                           product.shoeName.toLowerCase().includes('supreme') ||
                           product.shoeName.toLowerCase().includes('hoodie') ||
                           product.shoeName.toLowerCase().includes('t-shirt') ||
                           product.shoeName.toLowerCase().includes('fleece') ||
                           product.shoeName.toLowerCase().includes('watch') ||
                           product.shoeName.toLowerCase().includes('jacket') ||
                           product.shoeName.toLowerCase().includes('pants') ||
                           product.shoeName.toLowerCase().includes('cap') ||
                           product.shoeName.toLowerCase().includes('beanie') ||
                           product.shoeName.toLowerCase().includes('shorts') ||
                           product.shoeName.toLowerCase().includes('bag') ||
                           product.shoeName.toLowerCase().includes('accessory') ||
                           product.shoeName.toLowerCase().includes('vest') ||
                           product.shoeName.toLowerCase().includes('sweatshirt') ||
                           product.shoeName.toLowerCase().includes('off-white') ||
                           product.shoeName.toLowerCase().includes('palace') ||
                           product.shoeName.toLowerCase().includes('stussy') ||
                           product.shoeName.toLowerCase().includes('kith') ||
                           product.shoeName.toLowerCase().includes('heron preston') ||
                           product.shoeName.toLowerCase().includes('yeezy') ||
                           product.shoeName.toLowerCase().includes('a bathing ape') ||
                           product.shoeName.toLowerCase().includes('comme des garcons') ||
                           product.shoeName.toLowerCase().includes('cdg') ||
                           product.shoeName.toLowerCase().includes('undercover') ||
                           product.shoeName.toLowerCase().includes('neighborhood') ||
                           product.shoeName.toLowerCase().includes('billionaire boys club') ||
                           product.shoeName.toLowerCase().includes('bbc') ||
                           product.shoeName.toLowerCase().includes('anti social social club') ||
                           product.shoeName.toLowerCase().includes('assc') ||
                           product.shoeName.toLowerCase().includes('kaws') ||
                           product.shoeName.toLowerCase().includes('off white') ||
                           product.shoeName.toLowerCase().includes('rick owens');
                });
            } else {
                // Only sneakers
                products = products.filter(product => {
                    return product.shoeName.toLowerCase().includes('sneaker') ||
                           product.shoeName.toLowerCase().includes('shoe') ||
                           product.shoeName.toLowerCase().includes('yeezy') ||
                           product.shoeName.toLowerCase().includes('jordan') ||
                           product.shoeName.toLowerCase().includes('nike') ||
                           product.shoeName.toLowerCase().includes('adidas') ||
                           product.shoeName.toLowerCase().includes('puma') ||
                           product.shoeName.toLowerCase().includes('converse') ||
                           product.shoeName.toLowerCase().includes('reebok') ||
                           product.shoeName.toLowerCase().includes('asics') ||
                           product.shoeName.toLowerCase().includes('new balance') ||
                           product.shoeName.toLowerCase().includes('vans') ||
                           product.shoeName.toLowerCase().includes('saucony') ||
                           product.shoeName.toLowerCase().includes('under armour') ||
                           product.shoeName.toLowerCase().includes('air max') ||
                           product.shoeName.toLowerCase().includes('air force') ||
                           product.shoeName.toLowerCase().includes('air jordan') ||
                           product.shoeName.toLowerCase().includes('boost') ||
                           product.shoeName.toLowerCase().includes('ultraboost') ||
                           product.shoeName.toLowerCase().includes('lebron') ||
                           product.shoeName.toLowerCase().includes('kobe') ||
                           product.shoeName.toLowerCase().includes('kd') ||
                           product.shoeName.toLowerCase().includes('curry') ||
                           product.shoeName.toLowerCase().includes('pharrell') ||
                           product.shoeName.toLowerCase().includes('pharrell williams') ||
                           product.shoeName.toLowerCase().includes('off-white') ||
                           product.shoeName.toLowerCase().includes('virgil abloh') ||
                           product.shoeName.toLowerCase().includes('fear of god') ||
                           product.shoeName.toLowerCase().includes('jerry lorenzo');
                });
            }
            
            // Include image URL in the response
            const result = products.map(product => ({
                shoeName: product.shoeName,
                brand: product.brand,
                styleID: product.styleID,
                imageUrl: product.thumbnail,  // Assuming 'thumbnail' is the key for the image URL
            }));

            res.json(result);
        }
    });
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Sneaks app listening on port ${port}`);
});
