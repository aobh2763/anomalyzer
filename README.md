# Windows Log Anomaly Detection

<div align="left">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB" alt="React" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
</div>

A full-stack application designed to automatically detect anomalous or potentially malicious behavior in Windows Event Logs (`.evtx`). The project uses Unsupervised Machine Learning (Isolation Forest) to analyze Security, System, and Application logs without requiring labeled datasets.

## Demo

https://github.com/user-attachments/assets/833f25ab-7ee1-4396-85a0-7380e8b5f19f

## Features

- **Upload & Analyze**: Upload Windows Event Log (`.evtx`) files through a sleek web interface.
- **Anomaly Scoring**: Uses an Isolation Forest machine learning model to evaluate the rarity and suspicion of event sequences and payload data.
- **Detailed Parsing**: Custom ETL pipelines handle heterogeneous schemas across different Windows Event IDs.
- **Insights & Visualization**: Provides an interactive dashboard to explore log entries, identify spikes, and highlight anomalous activities.

## Tech Stack

### Backend
- **Python 3.12+**
- **FastAPI**: REST API framework.
- **Scikit-Learn**: Machine Learning models and custom data transformers.
- **Pandas & Numpy**: Data manipulation and feature engineering.
- **evtx**: Parsing raw Windows Event Log files.

### Frontend
- **React (Vite)**: Fast frontend development environment.
- **Mantine UI**: Component library for a modern, responsive interface.
- **AG-Grid**: High-performance data tables for viewing logs.
- **React Router**: Client-side routing.

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
├── assets/                    # Assets for the README
├── data/                      # Raw and processed datasets (ignored in git)
├── notebooks/                 # Jupyter notebooks for data exploration
├── tests/                     # Automated testing suite
├── docs/                      # Project documentation
│   ├── architecture.md        # Architecture documentation
│   └── methodology.md         # CRISP-DM methodology documentation
│
├── pyproject.toml             # Backend Python dependencies (Poetry)
└── README.md                  # This file
```

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js & npm/pnpm
- Poetry (for Python dependency management)

### Before Running
1. **Configure Environment Variables**: Make sure the `.env` file is set up with a `GROQ_API_KEY` in order to get access to the AI explanation feature.
2. **Download an Embedding Model**: Download an embedding model from sentence transformers (such as [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)) and place it in the `src/anomaly_detection/models/` directory, then update the `.env` file with the model name.
3. **Add Anomaly Detection Models**: Download or train three anomaly detection models (one for security, one for application, and one for system logs) and place them in the `src/anomaly_detection/models/` directory. You can use the Jupyter notebooks in the `notebooks/` directory to train your own, or download these pre-trained models:
   - [Security Model](https://file.garden/Zgs8LO9PayWvPfYO/Other/Anomalyzer/security_model.joblib)
   - [Application Model](https://file.garden/Zgs8LO9PayWvPfYO/Other/Anomalyzer/application_model.joblib)
   - [System Model](https://file.garden/Zgs8LO9PayWvPfYO/Other/Anomalyzer/system_model.joblib)

### Backend Setup
1. Navigate to the project root.
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Activate the virtual environment:
   ```bash
   poetry shell
   ```
4. Start the backend server:
   ```bash
   poetry run uvicorn src.anomaly_detection.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd app
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Documentation

For an in-depth explanation of the machine learning approach and the CRISP-DM methodology used for this project, see [docs/methodology.md](docs/methodology.md). For structural details, see [docs/architecture.md](docs/architecture.md).

## License

Please see the [LICENSE](LICENSE) file for more information on how this project is licensed.
