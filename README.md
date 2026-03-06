# FinHub

A small full-stack project built using the foundations of React.

The application collects financial market data, stores it in a database, exposes it through an API, and displays it in a React UI.

## Project structure

```
finhub/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   └── yf_service.py
│   └── pyproject.toml
│
└── frontend/
    ├── src/
    ├── package.json
    └── vite.config.ts
```

* **backend**: FastAPI service that fetches financial data and stores it in SQLite
* **frontend**: React + TypeScript UI created with Vite

## Backend

Requirements:

* Python
* `uv`

Install dependencies:

```
cd backend
uv sync
```

Run the API:

```
uv run uvicorn app.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

## Frontend

Requirements:

* Node.js

Install dependencies:

```
cd frontend
npm install
```

Start the development server:

```
npm run dev
```

The UI will run at:

```
http://localhost:5173
```

## Goal of the project

Build a small financial dashboard step-by-step:

* React fundamentals
* React Router
* API integration
* Data visualization
* Full-stack project structure
