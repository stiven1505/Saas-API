#!/bin/bash

# Verification script to check if the project structure is complete

echo "🔍 SaaS Platform - Project Structure Verification"
echo "=================================================="
echo ""

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
        return 0
    else
        echo "❌ $1"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $1/"
        return 0
    else
        echo "❌ $1/"
        return 1
    fi
}

echo "📁 Backend Structure:"
check_dir "backend/app/domain"
check_dir "backend/app/application"
check_dir "backend/app/infrastructure"
check_dir "backend/app/interfaces"
check_file "backend/app/main.py"
check_file "backend/requirements.txt"
check_file "backend/Dockerfile"
check_file "backend/.env"

echo ""
echo "🎨 Frontend Structure:"
check_dir "frontend/src/api"
check_dir "frontend/src/components"
check_dir "frontend/src/features"
check_dir "frontend/src/store"
check_file "frontend/package.json"
check_file "frontend/Dockerfile"
check_file "frontend/vite.config.ts"
check_file "frontend/src/main.ts"
check_file "frontend/src/index.html"

echo ""
echo "🐳 Docker Configuration:"
check_file "docker-compose.yml"
check_file ".env"
check_file ".env.example"

echo ""
echo "📚 Documentation:"
check_file "README.md"
check_file "docs/architecture.md"
check_file "docs/setup.md"
check_file "docs/api.md"
check_file "docs/development.md"
check_file "docs/deployment.md"

echo ""
echo "🔄 CI/CD Configuration:"
check_file ".github/workflows/backend-ci.yml"
check_file ".github/workflows/frontend-ci.yml"
check_file ".github/workflows/docker-build.yml"

echo ""
echo "🧪 Tests:"
check_file "backend/tests/conftest.py"
check_file "backend/tests/test_auth.py"
check_file "backend/tests/test_projects.py"

echo ""
echo "✨ Additional Files:"
check_file ".gitignore"
check_file "start.sh"
check_file "IMPLEMENTATION_SUMMARY.md"

echo ""
echo "=================================================="
echo "✅ Project structure verification complete!"
echo ""
echo "🚀 Next steps:"
echo "   2. Run: bash start.sh"
echo "   3. Access frontend at http://localhost:4200"
echo ""
