# TODO API

## Overview
The TODO API is a RESTful API designed to manage tasks effectively with team collaboration capabilities. Users can create, retrieve, update, and delete TODO items, as well as share tasks with team members. This API serves as a backend service for collaborative task management applications, enabling both personal task management and team coordination through shared tasks and collaborative features.

## Features
- **User Authentication**: Secure login with JWT token-based authentication, and user-specific task management
- **CRUD Operations**: Create, Read, Update, and Delete tasks seamlessly
- **Team Collaboration**: 
  - Add collaborators to specific tasks
  - Share tasks with team members
  - Multiple users can work on shared tasks
  - Track task ownership and collaborator access
- **Task Management**:
  - Filter tasks by status and priority
  - Search functionality for task titles and descriptions
  - Pagination support for efficient data handling
- **Scalability**: Designed to handle multiple users with isolated and shared task data
- **OpenAPI Specification**: Fully documented using OpenAPI (Swagger) for easy integration


## Table of Contents
- [Getting Started](#getting-started)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Error Handling](#error-handling)
- [Example Usage](#example-usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8+
- Virtualenv
- A database system (SQLite for development; you can modify setting to use DB system of choice)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CaptainAril/todo_api.git
   cd todo_api
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   cd todo_app
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access API Documentation**:
   Navigate to `http://127.0.0.1:8000/api/docs/` to view the API documentation.
   Access Live API documentation at  `https://todo-api-yh72.onrender.com/api/docs/`

## API Endpoints

All endpoints are prefixed with `/api/v1`. Here is a comprehensive overview of all available API endpoints:


### Authentication
- `POST /api/v1/signup`: Register a new user
- `POST /api/v1/login`: Authenticate and retrieve access and refresh tokens
- `POST /api/v1/refresh`: Get a new access token using refresh token
- `POST /api/v1/logout`: Logout the current user (requires authentication)
- `GET /api/v1/user`: Retrieve current user details (requires authentication)

The API uses JWT token-based authentication with both access and refresh tokens. Include the access token in the Authorization header for all protected endpoints:

```http
Authorization: Bearer your_access_token_here
```

### Authentication Flow
1. Register a new user using `/api/v1/signup`
2. Login with your credentials at `/api/v1/login` to receive both access and refresh tokens
3. Use the access token for all authenticated requests
4. When the access token expires, use `/api/v1/refresh` with your refresh token to get a new access token
5. Use `/api/v1/logout` to invalidate both tokens

### Token Refresh
When your access token expires, send a POST request to `/api/v1/refresh` with your refresh token to obtain a new access token. This allows for continuous authentication without requiring re-login.

### TODO Tasks
- `GET /api/v1/tasks/all`: Retrieve all tasks for the authenticated user with pagination support
  - Query Parameters:
    - `q`: Search tasks by title or description
    - `status`: Filter tasks by status
    - `priority`: Filter tasks by priority
    - `page`: Page number for pagination
    - `page_size`: Number of items per page (default: 10, max: 100)
- `POST /api/v1/tasks/create`: Create a new task
- `GET /api/v1/tasks/{id}`: Retrieve a specific task by ID
- `PUT /api/v1/tasks/{id}/update`: Update a specific task by ID
- `DELETE /api/v1/tasks/{id}/delete`: Delete a specific task by ID

### Collaboration
- `POST /api/v1/tasks/add-collaborator`: Add a collaborator to a task
  - Required fields: `task_id`, `collaborator_id`
- `POST /api/v1/tasks/remove-collaborator`: Remove a collaborator from a task
  - Required fields: `task_id`, `collaborator_id`

### System
- `GET /api/v1/status`: Check API status and health


## Error Handling

The API uses structured error responses. Example:

```json
{
  "error": {
    "code": 400,
    "message": "Invalid input data",
    "details": [
      "Field 'title' is required."
    ]
  }
}
```

| Code | Description |
|------|-------------|
| 200  | Success |
| 400  | Bad Request |
| 401  | Unauthorized |
| 404  | Resource Not Found |
| 500  | Internal Server Error |

## Example Usage

### Create a Task

Request:
```http
POST /tasks HTTP/1.1
Authorization: Bearer your_token_here
Content-Type: application/json

{
  "title": "Learn OpenAPI",
  "description": "Understand how to document APIs effectively.",
  "priority": 1
}
```

Response:
```json
{
  "id": 1,
  "title": "Learn OpenAPI",
  "description": "Understand how to document APIs effectively.",
  "status": "pending",
  "priority": 1,
  "collaborators": [],
  "created_at": "2025-01-01T10:00:00Z"
}
```

### Retrieve All Tasks

Request:
```http
GET /tasks HTTP/1.1
Authorization: Bearer your_token_here
```

Response:
```json
[
  {
    "id": 1,
    "title": "Learn OpenAPI",
    "description": "Understand how to document APIs effectively.",
    "status": "pending",
    "priority": 1,
    "collaborators": [],
    "created_at": "2025-01-01T10:00:00Z"
  }
]
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or fix
3. Commit your changes and push them to your fork
4. Create a pull request to the main repository

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.