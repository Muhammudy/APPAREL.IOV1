const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const SneaksAPI = require('sneaks-api');
const sneaks = new SneaksAPI();

app.use(bodyParser.json());

const salesData = {}; // In-memory store for sales data

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
