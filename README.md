# Markdown App

A simple Flask application for creating, managing, and rendering Markdown notes. It also supports grammar checking and file attachments.

## Features

- Create, view, update, and delete notes.
- Store notes with titles and Markdown content.
- Render Markdown content as HTML.
- Check grammar using LanguageTool.
- Upload and manage note attachments.
- Track note creation and update timestamps.
- Store data in an SQLite database.

## Tech Stack

- **Python**
- **Flask** — Web framework
- **Flask-SQLAlchemy** — Database management
- **SQLite** — Database
- **Markdown** — Markdown-to-HTML conversion
- **LanguageTool** — Grammar checking
- **Flask-WTF** — File upload forms and validation

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Birmechis/Markdown-app.git
   cd Markdown-app
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python run.py
   ```

The application initializes the SQLite database automatically when it starts.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/notes` | Create a note |
| GET | `/notes` | Get all notes |
| GET | `/notes/<id>` | Get a specific note |
| PUT | `/notes/<id>` | Update a note |
| DELETE | `/notes/<id>` | Delete a note |
| POST | `/notes/<id>/checks` | Check grammar |
| GET | `/notes/<id>/render` | Render a note as HTML |
| POST | `/notes/<id>/attachments` | Upload an attachment |
| GET | `/notes/<id>/attachments` | Get a note's attachments |

## Project Structure

```text
Markdown-app/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   └── static/
│       └── files/
├── requirements.txt
└── run.py
```

## License

No license has been specified yet.