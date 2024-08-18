Sneaker Tracker
Sneaker Tracker is a web application designed to help users manage their sneaker collections, track inventory, set goals, and visualize data. This application utilizes the Sneaks API to fetch real-time sneaker data and integrates it with a CRUD-based (Create, Read, Update, Delete) system to allow users to efficiently manage their sneaker inventory.

Features
Sneaks API Integration: Fetch real-time sneaker data, including details such as prices, release dates, and availability.
Inventory Management: Easily add, update, and delete sneakers from your collection using a user-friendly interface.
Goal Setting: Set collection goals and track your progress using visual data representations.
Data Visualization: View statistics and trends related to your sneaker collection through graphs and charts.
User Authentication: Secure login and registration system to manage user accounts and personalized sneaker collections.
Responsive Design: The application is mobile-friendly and works well across different screen sizes.
Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: Django, Python
Database: SQLite (default), can be configured for other databases
API Integration: Sneaks API for sneaker data
Deployment: Render, Gunicorn, Whitenoise for static file management
Setup
Prerequisites
Python 3.8 or higher
Node.js and npm
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/Thedarkplays/sneakertracker.git
cd sneakertracker
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
Install the required Node.js packages:

bash
Copy code
npm install
Apply database migrations:

bash
Copy code
python manage.py migrate
Collect static files:

bash
Copy code
python manage.py collectstatic --noinput
Run the application locally:

bash
Copy code
python manage.py runserver
Deployment
The application can be deployed using services like Render or Heroku. For deployment, ensure that the environment variables (like DJANGO_SECRET_KEY) are properly set and that static files are collected using the appropriate commands.

Usage
User Registration and Login:

Users can register an account and log in to manage their sneaker collection.
Managing Sneakers:

Add new sneakers to the inventory using data fetched from the Sneaks API.
Update existing sneaker details or delete sneakers from the inventory.
View sneaker details, including prices and release dates.
Setting Goals:

Users can set and track goals for their sneaker collection, such as the number of sneakers or total value.
Data Visualization:

View charts and graphs to understand trends and statistics related to your sneaker collection.
Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request.

License
This project is licensed under the MIT License.

Acknowledgments
Sneaks API: Special thanks to druv5319 for providing the Sneaks API.
