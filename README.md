# APPAREL.IO

APPAREL.IO is a robust web application designed to streamline the management of sneaker collections. Whether you're a sneaker enthusiast or a reseller, this app helps you keep track of your inventory, set collection goals, and visualize key data metrics. By leveraging the Sneaks API, APPAREL.IO fetches real-time sneaker data, providing users with up-to-date information on prices, release dates, and availability.

## Features

- **Sneaks API Integration**: Seamlessly integrate with the [Sneaks API](https://github.com/druv5319/Sneaks-API) to fetch real-time data on sneakers, including prices, release dates, and availability.
- **Inventory Management**: Easily add, update, and delete sneakers from your collection using an intuitive, user-friendly interface.
- **Goal Setting**: Define personal or business-related goals for your sneaker collection and track progress through visual data representations.
- **Data Visualization**: Gain insights into your collection with comprehensive graphs and charts that depict trends and statistics related to your sneaker inventory.
- **User Authentication**: Secure user login and registration, allowing each user to manage their personalized sneaker collections.
- **Responsive Design**: Enjoy a consistent experience across all devices, with a mobile-friendly design that ensures optimal usability on different screen sizes.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django, Python
- **Database**: SQLite (default), easily configurable for other database systems
- **API Integration**: Sneaks API for real-time sneaker data
- **Deployment**: Render, with Gunicorn for serving the Django application and WhiteNoise for static file management

## Setup

### Prerequisites

- Python 3.8 or higher
- Node.js and npm

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Thedarkplays/sneakertracker.git
   cd sneakertracker
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install the required Node.js packages:**

   ```bash
   npm install
   ```

5. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Collect static files:**

   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run the application locally:**

   ```bash
   python manage.py runserver
   ```



## Usage

### User Registration and Login

- Users can register for an account and securely log in to manage their sneaker collection.

### Managing Sneakers

- **Add**: Input new sneakers into your inventory, using data fetched from the Sneaks API to auto-populate fields.
- **Update**: Modify details of existing sneakers in your collection.
- **Delete**: Remove sneakers that are no longer part of your collection.

### Setting Goals

- Set and track goals related to your sneaker collection, such as increasing the number of sneakers or the total value of your inventory.

### Data Visualization

- Visualize trends and key statistics about your sneaker collection through dynamic charts and graphs, helping you make informed decisions.

## Contributing

Contributions are welcome! If you would like to contribute, please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License.

## Acknowledgments

- **Sneaks API**: Special thanks to [druv5319](https://github.com/druv5319) for developing the Sneaks API, which powers the real-time sneaker data in APPAREL.IO.
