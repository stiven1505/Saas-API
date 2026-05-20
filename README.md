# SaaS Platform - Production Ready Monorepo

A complete production-ready SaaS platform with FastAPI backend, React frontend, and Docker support.

## Features

- **Clean Hexagonal Architecture** - Well-organized domain, application, and infrastructure layers
- **Multi-Workspace RBAC** - Role-based access control with workspace isolation
- **JWT Authentication** - Secure token-based authentication
- **PostgreSQL** - Robust data persistence
- **Docker & Docker Compose** - Easy deployment and development
- **GitHub Actions CI/CD** - Automated testing and building
- **Material UI (MUI)** - Modern, responsive UI components
- **Zustand** - Global state management
- **Comprehensive API** - Fully documented with Swagger/OpenAPI

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 20+ (for local frontend development)
- PostgreSQL 16+ (for local development)

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd saas-platform

# Copy environment file
cp .env.example .env


# Start all services
docker-compose up --build

# Services will be available at:
# - Frontend: http://localhost:4200
# - Backend API: http://localhost:8000
# - Database: localhost:5432
```

### Local Development Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Run migrations and seed data (when ready)
python -m alembic upgrade head
python scripts/seed.py

# Start development server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Application will be available at http://localhost:4200
```

## Project Structure

```
project-root/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── domain/              # Domain entities and repositories
│   │   ├── application/         # Use cases and services
│   │   ├── infrastructure/      # Database and implementations
│   │   ├── interfaces/          # API routes and schemas
│   │   ├── core/                # Configuration and exceptions
│   │   └── main.py              # FastAPI application
│   ├── tests/                   # Test suite
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Backend container
│   └── .env                     # Environment variables
│
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── api/                 # Axios config and interceptors
│   │   ├── components/          # Reusable MUI components
│   │   ├── features/            # Feature pages (Login, Dashboard, etc.)
│   │   ├── store/               # Zustand stores
│   │   ├── App.tsx              # Routing and Guards
│   │   └── main.tsx             # Bootstrap entry point
│   ├── package.json             # Node dependencies
│   ├── Dockerfile               # Frontend container
│   └── vite.config.ts           # Vite configuration
│
├── docs/                        # Documentation
│   ├── architecture.md
│   ├── setup.md
│   ├── api.md
│   ├── deployment.md
│   └── development.md
│
├── .github/
│   └── workflows/               # CI/CD pipelines
│       ├── backend-ci.yml
│       ├── frontend-ci.yml
│       └── docker-build.yml
│
├── docker-compose.yml           # Docker Compose configuration
├── .env                         # Environment variables
├── .env.example                 # Example environment variables
└── README.md                    # This file
```

## Architecture

### Backend - Hexagonal Architecture

The backend follows clean hexagonal architecture principles:

- **Domain Layer**: Pure business logic, independent of frameworks
  - Entities: Core business objects
  - Repositories: Abstract interfaces for data access
  
- **Application Layer**: Use cases and orchestration
  - Services: Application logic and workflows
  - DTOs: Data transfer objects
  
- **Infrastructure Layer**: Technical implementations
  - Database: SQLAlchemy ORM
  - Repositories: Implementation of domain interfaces
  
- **Interfaces Layer**: API exposure
  - Routes: HTTP endpoints
  - Schemas: Request/response validation
  - Middleware: Cross-cutting concerns

### Authentication Flow

1. User logs in with email/password
2. Backend validates credentials
3. JWT token is generated with user_id, workspace_id, and role
4. Frontend stores token in localStorage
5. All subsequent requests include token in Authorization header
6. Backend validates token and extracts user context

### Multi-Workspace Architecture

- Users can belong to multiple workspaces
- Each user has a role (ADMIN, EDITOR, READER) per workspace
- JWT contains current workspace context
- API enforces workspace isolation

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/token` - Get access token

### Projects
- `GET /api/projects` - List projects in current workspace
- `POST /api/projects` - Create new project

### Workspaces
- `GET /api/workspaces` - List user's workspaces
- `POST /api/workspaces` - Create new workspace


## Database

### Models

- **User** - User accounts
- **Workspace** - Isolated work environments
- **WorkspaceMember** - User-workspace assignments with roles
- **Project** - Projects within workspaces

### Migrations

Alembic is used for database migrations. To create a new migration:

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Testing

### Backend Tests

```bash
cd backend
pytest -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment Variables

Create `.env` file with production values:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/db

# JWT
JWT_SECRET=your-strong-secret-key
JWT_EXPIRE_MINUTES=60


# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
```

## Development

### Code Style

- Backend: PEP 8, type hints
- Frontend: ESLint, Prettier, React Best Practices

### Git Workflow

1. Create feature branch
2. Make changes
3. Push and create pull request
4. CI/CD runs tests
5. Merge after approval

## Security

- Passwords hashed with bcrypt
- JWT tokens with expiration
- CORS configured
- SQL injection prevention (ORM)
- XSS protection (React DOM sanitization)
- Environment variables for secrets
- No hardcoded credentials

## Performance

- Async/await in FastAPI
- Connection pooling in database
- Code splitting and lazy loading in React (Vite)
- Caching strategies
- Indexed database queries

## Support

For issues and questions:
- GitHub Issues
- Documentation: [docs/](docs/)
- Contact: support@saas-platform.com

## License

MIT License - see LICENSE file for details
