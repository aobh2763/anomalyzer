anomaly-detection/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── pyproject.toml
│
├── data/                          # Ignored
│   ├── raw/                       # Original EVTX files
│   ├── interim/                   # Parsed but not finalized
│   ├── processed/                 # Feature-ready data
│   └── README.md                  # Data documentation
│
├── notebooks/
│
├── src/
│   ├── parser/
│   ├── features/
│   ├── models/
│   ├── utils/
│   ├── api/
│   └── main.py
│
├── apps/
│   └── dashboard/                 # Next.js
│
├── docs/
│   ├── methodology.md
│   └── architecture.md
│
├── notes/                         # Ignored
│   ├── journal.md
│   └── supervisor.md
│
├── tests/
│
├── assets/
│   ├── diagrams/
│   └── screenshots/
│
└── outputs/