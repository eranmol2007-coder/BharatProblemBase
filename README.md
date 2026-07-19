# BharatProblemBase

🌐 **Live Site**: [https://bharat-problem-base.vercel.app](https://bharat-problem-base.vercel.app)

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
git clone https://github.com/eranmol2007-coder/BharatProblemBase.git
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

Open [https://bharat-problem-base.vercel.app](https://bharat-problem-base.vercel.app)

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

## Deployment

### Automated Deployment

This project uses GitHub Actions for automated deployment to Vercel. Every push to the `main` branch automatically triggers:

1. Frontend build (`npm install && npm run build`)
2. Deployment to Vercel production environment

### Required GitHub Secrets

To enable automated deployment, configure these secrets in your GitHub repository settings (Settings → Secrets and variables → Actions):

- **VERCEL_TOKEN**: Personal access token from Vercel dashboard (Settings → Tokens)
- **VERCEL_ORG_ID**: Your Vercel organization ID (found in `.vercel/project.json` after manual deploy)
- **VERCEL_PROJECT_ID**: Your Vercel project ID (found in `.vercel/project.json` after manual deploy)

### Manual Deployment

For manual deployment to Vercel:

```bash
# Install Vercel CLI
npm i -g vercel

# Build frontend
cd frontend && npm run build && cd ..

# Deploy to production
vercel --prod
```

### Environment Variables in Vercel

Configure these in your Vercel project dashboard (Settings → Environment Variables):

- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `SMTP_HOST`: SMTP server hostname (e.g., smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (e.g., 587)
- `SMTP_USER`: Email address for sending OTP emails
- `SMTP_PASS`: Email password or app-specific password
- `FROM_EMAIL`: Sender email address

The `VERCEL` environment variable is automatically set to `"1"` by Vercel's runtime and used to detect production environment.

### Local Development vs Production

- **Local**: Uses `uvicorn` to serve both API and frontend static files from `frontend/dist`
- **Production**: Vercel routes `/api/*` to Python serverless function and serves frontend as static files
- Frontend API client uses relative paths (`/api`) that work in both environments
