# SQL Task Project

## Overview

This Python project demonstrates basic SQL operations and REST API integration. It uses Python, Flask, SQLAlchemy, and provides comprehensive Swagger documentation for the API endpoints.

## Features

- CRUD operations for managing students and courses
- REST API built with Flask
- Database management using SQLAlchemy
- Automatic database population
- Swagger documentation for API endpoints
- Unit tests for application and API

## Project Structure

```
.
├── app.py
├── rest_api_app.py
├── creator.py
├── models.py
├── swagger_docs/
│   ├── add_student_on_course.yml
│   ├── delete_student_by_id.yml
│   ├── delete_student_from_course.yml
│   ├── groups_by_quantity.yml
│   ├── put_student.yml
│   └── students_by_course.yml
└── tests/
    ├── test_app.py
    └── test_rest_api_app.py
```

## Setup

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd flask_university_api
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Database Setup

Initialize and populate the database:

```bash
python creator.py
```

### Running the Application

Start Flask server:

```bash
python app.py
```

Access the REST API server:

```bash
python rest_api_app.py
```

### Swagger API Documentation

Swagger documentation is available in the `swagger_docs` directory.

### Running Tests

Run unit tests:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome. Please submit pull requests or create issues.

## License

MIT License.


