# Practice Pitch

This project is a prototype service that allows startup founders to practice their pitch with an AI powered investor.

## Repository layout

- `backend/` – FastAPI application handling submissions and scheduling.
- `frontend/` – React + TypeScript client for the website and form.

## Running the backend

Python 3.11 is required. Install dependencies:

```bash
pip install fastapi uvicorn requests pydantic beautifulsoup4
```

Run the development server:

```bash
uvicorn backend.app:app --reload
```

## Running the frontend

The frontend uses Vite. From the `frontend` directory run:

```bash
npm install
npm run dev
```

Open http://localhost:5173 to view the site.
