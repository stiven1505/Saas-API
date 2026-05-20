# API Documentation

## Base URL
- Development: `http://localhost:8000/api`
- Production: `https://api.yourdomain.com/api`

## Authentication

All endpoints (except `/auth/login`) require JWT token in Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Response Format

All responses follow this format:

### Success Response (2xx)
```json
{
    "data": { /* response data */ },
    // or direct object/array
}
```

### Error Response (4xx, 5xx)
```json
{
    "detail": "Error message"
}
```

## Endpoints

### Authentication

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}

Response (200 OK):
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "workspace_id": "550e8400-e29b-41d4-a716-446655440001"
}
```

#### Get Token
```
POST /api/auth/token
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}

Response (200 OK):
{
    "access_token": "...",
    "token_type": "bearer",
    "user_id": "...",
    "workspace_id": "..."
}
```

### Workspaces

#### List User Workspaces
```
GET /api/workspaces
Authorization: Bearer <token>

Response (200 OK):
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Workspace Alpha",
        "role": "ADMIN",
        "created_at": "2024-01-15T10:30:00Z"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Workspace Beta",
        "role": "READER",
        "created_at": "2024-01-20T15:45:00Z"
    }
    {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "name": "Workspace Mega",
        "role": "EDITOR",
        "created_at": "2024-01-20T15:45:00Z"
    }
]
```

#### Create Workspace
```
POST /api/workspaces
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "New Workspace",
    "description": "Workspace description"
}

Response (201 Created):
{
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "New Workspace",
    "description": "Workspace description",
    "owner_id": "550e8400-e29b-41d4-a716-446655440000",
    "is_active": true,
    "created_at": "2024-02-01T12:00:00Z"
}
```

### Projects

#### List Projects
```
GET /api/projects
Authorization: Bearer <token>

Response (200 OK):
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Project Alpha",
        "description": "First project",
        "status": "ACTIVE",
        "created_by": "550e8400-e29b-41d4-a716-446655440000",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z"
    }
]
```

#### Create Project
```
POST /api/projects
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "New Project",
    "description": "Project description",
    "status": "ACTIVE"
}

Response (201 Created):
{
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "New Project",
    "description": "Project description",
    "status": "ACTIVE",
    "created_by": "550e8400-e29b-41d4-a716-446655440000",
    "is_active": true,
    "created_at": "2024-02-01T12:00:00Z"
}
```

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

## Rate Limiting

Currently not implemented, but planned for production:
- 100 requests per minute per user
- 1000 requests per hour per user

## Pagination

Currently not implemented, but projects with many items will include:
- `limit`: Number of items (default: 20)
- `offset`: Number of items to skip (default: 0)

## Filtering & Sorting

Currently not fully implemented. Planned filters:
- Projects: by status, created_by
- Workspaces: by owner_id
- Sort: by created_at, name

## Webhooks

Currently not implemented. Planned for future:
- Project updated
- User added to workspace

## SDK Examples

### Python
```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "test@example.com",
    "password": "password123"
})
token = response.json()["access_token"]

# Get projects
headers = {"Authorization": f"Bearer {token}"}
projects = requests.get(f"{BASE_URL}/projects", headers=headers).json()
```

### JavaScript/TypeScript
```typescript
const BASE_URL = "http://localhost:8000/api";

// Login
const loginResponse = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        email: "test@example.com",
        password: "password123"
    })
});
const { access_token } = await loginResponse.json();

// Get projects
const projectsResponse = await fetch(`${BASE_URL}/projects`, {
    headers: { "Authorization": `Bearer ${access_token}` }
});
const projects = await projectsResponse.json();
```

## Testing with cURL

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Get projects
TOKEN="your_token_here"
curl -X GET http://localhost:8000/api/projects \
  -H "Authorization: Bearer $TOKEN"

# Create project
curl -X POST http://localhost:8000/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"New Project","description":"Test"}'


## Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI where you can:
- View all endpoints
- Read parameter descriptions
- Try endpoints directly
- See response examples
