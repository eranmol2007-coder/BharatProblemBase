"""
Preservation Property Tests - Local Development Workflow

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**

These tests capture the baseline behavior of local development that MUST remain unchanged
after implementing the Vercel deployment fix. They follow observation-first methodology:
observe current behavior, then encode as test assertions.

IMPORTANT: These tests should PASS on UNFIXED code and PASS on FIXED code.
If they fail after the fix, it indicates a regression in local development.
"""

import os
import sys
import subprocess
import time
import json
import socket
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_test(name):
    print(f"\n{Colors.BLUE}→ Testing: {name}{Colors.RESET}")


def print_pass(message):
    print(f"  {Colors.GREEN}✓ PASS: {message}{Colors.RESET}")


def print_fail(message):
    print(f"  {Colors.RED}✗ FAIL: {message}{Colors.RESET}")


def print_info(message):
    print(f"  {Colors.YELLOW}ℹ INFO: {message}{Colors.RESET}")


def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except OSError:
            return True


def test_backend_port_configuration():
    """
    Property: Backend server configuration specifies port 8000
    Requirements: 3.1 - Local backend continues to serve on localhost:8000
    """
    print_test("Backend Port Configuration")
    
    # Check start_backend.bat for port configuration
    start_backend = PROJECT_ROOT / "start_backend.bat"
    if start_backend.exists():
        content = start_backend.read_text()
        # Check that uvicorn command exists with port 8000
        if "uvicorn" in content and "app.main:app" in content and "8000" in content:
            print_pass("start_backend.bat contains uvicorn command for app.main:app on port 8000")
        else:
            print_fail("start_backend.bat missing expected uvicorn command or port 8000")
            return False
    else:
        print_fail("start_backend.bat not found")
        return False
    
    # Check vite.config.js proxy configuration
    vite_config = PROJECT_ROOT / "frontend" / "vite.config.js"
    if vite_config.exists():
        content = vite_config.read_text()
        if "localhost:8000" in content and "'/api'" in content:
            print_pass("vite.config.js proxies /api to localhost:8000")
        else:
            print_fail("vite.config.js proxy configuration changed")
            return False
    else:
        print_fail("vite.config.js not found")
        return False
    
    return True


def test_frontend_build_structure():
    """
    Property: Frontend build generates dist/ with index.html and assets
    Requirements: 3.3 - Frontend build continues to generate static assets in frontend/dist
    """
    print_test("Frontend Build Output Structure")
    
    dist_dir = PROJECT_ROOT / "frontend" / "dist"
    if not dist_dir.exists():
        print_fail("frontend/dist directory does not exist - run 'npm run build' first")
        return False
    
    print_pass("frontend/dist directory exists")
    
    # Check for index.html
    index_html = dist_dir / "index.html"
    if index_html.exists():
        print_pass("frontend/dist/index.html exists")
    else:
        print_fail("frontend/dist/index.html not found")
        return False
    
    # Check for assets directory
    assets_dir = dist_dir / "assets"
    if assets_dir.exists():
        print_pass("frontend/dist/assets directory exists")
    else:
        print_fail("frontend/dist/assets directory not found")
        return False
    
    # Check that assets contains JS/CSS files
    asset_files = list(assets_dir.glob("*"))
    if len(asset_files) > 0:
        print_pass(f"frontend/dist/assets contains {len(asset_files)} files")
    else:
        print_fail("frontend/dist/assets is empty")
        return False
    
    return True


def test_api_endpoint_configuration():
    """
    Property: API endpoints are configured under /api prefix
    Requirements: 3.4 - API endpoints continue to work with same behavior
    """
    print_test("API Endpoint Configuration")
    
    # Check app/main.py for router configuration
    main_py = PROJECT_ROOT / "app" / "main.py"
    if not main_py.exists():
        print_fail("app/main.py not found")
        return False
    
    content = main_py.read_text()
    
    # Check for router includes
    if "problems_router" in content and "auth_router" in content:
        print_pass("Main app includes problems_router and auth_router")
    else:
        print_fail("Expected routers not found in app/main.py")
        return False
    
    # Check for health endpoint
    if "/api/health" in content:
        print_pass("Health endpoint configured at /api/health")
    else:
        print_fail("Health endpoint not found")
        return False
    
    # Check for CORS middleware
    if "CORSMiddleware" in content:
        print_pass("CORS middleware configured")
    else:
        print_fail("CORS middleware not found")
        return False
    
    return True


def test_database_structure():
    """
    Property: Database configuration and models remain unchanged
    Requirements: 3.5 - SQLite database operations continue to function
    """
    print_test("Database Configuration")
    
    # Check database.py exists
    database_py = PROJECT_ROOT / "app" / "database.py"
    if not database_py.exists():
        print_fail("app/database.py not found")
        return False
    
    print_pass("app/database.py exists")
    
    # Check models directory
    models_dir = PROJECT_ROOT / "app" / "models"
    if not models_dir.exists():
        print_fail("app/models directory not found")
        return False
    
    print_pass("app/models directory exists")
    
    # Check for key model files
    problem_model = models_dir / "problem_statement.py"
    user_model = models_dir / "user.py"
    
    if problem_model.exists():
        print_pass("ProblemStatement model exists")
    else:
        print_fail("ProblemStatement model not found")
        return False
    
    if user_model.exists():
        print_pass("User model exists")
    else:
        print_fail("User model not found")
        return False
    
    # Check data directory for database
    data_dir = PROJECT_ROOT / "data"
    if data_dir.exists():
        print_pass("data/ directory exists for SQLite database")
    else:
        print_fail("data/ directory not found")
        return False
    
    return True


def test_auth_flow_configuration():
    """
    Property: Authentication flow with JWT and OTP remains configured
    Requirements: 3.6 - Authentication flows continue to work with JWT and email verification
    """
    print_test("Authentication Flow Configuration")
    
    # Check auth router
    auth_router = PROJECT_ROOT / "app" / "routers" / "auth.py"
    if not auth_router.exists():
        print_fail("app/routers/auth.py not found")
        return False
    
    print_pass("Authentication router exists")
    
    # Check security utils
    security_utils = PROJECT_ROOT / "app" / "utils" / "security.py"
    if not security_utils.exists():
        print_fail("app/utils/security.py not found")
        return False
    
    content = security_utils.read_text()
    
    # Check for JWT-related functions
    if "jwt" in content.lower():
        print_pass("JWT functionality present in security utils")
    else:
        print_fail("JWT functionality not found")
        return False
    
    # Check email utils
    email_utils = PROJECT_ROOT / "app" / "utils" / "email.py"
    if email_utils.exists():
        print_pass("Email utilities exist for OTP verification")
    else:
        print_fail("Email utilities not found")
        return False
    
    return True


def test_vercel_environment_detection():
    """
    Property: IS_VERCEL flag correctly distinguishes local vs production
    Requirements: 3.1 - Local development not affected by Vercel detection
    """
    print_test("Vercel Environment Detection")
    
    # Ensure VERCEL environment variable is not set locally
    vercel_env = os.environ.get("VERCEL")
    if vercel_env == "1":
        print_fail("VERCEL environment variable is set to '1' - should not be set locally")
        return False
    else:
        print_pass("VERCEL environment variable not set (local environment)")
    
    # Check that IS_VERCEL logic exists in main.py
    main_py = PROJECT_ROOT / "app" / "main.py"
    content = main_py.read_text()
    
    if 'IS_VERCEL = os.environ.get("VERCEL") == "1"' in content:
        print_pass("IS_VERCEL detection logic present in app/main.py")
    else:
        print_fail("IS_VERCEL detection logic missing or changed")
        return False
    
    # Check that static file serving is conditional
    if "if not IS_VERCEL" in content:
        print_pass("Static file serving is conditional on IS_VERCEL flag")
    else:
        print_fail("Static file serving not properly conditional")
        return False
    
    return True


def test_package_json_scripts():
    """
    Property: Frontend package.json scripts remain unchanged
    Requirements: 3.2, 3.3 - Frontend dev and build scripts work as before
    """
    print_test("Frontend Package Scripts")
    
    package_json = PROJECT_ROOT / "frontend" / "package.json"
    if not package_json.exists():
        print_fail("frontend/package.json not found")
        return False
    
    with open(package_json) as f:
        package_data = json.load(f)
    
    scripts = package_data.get("scripts", {})
    
    # Check dev script
    if scripts.get("dev") == "vite":
        print_pass("Dev script configured: 'vite'")
    else:
        print_fail(f"Dev script changed: {scripts.get('dev')}")
        return False
    
    # Check build script
    if scripts.get("build") == "vite build":
        print_pass("Build script configured: 'vite build'")
    else:
        print_fail(f"Build script changed: {scripts.get('build')}")
        return False
    
    return True


def test_api_serverless_wrapper():
    """
    Property: api/index.py correctly wraps app for Vercel
    Requirements: Vercel deployment readiness (doesn't affect local dev)
    """
    print_test("API Serverless Wrapper")
    
    api_index = PROJECT_ROOT / "api" / "index.py"
    if not api_index.exists():
        print_fail("api/index.py not found")
        return False
    
    content = api_index.read_text()
    
    if "from app.main import app" in content:
        print_pass("api/index.py correctly imports app from app.main")
    else:
        print_fail("api/index.py import statement changed or missing")
        return False
    
    return True


def run_all_tests():
    """Run all preservation tests"""
    print(f"\n{Colors.BLUE}{'=' * 70}")
    print("PRESERVATION PROPERTY TESTS - LOCAL DEVELOPMENT WORKFLOW")
    print(f"{'=' * 70}{Colors.RESET}\n")
    
    print_info("These tests verify that local development behavior remains unchanged")
    print_info("All tests should PASS before and after implementing the deployment fix")
    
    tests = [
        ("Backend Port Configuration", test_backend_port_configuration),
        ("Frontend Build Structure", test_frontend_build_structure),
        ("API Endpoint Configuration", test_api_endpoint_configuration),
        ("Database Structure", test_database_structure),
        ("Authentication Flow Configuration", test_auth_flow_configuration),
        ("Vercel Environment Detection", test_vercel_environment_detection),
        ("Frontend Package Scripts", test_package_json_scripts),
        ("API Serverless Wrapper", test_api_serverless_wrapper),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_fail(f"Test '{name}' raised exception: {e}")
            results.append((name, False))
    
    # Summary
    print(f"\n{Colors.BLUE}{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}{Colors.RESET}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if result else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"  {status} - {name}")
    
    print(f"\n{Colors.BLUE}Total: {passed}/{total} tests passed{Colors.RESET}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}✓ All preservation tests PASSED{Colors.RESET}")
        print(f"{Colors.GREEN}Local development workflow is preserved correctly{Colors.RESET}\n")
        return True
    else:
        print(f"{Colors.RED}✗ Some preservation tests FAILED{Colors.RESET}")
        print(f"{Colors.RED}Local development workflow may have regressions{Colors.RESET}\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
