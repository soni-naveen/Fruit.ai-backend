# Fruit.Ai backend
This application allows you to manage FAQs related to fruits. You can create, view, update, and delete FAQs through a simple interface.

## Features
Create: Add new FAQs.\
Read: View all FAQs or a specific FAQ by ID.\
Update: Edit existing FAQs.\
Delete: Remove FAQs.

## Endpoints
GET /faqs: Fetch all faqs.\
GET /faqs/:id: Fetch a single faq by ID.\
POST /faqs: Create a new faq.\
PUT /faqs/:id: Update a faq by ID.\
DELETE /faqs/:id: Delete a faq by ID.

## Setup Backend
Install Dependencies:

pip install Flask Flask-PyMongo Flask-Cors\
Run the Server:

python app.py

The server will run on http://localhost:4000.

### Error Handling
Includes error responses for invalid inputs, not found errors, and server issues.
