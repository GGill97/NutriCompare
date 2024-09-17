# NutriCompare

NutriCompare is a web application that allows users to compare different protein powders based on their nutritional content, price, and other features. This tool helps fitness enthusiasts and health-conscious individuals make informed decisions when choosing protein supplements.

## Features

- Browse and search a wide range of protein powder products
- Filter products by brand, type, price range, and protein content
- Compare up to four products side by side
- Detailed nutritional information for each product
- Visual comparison of macronutrients and micronutrients using charts
- Responsive design for desktop and mobile devices

## Technologies Used

- Python
- Flask (Web framework)
- SQLAlchemy (ORM)
- HTML/CSS
- JavaScript
- Chart.js (for data visualization)
- Bootstrap (for responsive design)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/GGill97/NutriCompare
   cd nutricompare
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```
   flask db upgrade
   ```

5. (Optional) Load sample data:
   ```
   flask load-sample-data
   ```

## Usage

1. Start the Flask development server:

   ```
   flask run
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Use the search and filter options to find protein powders you're interested in

4. Select up to four products to compare

5. View the detailed comparison, including nutritional charts and product information

## Contributing

Contributions to NutriCompare are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with descriptive commit messages
4. Push your changes to your fork
5. Submit a pull request to the main repository
