# Cafe REST API

This project is a RESTful API built with Flask and SQLAlchemy to manage a directory of cafes. It allows clients to:


- Retrieve a random cafe
- List all cafes
- Search cafes by location
- Add new cafes
- Update cafe coffee prices
- Report and delete closed cafes (with API key authentication)

The API uses an SQLite database (`cafe.db`) to store cafe information, including amenities like WiFi, sockets, toilets, and pricing.

## API Documentation

Detailed API documentation is available on Postman:

[View API docs on Postman](https://documenter.getpostman.com/view/45814091/2sB2x6kBYV#3408d883-8fb1-4945-8ab4-5b35189b4416)

---

## Features

- **GET /random** — Get a random cafe from the database
- **GET /all_cafes** — Get all cafes sorted by name
- **GET /search?loc=LOCATION** — Search cafes by location
- **POST /add** — Add a new cafe (form data required)
- **PATCH /update-price/<cafe_id>?new_price=PRICE** — Update the coffee price of a cafe
- **DELETE /report-closed/<cafe_id>?api_key=API_KEY** — Delete a cafe with API key authentication

---

## Technologies Used

- Python 3
- Flask
- SQLAlchemy
- SQLite
- dotenv (for environment variables)

---

## Setup and Running

1. Clone the repo
2. Install dependencies (`flask`, `flask_sqlalchemy`, `python-dotenv`)
3. Create a `.env` file with your API key: `FLASK_API_KEY=your_secret_key`
4. Run the app: `python app.py`
5. Access API endpoints at `http://localhost:5000`

---

## Example Data Model

Each cafe record includes:

- Name
- Location
- Map URL
- Image URL
- Seating capacity
- Amenities (WiFi, sockets, toilets, phone calls)
- Coffee price

---

Feel free to contribute, open issues, or suggest new features!

## About

This project is inspired by the **100 Days of Code** challenge with Angela Yu from **Udemy**.  
It’s a practical exercise in building REST APIs with Flask and SQLAlchemy.
