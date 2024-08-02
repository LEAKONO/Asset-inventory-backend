# Asset Inventory Management System

## Overview
The Asset Inventory Management System is a backend project designed to manage and track assets within an organization. It includes user authentication and role-based access control, allowing different levels of access and permissions for employees, procurement managers, and admins.

## Features
- *User Authentication*: Sign up, login, and logout functionalities.
- *Role-Based Access Control*: Different roles (employee, procurement manager, admin) with specific permissions.
- *Asset Management*: Add, update, and allocate assets.
- *Request Management*: Employees can request new assets or repairs, and procurement managers can review and approve requests.

## Technologies Used
- *Backend*: Python Flask
- *Database*: PostgreSQL
- *Authentication*: JSON Web Token (JWT)
- *Dependencies Management*: Pipenv

## Installation
1. Clone the repository:
    bash
    git clone https://github.com/LEAKONO/Asset-inventory-backend.git
    <!-- cd asset-inventory-management -->
    

2. Set up the virtual environment and install dependencies:
    bash
    pipenv install
    

3. Create the .env file with your environment variables:
    env
    DATABASE_URL=your_database_url
    JWT_SECRET_KEY=your_jwt_secret_key
    

4. Initialize the database:
    bash
    pipenv run flask db init
    pipenv run flask db migrate
    pipenv run flask db upgrade
    

## Running the Application
1. Activate the virtual environment:
    bash
    pipenv shell
    

2. Run the Flask application:
    bash
    flask run
    

## API Endpoints
### Auth Endpoints
- *Sign Up*
    - URL: http://127.0.0.1:5000/auth/signup
    - Method: POST
    - Payload: { "username": "example", "password": "example", "email": "example@example.com" }
    - Description: Register a new user. Role is determined by the email domain.

- *Login*
    - URL: http://127.0.0.1:5000/auth/login
    - Method: POST
    - Payload: { "username": "example", "password": "example" }
    - Description: Authenticate a user and return a JWT token.

### Asset Endpoints
- *Create Asset*
    - URL: http://127.0.0.1:5000/api/assets
    - Method: POST
    - Payload: { "name": "Laptop", "description": "Dell XPS 13", "image_url": "http://example.com/image.jpg", "category": "Electronics" }
    - Description: Add a new asset.

- *Get All Assets*
    - URL: http://127.0.0.1:5000/api/assets
    - Method: GET
    - Description: Retrieve all assets.

- *Allocate Asset*
    - URL: http://127.0.0.1:5000/api/assets/<int:asset_id>/allocate
    - Method: POST
    - Payload: { "user_id": 1 }
    - Description: Allocate an asset to a user. Role required: procurement_manager.

### Request Endpoints
- *Create Request*
    - URL: http://127.0.0.1:5000/api/requests
    - Method: POST
    - Payload: { "asset_id": 1, "reason": "New project", "quantity": 5, "urgency": "High" }
    - Description: Create a new request for an asset.

- *Get User Requests*
    - URL: http://127.0.0.1:5000/api/user/requests
    - Method: GET
    - Description: Get all requests made by the current user.

- *Get Pending Requests*
    - URL: http://127.0.0.1:5000/api/requests/pending
    - Method: GET
    - Description: Retrieve all pending requests. Role required: procurement_manager.

- *Update Request Status*
    - URL: http://127.0.0.1:5000/api/requests/<int:request_id>
    - Method: PATCH
    - Payload: { "status": "Approved" }
    - Description: Update the status of a request. Role required: procurement_manager.

## Authentication and Authorization
- *JWT Authentication*: Secure the endpoints using JWT tokens. Users must include the token in the Authorization header as Bearer <token>.
- *Role-Based Access Control*: Use decorators to restrict access to certain endpoints based on user roles.

## Contribution Guidelines
1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.