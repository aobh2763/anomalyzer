# Architecture

The anomaly detection project is structured as a full-stack application. It uses a Python (FastAPI) backend for log processing and machine learning, and a React (Vite) frontend for the user interface.

## Project Structure

```text
anomaly-detection/
├── app/                       # Frontend React Application
│   ├── src/                   # React source code
│   │   ├── api/               # API service calls
│   │   ├── assets/            # Static assets
│   │   ├── components/        # Reusable UI components
│   │   ├── helpers/           # Utility functions
│   │   ├── hooks/             # Custom React hooks
│   │   ├── pages/             # Application views/pages
│   │   ├── theme.jsx          # UI theming (Mantine)
│   │   └── main.jsx           # App entry point
│   ├── package.json           # Frontend dependencies
│   └── vite.config.js         # Vite bundler configuration
│
├── src/                       # Backend Python Application
│   └── anomaly_detection/     # Main package
│       ├── api/               # FastAPI implementation
│       │   ├── routers/       # API endpoints
│       │   ├── services/      # Business logic and ML inference
│       │   ├── models.py      # Pydantic models (schemas)
│       │   └── db.py          # Database/Storage utilities
│       ├── encoders/          # ML Categorical/Feature encoders
│       ├── etl/               # Data pipeline (Extract, Transform, Load)
│       ├── features/          # Feature engineering logic
│       ├── models/            # Machine learning models (Isolation Forest)
│       ├── parser/            # EVTX parsing utilities
│       ├── storage/           # Local file storage utilities
│       ├── transformers/      # Data transformers
│       ├── utils/             # Helper functions
│       └── main.py            # FastAPI application entry point
│
├── data/                      # Raw and processed datasets (ignored in git)
├── notebooks/                 # Jupyter notebooks for data exploration
├── tests/                     # Automated testing suite
├── docs/                      # Project Documentation
│   ├── architecture.md        # This file
│   └── methodology.md         # CRISP-DM methodology documentation
│
├── pyproject.toml             # Backend Python dependencies (Poetry)
└── README.md                  # Project overview and setup instructions
```

## Backend (Python / FastAPI)
The backend is responsible for:
- Parsing Windows Event Logs (`.evtx`) into structured formats.
- Applying ETL (Extract, Transform, Load) pipelines to prepare data.
- Feature engineering to represent sequences and metadata.
- Using pre-trained `IsolationForest` models to score anomalies.
- Serving REST endpoints for the frontend to upload files and view results.

## Frontend (React / Vite)
The frontend provides a user-friendly interface for analysts:
- Built with React and bundled via Vite.
- Styled using the Mantine UI library.
- Communicates with the FastAPI backend to submit logs and retrieve analysis.
- Visualizes results using AG-Grid and charting components.