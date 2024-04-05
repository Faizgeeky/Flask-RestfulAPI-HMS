### Hospital Management System Restful API's using Flask

This project is a Hospital Management System API built using Flask. It provides endpoints for managing patients, doctors, departments, and searching functionality.

### Installation

Step 1: Install all required libraries using pip:

```bash
pip install -r requirements.txt
```

Step 2: Create the SQLite database schema:

```bash
python api/models.py
```

Step 3: Run the Flask application:

```bash
python app.py
```

### Postman Collection

All APIs are documented in the Postman Collection file, which is organized into four separate folders:

- **Patient Management**: APIs related to managing patients.
- **Doctor Management**: APIs related to managing doctors.
- **Department Management**: APIs related to managing departments.
- **Search APIs**: APIs for searching functionality.

You can import the Postman Collection file into your Postman application to access and test the APIs conveniently.

### Tech Stack

The project uses the following technologies:

- Flask
- Flask-RESTful
- JSON
- SQLite3

The Python version used is Python 3 or higher.

### File Structure

```
LOCH.ONE
├── api
│   ├── models.py
│   ├── config.py
│   ├── view.py
│   └── resources
│       └── hm_system.py
├── .gitignore
├── README.md
├── hospital.db
├── app.py
├── apis_list.txt
├── requirements.txt
└── API.postman_collection.json
```