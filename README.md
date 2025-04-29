# Sanskrit Text Display App

A Flask-based web application that displays one unique Sanskrit text per day with translations in English and Hindi. Includes an admin interface for managing texts.

## Features
- User-facing homepage displaying daily text with Sanskrit, English, and Hindi translations
- Texts are not repeated unless user clicks "See Again"
- Admin interface to:
  - Add new texts
  - View all texts
  - Edit existing texts
  - Delete texts
- Data stored in JSON files
- Unique UUID for each text

## Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python app.py`

## Project Structure
SanskritTextApp/
├── app.py              # Main Flask application
├── requirements.txt    # Project dependencies
├── README.md           # This file
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── admin.html
├── static/            # Static files
│   ├── style.css
├── data/              # JSON data storage
│   ├── data.json
│   ├── daily_display.json
│   ├── user_seen.json


## Usage
- Visit `http://localhost:5000/` for the user homepage
- Visit `http://localhost:5000/admin` for the admin interface
- Add new texts through the admin interface
- Click "See Again" on homepage to reset viewed texts

## Data Files
- `data.json`: Stores all texts with their translations
- `daily_display.json`: Tracks the current day's displayed text
- `user_seen.json`: Tracks which texts the user has seen

- 

