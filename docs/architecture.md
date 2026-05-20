# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Browser                           │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/REST
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              React Frontend (Vite)                           │
├─────────────────────────────────────────────────────────────┤
│ • Components (Login, Dashboard)                │
│ • Services (Auth, Project, Workspace)                   │
│ • Store & Context (Zustand)                                 │
│ • Material UI (MUI)                                         │
└───────────────────────┬─────────────────────────────────────┘
                        │ API Calls (http://localhost:8000)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Async)                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Interfaces Layer (API Routes)                        │  │
│  │ • routes_auth.py - Authentication endpoints         │  │
│  │ • routes_projects.py - Project endpoints            │  │
│  │ • routes_workspaces.py - Workspace endpoints        │  │
│  │        │  │
│  └──────────────────────────────────────────────────────┘  │
│                        ▲                                    │
│                        │ Uses                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Application Layer (Services/Use Cases)               │  │
│  │ • AuthService - Login logic                          │  │
│  │ • WorkspaceService - Workspace management            │  │
│  │ • ProjectService - Project management                │  │
│  └──────────────────────────────────────────────────────┘  │
│                        ▲                                    │
│                        │ Depends On                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Domain Layer (Business Logic)                        │  │
│  │ • Entities (User, Workspace, Project)                │  │
│  │ • Repository Interfaces (Abstract)                   │  │
│  │ • Enums (Roles, ProjectStatus)                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                        ▲                                    │
│                        │ Implemented By                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Infrastructure Layer                                 │  │
│  │ • SQLAlchemy ORM & Models                            │  │
│  │ • Repository Implementations                         │  │
│  │ • Database Connection Management                     │  │
│  │ • Authentication Utilities                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                        ▲                                    │
└────────────────────────┼────────────────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │   PostgreSQL Database           │
        │ • Users                         │
        │ • Workspaces                    │
        │ • Projects                      │
        │ • WorkspaceMembers              │
        └─────────────────────────────────┘


## Hexagonal Architecture (Backend)

### Layer Responsibilities

#### Domain Layer (Pure Business Logic)
- **Independence**: No framework dependencies
- **Reusability**: Can be used in different contexts
- **Testability**: Easy to unit test
- **Contents**:
  - Entities: `UserEntity`, `WorkspaceEntity`, `ProjectEntity`, `WorkspaceMemberEntity`
  - Repository Interfaces: Abstract contracts for data access
  - Enums: `Role`, `ProjectStatus`
  - Business Rules: Domain-specific logic

#### Application Layer (Use Cases)
- **Orchestration**: Combines domain entities and repositories
- **Business Workflows**: Implements use cases
- **Service Layer**: `AuthService`, `WorkspaceService`, `ProjectService`
- **DTOs**: Request/Response schemas

#### Infrastructure Layer (Technical Implementations)
- **Persistence**: SQLAlchemy ORM models
- **Repository Implementations**: Concrete implementations of domain interfaces
- **Technical Details**: Database connections, migrations

#### Interfaces Layer (API Exposure)
- **HTTP Routes**: FastAPI routers for REST endpoints
- **Request/Response Validation**: Pydantic schemas
- **Cross-cutting Concerns**: Middleware, error handling
- **Authentication**: JWT token validation

## Data Flow

### 1. Login Flow

```
Frontend                    Backend
  │                           │
  ├─ POST /login ────────────▶│
  │  {email, password}        │
  │                      ┌────▼────────────────┐
  │                      │ AuthService.login() │
  │                      │ 1. Get user by email│
  │                      │ 2. Verify password  │
  │                      │ 3. Get memberships  │
  │                      │ 4. Create JWT token │
  │                      └────┬────────────────┘
  │◀────────────────────────────┤
  │  TokenResponse              │
  │  - access_token             │
  │  - workspace_id             │
  │  - user_id                  │
  │                             │
  ├─ Store token in localStorage
  ├─ Store workspace_id
  ├─ Store user_id
  └─ Redirect to dashboard
```

### 2. Project List Flow

```
Frontend              Backend
  │                     │
  ├─ GET /projects ────▶│
  │  + Authorization    │
  │                 ┌────▼─────────────────┐
  │                 │ ProjectService       │
  │                 │ - Extract workspace  │
  │                 │ - Query projects     │
  │                 │ - Convert to DTOs    │
  │                 └────┬─────────────────┘
  │◀────────────────────────┤
  │  ProjectResponse[]      │
  │  - id                   │
  │  - name                 │
  │  - status               │
  │  - created_at           │
  │                         │
  ├─ Display in table
  
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Workspaces Table
```sql
CREATE TABLE workspaces (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    owner_id UUID NOT NULL REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### WorkspaceMembers Table
```sql
CREATE TABLE workspace_members (
    id UUID PRIMARY KEY,
    workspace_id UUID NOT NULL REFERENCES workspaces(id),
    user_id UUID NOT NULL REFERENCES users(id),
    role ENUM('ADMIN', 'EDITOR', 'READER') DEFAULT 'READER',
    is_active BOOLEAN DEFAULT TRUE,
    joined_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(workspace_id, user_id)
);
```

### Projects Table
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    workspace_id UUID NOT NULL REFERENCES workspaces(id),
    name VARCHAR NOT NULL,
    description TEXT,
    status ENUM('ACTIVE', 'COMPLETED', 'ON_HOLD', 'CANCELLED') DEFAULT 'ACTIVE',
    created_by UUID NOT NULL REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Authentication & Authorization

### JWT Token Structure

```
{
    "sub": "user-id",              # User ID
    "workspace_id": "workspace-id", # Current workspace
    "role": "ADMIN",                # Role in workspace
    "exp": 1234567890,              # Expiration time
    "iat": 1234567890               # Issued at time
}
```

### Authorization Levels

1. **Unauthenticated**: Access to login endpoint only
2. **Authenticated**: Access to all endpoints with valid JWT
3. **Workspace Role**:
   - **ADMIN**: Full access to workspace resources
   - **EDITOR**: Can modify resources
   - **READER**: Read-only access

## Error Handling

### Exception Hierarchy

```
AppBaseError
├── NotFoundError (404)
├── UnauthorizedError (401)
├── ForbiddenError (403)
├── ConflictError (409)
├── ValidationError (422)
├── AIError (500)
└── DatabaseError (500)
```

### Error Response Format

```json
{
    "detail": "User not found"
}
```

## Dependency Injection

The backend uses FastAPI's built-in dependency injection for:
- Database sessions
- Repository instances
- Service instances
- Authenticated user context

Example:
```python
@router.get("/projects")
async def list_projects(
    current_user: TokenData = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service)
):
    # Services and auth automatically injected
    ...
```

## Security Measures

1. **Password Hashing**: bcrypt with salting
2. **JWT Tokens**: HS256 algorithm with secrets
3. **CORS**: Configured for frontend origin
4. **SQL Injection**: ORM parameterized queries
5. **XSS Prevention**: React DOM sanitization
6. **CSRF**: Stateless JWT auth
7. **Secrets Management**: Environment variables
