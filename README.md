# Graph Theory Password Strength Analyzer

A password strength analyzer that uses graph theory to evaluate password security. It analyzes passwords based on their representation as walks on a QWERTY keyboard graph, providing detailed metrics about password strength.

## Features

- Analyzes password strength using graph theory concepts
- Detects keyboard walks and patterns
- Provides a detailed breakdown of password metrics
- Simple web interface and API
- Command-line interface for scripting

## Quick Start

### Prerequisites

- Python 3.7+
- Node.js (for development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GraphTheoryPasswordStrengthAnalyzer.git
   cd GraphTheoryPasswordStrengthAnalyzer
   ```

2. Set up the Python virtual environment and install dependencies:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   
   # Install backend dependencies
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

#### Backend (API Server)

```bash
# From the backend directory
uvicorn app.api:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

#### Frontend

Open `frontend/index.html` directly in your browser or use a simple HTTP server:

```bash
# From the project root
python -m http.server 3000
# Then visit http://localhost:3000/frontend/index.html
```

### Using the CLI

```bash
# From the backend directory
python -m app.cli yourpassword
```

## API Endpoints

- `POST /analyze` - Analyze a password
  - Request body: `{"password": "yourpassword"}`
  - Returns: JSON with analysis results

- `GET /health` - Health check endpoint
  - Returns: `{"status": "ok"}`

## Development

### Running Tests

```bash
# From the backend directory
pytest -v
```

### Project Structure

```
GraphTheoryPasswordStrengthAnalyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── keyboard_graph.py    # Keyboard graph implementation
│   │   ├── password_analyzer.py # Core analysis logic
│   │   ├── api.py              # FastAPI endpoints
│   │   └── cli.py              # Command-line interface
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── index.html              # Web interface
│   └── app.js                  # Frontend JavaScript
├── tests/                      # Test files
│   └── test_analyzer.py
└── README.md                   # This file
```

## How It Works

The analyzer evaluates passwords based on several graph-theoretic metrics:

1. **Keyboard Graph Analysis**: Models the QWERTY keyboard as a graph where keys are nodes and edges represent adjacent keys.
2. **Adjacency Ratio**: Measures how many consecutive characters are adjacent on the keyboard.
3. **Longest Simple Path**: Finds the longest sequence of adjacent keys without repetition.
4. **Vertex Cover Analysis**: Uses a greedy algorithm to find a vertex cover of the password's induced subgraph.
5. **Character Variety**: Checks for different character types (lowercase, uppercase, digits, symbols).
6. **Length Score**: Rewards longer passwords.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
