# Development Guide

## Development Environment Setup

### Backend Development

#### IDE Setup
- Recommended: VS Code or PyCharm
- Python Extension for VS Code

#### Code Quality Tools

```bash
# Install development tools
pip install black flake8 mypy isort

# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/

# Sort imports
isort app/
```

#### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_auth.py::test_login

# Watch mode
pytest-watch
```

### Frontend Development

#### IDE Setup
- Recommended: VS Code
- Extensions: ESLint, Prettier, Tailwind CSS IntelliSense (if applicable)

#### Code Quality Tools

```bash
# Install dependencies
npm install

# Lint code
npm run lint

# Format code
npx prettier --write src/

# Run tests
npm run test

# Build project
npm run build
```

#### Hot Reload Development

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

## Git Workflow

### Branch Naming

```
feature/feature-name           # New features
bugfix/bug-description         # Bug fixes
docs/documentation-topic       # Documentation
refactor/refactoring-name      # Refactoring
test/test-description          # Tests
```

### Commit Messages

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `perf`: Performance
- `test`: Tests
- `chore`: Maintenance

Example:
```
feat(auth): add JWT token refresh

- Implement refresh token endpoint
- Add token expiration handling
- Add tests for refresh flow

Closes #123
```

### Pull Request Process

1. Create feature branch from `develop`
2. Make changes with meaningful commits
3. Push branch to GitHub
4. Create pull request with description
5. Ensure CI/CD passes
6. Request review
7. Address feedback
8. Merge to `develop`

## Testing Strategy

### Backend Testing

```
tests/
├── unit/
│   ├── test_auth.py
│   ├── test_projects.py
│   └── test_services.py
├── integration/
│   ├── test_auth_flow.py
│   └── test_project_workflow.py
└── fixtures.py
```

### Frontend Testing

```
src/
├── components/
│   └── Layout.test.tsx
├── features/
│   ├── Login.test.tsx
│   └── Dashboard.test.tsx
├── store/
│   ├── authStore.test.ts
│   └── workspaceStore.test.ts
```

### Test Example (Backend)

```python
import pytest
from app.interfaces.auth import AuthUtils

@pytest.mark.asyncio
async def test_password_hashing():
    password = "test_password_123"
    hashed = AuthUtils.hash_password(password)
    
    assert hashed != password
    assert AuthUtils.verify_password(password, hashed)
    assert not AuthUtils.verify_password("wrong_password", hashed)
```

### Test Example (Frontend)

```typescript
import { render, screen } from '@testing-library/react';
import { useAuthStore } from './authStore';

describe('AuthStore', () => {
  it('should store and retrieve token', () => {
    const { setToken, token } = useAuthStore.getState();
    setToken('test_token');
    expect(useAuthStore.getState().token).toBe('test_token');
  });
});
```

## Code Standards

### Python (Backend)

- Follow PEP 8
- Use type hints
- Max line length: 88 (Black default)
- Docstrings for modules, classes, functions

```python
def get_user_by_email(email: str) -> Optional[UserEntity]:
    """Get user by email address.
    
    Args:
        email: User email address
        
    Returns:
        User entity or None if not found
        
    Raises:
        DatabaseError: If database query fails
    """
```

### TypeScript (Frontend)

- Follow React style guide
- Use strict mode: `"strict": true` in tsconfig
- Use Functional Components with Hooks
- Max line length: 120

```typescript
import api from '../api/axios';

const getProjects = async () => {
  const response = await api.get('/projects');
  return response.data;
};
```

## Adding Features

### Backend Feature Example

1. **Add Domain Entity** (`domain/entities/`)
2. **Add Repository Interface** (`domain/repositories/`)
3. **Add Database Model** (`infrastructure/database.py`)
4. **Implement Repository** (`infrastructure/repositories.py`)
5. **Add Service** (`application/services.py`)
6. **Add Route** (`interfaces/routes_*.py`)
7. **Add Schema** (`interfaces/schemas.py`)
8. **Add Tests** (`tests/`)

### Frontend Feature Example

1. **Create Component** (`features/component-name/`)
2. **Add Store Logic** if needed (`store/`)
3. **Add Route** (`App.tsx`)
4. **Add Tests** (`.test.tsx`)

## Debugging

### Backend Debugging

```python
# Add breakpoint
breakpoint()

# Or use pdb
import pdb; pdb.set_trace()

# Debug with VS Code
# Create .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

### Frontend Debugging

```typescript
// Add console logs
console.log('Value:', value);

// Use React DevTools extension
// Or use browser DevTools (F12)

// Debug with VS Code
// Create .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "vite dev",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:4200",
      "webRoot": "${workspaceFolder}",
      "sourceMapPathOverrides": {
        "webpack:/*": "${webspaceFolder}/*"
      }
    }
  ]
}
```

## Performance Optimization

### Backend

- Use database indexes
- Implement caching
- Optimize queries
- Use connection pooling
- Profile with `cProfile`

### Frontend

- Code splitting (React.lazy)
- Memoization (React.memo, useMemo, useCallback)
- Optimize bundle size
- Virtual scrolling for large lists

## Documentation

- Update README when adding features
- Add docstrings to functions
- Keep API docs current
- Document breaking changes
- Add code examples

## Common Tasks

### Add new environment variable

1. Add to `backend/.env.example` or `frontend/.env.example`
2. Update `backend/app/core/config.py` or frontend environment file
3. Update Docker configs
4. Update documentation

### Add new API endpoint

1. Create route handler
2. Add schema for request/response
3. Add service logic
4. Register router in `main.py`
5. Add tests
6. Update API documentation

### Add new database model

1. Create entity in `domain/entities/`
2. Create SQLAlchemy model in `infrastructure/database.py`
3. Create repository interface in `domain/repositories/`
4. Implement repository in `infrastructure/repositories.py`
5. Create migration with Alembic
6. Add service logic
7. Add tests

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Getting Help

1. Check existing documentation
2. Review code comments
3. Check GitHub Issues
4. Ask in team chat
5. Review similar implementations
