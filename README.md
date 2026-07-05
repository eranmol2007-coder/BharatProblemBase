# BharatProblemBase

A full-stack hackathon problem statement aggregator built with FastAPI and React. Scrapes 100,000+ problem statements from SIH, Unstop, Devfolio, and HackerEarth into a searchable dashboard with advanced filtering, live scraping, auto-classification, and a modern animated UI using Tailwind and Framer Motion.

## Features

- **100,000+ problem statements** from leading hackathon platforms
- **Advanced filtering** by domain, platform, difficulty, and organization
- **Full-text search** with autocomplete suggestions
- **Live scraping** via integrated scrapers for each platform
- **Auto-classification** of domain, difficulty, and tags
- **JWT authentication** with OTP-based email verification
- **Animated UI** with 3D hero section, parallax scrolling, and smooth transitions

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy, SQLite |
| Frontend | React 19, Vite, Tailwind CSS 4, Framer Motion |
| Scraping | Requests, BeautifulSoup, lxml |
| Auth | JWT, bcrypt, OTP-based verification |

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/BharatProblemBase.git
cd BharatProblemBase

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running

**Windows:**
```bash
start.bat
```

**Manual:**
```bash
# Build frontend
cd frontend && npm run build && cd ..

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open [http://localhost:8000](http://localhost:8000)

## Project Structure

```
BharatProblemBase/
├── app/
│   ├── main.py           # FastAPI entry point
│   ├── database.py       # SQLAlchemy config
│   ├── models/           # Database models
│   ├── routers/          # API routes (problems, auth)
│   ├── schemas/          # Pydantic schemas
│   ├── scrapers/         # Platform scrapers
│   ├── ml/               # Classification heuristics
│   └── utils/            # Security, email utilities
├── frontend/
│   ├── src/
│   │   ├── pages/        # Home, Problems, About, Help
│   │   ├── components/   # Navbar, Footer, Cards, Filters
│   │   └── api.js        # API client
│   └── dist/             # Production build
├── scripts/              # Data generation & seeding
├── data/                 # SQLite database & JSON data
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/problems` | List problems with filters |
| GET | `/api/problems/stats` | Get platform statistics |
| GET | `/api/problems/platforms` | List all platforms |
| GET | `/api/problems/domains` | List all domains |
| POST | `/api/problems/scrape` | Trigger live scraping |
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | Login |

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
JWT_SECRET_KEY=your-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
FROM_EMAIL=your-email@gmail.com
```

## License

[MIT](LICENSE)
