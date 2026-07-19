# Implementation Plan

## Overview

This plan follows the bug condition methodology to fix Vercel deployment issues. We'll first write tests to understand the current deployment failures (exploration), preserve existing local development behavior (preservation), then implement the fix with confidence.

---

## Testing and Implementation Tasks

- [ ] 1. Write bug condition exploration test (BEFORE implementing fix)
  - **Property 1: Bug Condition** - Deployment Infrastructure Verification
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate deployment is not working
  - **Scoped Verification Approach**: Check concrete deployment infrastructure components
  
  **Test Implementation**:
  - Verify GitHub Actions workflow file exists at `.github/workflows/deploy.yml`
  - Verify workflow contains required Vercel deployment steps
  - Verify `vercel.json` contains frontend build configuration
  - Verify `.vercelignore` file exists and excludes unnecessary files
  - Verify README.md contains production URL section
  
  **Test Assertions (Expected Behavior from Design)**:
  - GitHub Actions workflow file should exist and be syntactically valid
  - Workflow should trigger on push to main branch
  - Workflow should include frontend build step (`npm install && npm run build`)
  - Workflow should include Vercel deployment step with production flag
  - `vercel.json` should specify build command for frontend
  - `.vercelignore` should exclude `.venv`, `.venv-1`, `node_modules`, `.git`, `__pycache__`
  - README should contain production URL or placeholder in prominent location
  
  **Run on UNFIXED code**:
  - Create a test script `scripts/test_deployment_infrastructure.py` that checks these conditions
  - Run: `python scripts/test_deployment_infrastructure.py`
  
  **EXPECTED OUTCOME**: Test FAILS with specific missing components identified:
  - "FAIL: GitHub Actions workflow not found at .github/workflows/deploy.yml"
  - "FAIL: vercel.json missing build configuration"
  - "FAIL: .vercelignore file not found"
  - "FAIL: README.md missing production URL section"
  
  **Document counterexamples** to understand what's missing:
  - Which specific files are missing
  - Which configuration sections are incomplete
  - What the deployment pipeline gaps are
  
  Mark task complete when test is written, run, and failures are documented
  
  _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Local Development Workflow Preservation
  - **IMPORTANT**: Follow observation-first methodology
  - **GOAL**: Capture baseline local development behavior that must not change
  
  **Observation Phase (on UNFIXED code)**:
  - Start local backend: `uvicorn app.main:app --reload` → observe it starts on port 8000
  - Check API response: `curl http://localhost:8000/api/health` → observe response format
  - Start frontend dev: `cd frontend && npm run dev` → observe it starts with proxy
  - Build frontend: `cd frontend && npm run build` → observe dist/ structure
  - Check API call from frontend dev → observe successful proxying to localhost:8000
  
  **Write Property-Based Tests** capturing observed patterns:
  - Create `scripts/test_local_preservation.py`
  - Test: Local uvicorn server starts and responds on port 8000
  - Test: Frontend dev server starts and proxies /api to localhost:8000
  - Test: Frontend build generates dist/ directory with expected structure
  - Test: All API endpoints return expected status codes and response shapes
  - Test: Database operations (read/write) work correctly
  
  **Run tests on UNFIXED code**:
  - Run: `python scripts/test_local_preservation.py`
  
  **EXPECTED OUTCOME**: Tests PASS (confirms baseline behavior to preserve)
  - "PASS: Backend starts on http://localhost:8000"
  - "PASS: Frontend dev server proxies API calls correctly"
  - "PASS: Frontend build generates dist/ with index.html"
  - "PASS: API endpoints return expected responses"
  - "PASS: Database operations function correctly"
  
  Mark task complete when tests are written, run, and passing on unfixed code
  
  _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ] 3. Implement Vercel deployment fix

  - [ ] 3.1 Create GitHub Actions workflow file
    - Create `.github/workflows/deploy.yml`
    - Configure workflow to trigger on push to `main` branch
    - Add job with Node.js and Python setup
    - Add step: Install frontend dependencies (`cd frontend && npm install`)
    - Add step: Build frontend (`cd frontend && npm run build`)
    - Add step: Deploy to Vercel using `amondnet/vercel-action@v25`
    - Configure Vercel action with `--prod` flag and required secrets
    - Document required GitHub secrets in comments: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`
    - _Bug_Condition: isBugCondition(action) where action == "PUSH_TO_MAIN" AND NOT githubActionsTriggered()_
    - _Expected_Behavior: Workflow exists, triggers on push, builds frontend, deploys to Vercel (from design)_
    - _Preservation: No changes to local development workflows_
    - _Requirements: 1.2, 2.2_

  - [ ] 3.2 Update vercel.json configuration
    - Open existing `vercel.json` file
    - Add or verify `buildCommand` in builds section: `cd frontend && npm install && npm run build`
    - Verify routes configuration priority:
      1. `/api/*` routes to `api/index.py` (already exists)
      2. `/assets/*` routes to `frontend/dist/assets/*` (already exists)
      3. Filesystem handler for direct access (already exists)
      4. Catch-all `(.*)` to `frontend/dist/index.html` (already exists)
    - Optionally add `env` section documenting required environment variables
    - Validate JSON syntax
    - _Bug_Condition: isBugCondition(action) where action involves frontend build or API routing_
    - _Expected_Behavior: Frontend builds automatically, API routes correctly (from design)_
    - _Preservation: No changes to local Vite config or API behavior_
    - _Requirements: 1.3, 2.3_

  - [ ] 3.3 Verify frontend API client configuration
    - Open `frontend/src` directory and locate API client code
    - Check if API calls use relative paths (`/api/problems`) or absolute paths (`http://localhost:8000/api/problems`)
    - **IF using relative paths**: No changes needed - vercel.json routing will handle it
    - **IF using absolute localhost URLs**: 
      - Add environment detection: use relative `/api` in production
      - Use `import.meta.env.PROD` or `window.location.origin` to detect environment
      - Ensure development mode still uses Vite proxy (no changes to vite.config.js)
    - Test that API base URL logic is correct for both environments
    - _Bug_Condition: isBugCondition(action) where action == "FRONTEND_API_CALL" in production_
    - _Expected_Behavior: API calls route to backend serverless function via /api (from design)_
    - _Preservation: Local dev server continues using Vite proxy to localhost:8000_
    - _Requirements: 1.3, 2.3, 3.2_

  - [ ] 3.4 Create .vercelignore file
    - Create `.vercelignore` file in project root
    - Add Python virtual environments: `.venv`, `.venv-1`, `venv/`, `env/`
    - Add Node.js modules: `node_modules/`, `frontend/node_modules/`
    - Add Git directory: `.git/`
    - Add Python cache: `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`
    - Add environment files: `.env` (secrets should be in Vercel dashboard)
    - Add development artifacts: `*.log`, `.DS_Store`, `Thumbs.db`
    - Ensure `frontend/dist/` is NOT ignored (needed for production)
    - _Bug_Condition: Not directly tied to bug condition, but improves deployment_
    - _Expected_Behavior: Cleaner, faster deployments with smaller bundle size_
    - _Preservation: No effect on local development_
    - _Requirements: (Optimization, not explicitly required but recommended)_

  - [ ] 3.5 Update README.md with production URL
    - Open `README.md`
    - Add production URL section near the top (after title/description)
    - Add badge or prominent link: `🌐 **Live Site**: https://bharat-problem-base.vercel.app` (or actual URL)
    - Alternative: Use placeholder `🌐 **Live Site**: [Deploying - check back soon]` until first deployment
    - Add new "Deployment" section explaining:
      - Automatic deployment via GitHub Actions on push to main
      - How to set up required GitHub secrets
      - Link to Vercel dashboard for environment variables
    - Update "Development" section to clarify local vs production environments
    - Keep all existing local development instructions unchanged
    - _Bug_Condition: isBugCondition(action) where action == "VIEW_README" AND NOT productionURLShown()_
    - _Expected_Behavior: README displays working production URL prominently (from design)_
    - _Preservation: All local development documentation remains unchanged_
    - _Requirements: 1.4, 2.4, 2.5_

  - [ ] 3.6 Verify api/index.py serverless function
    - Open `api/index.py`
    - Verify it imports `from app.main import app`
    - Verify it exports `app` for Vercel's Python runtime
    - **NO CHANGES EXPECTED** - current structure is correct for Vercel
    - If deployment fails, check that `app.main:app` is the correct FastAPI instance
    - _Bug_Condition: API routing must work in Vercel environment_
    - _Expected_Behavior: Backend serverless function serves API correctly_
    - _Preservation: No changes to local API serving via uvicorn_
    - _Requirements: 2.3, 3.4_

  - [ ] 3.7 Verify app/main.py Vercel environment detection
    - Open `app/main.py`
    - Verify `IS_VERCEL = os.environ.get("VERCEL") == "1"` exists
    - Verify static file serving is disabled when `IS_VERCEL` is True
    - Verify CORS configuration allows frontend origin
    - **NO CHANGES EXPECTED** - current logic is correct
    - If needed, tighten CORS to specific production domain (optional security improvement)
    - _Bug_Condition: Backend must adapt to Vercel serverless environment_
    - _Expected_Behavior: Backend detects Vercel and adjusts behavior appropriately_
    - _Preservation: Local development uses full uvicorn with static serving_
    - _Requirements: 2.3, 3.1, 3.4_

  - [ ] 3.8 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - Deployment Infrastructure Complete
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the deployment infrastructure is complete
    - Run: `python scripts/test_deployment_infrastructure.py`
    - **EXPECTED OUTCOME**: Test PASSES with all checks successful:
      - "PASS: GitHub Actions workflow found at .github/workflows/deploy.yml"
      - "PASS: Workflow contains required build and deploy steps"
      - "PASS: vercel.json contains proper configuration"
      - "PASS: .vercelignore file exists with correct patterns"
      - "PASS: README.md contains production URL section"
    - If any checks fail, return to relevant implementation subtask and fix
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ] 3.9 Verify preservation tests still pass
    - **Property 2: Preservation** - Local Development Unchanged
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run: `python scripts/test_local_preservation.py`
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions in local development)
      - "PASS: Backend starts on http://localhost:8000"
      - "PASS: Frontend dev server proxies API calls correctly"
      - "PASS: Frontend build generates dist/ with index.html"
      - "PASS: API endpoints return expected responses"
      - "PASS: Database operations function correctly"
    - If any tests fail, identify what changed and restore original behavior
    - Confirm all local development workflows work identically to before the fix
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ] 4. Test automated deployment end-to-end

  - [ ] 4.1 Commit and push changes to trigger GitHub Actions
    - Stage all changes: workflow, vercel.json, .vercelignore, README
    - Create commit: `git commit -m "Add automated Vercel deployment pipeline"`
    - Push to main branch: `git push origin main`
    - Observe GitHub Actions tab for workflow trigger
    - _Requirements: 2.2_

  - [ ] 4.2 Monitor GitHub Actions workflow execution
    - Open repository's GitHub Actions tab
    - Verify workflow "Deploy to Vercel" is running
    - Monitor build logs for frontend build step
    - Monitor logs for Vercel deployment step
    - Verify workflow completes successfully (green checkmark)
    - If workflow fails, check logs for errors and fix configuration
    - _Requirements: 2.2_

  - [ ] 4.3 Verify production deployment is accessible
    - Get deployment URL from GitHub Actions logs or Vercel dashboard
    - Visit production URL in browser
    - Verify site loads with correct styling and assets
    - Verify homepage displays problems list
    - Verify navigation works (search, filters, pagination)
    - Check browser DevTools Network tab for API calls
    - _Requirements: 2.1, 2.3_

  - [ ] 4.4 Test production API endpoints
    - From production site, test main API endpoints:
      - GET `/api/problems` - should return problems list
      - GET `/api/problems/stats` - should return statistics
      - GET `/api/health` - should return health check
    - Verify responses are correct and match local behavior
    - Test search and filter functionality
    - Test pagination controls
    - If API calls fail, check Vercel function logs and API routing configuration
    - _Requirements: 2.3, 3.4_

  - [ ] 4.5 Update README with actual production URL
    - After successful deployment, get final production URL
    - Update README.md with actual URL (replace placeholder if used)
    - Update GitHub repository About section with website URL
    - Commit and push: `git commit -m "Update README with production URL"`
    - _Requirements: 2.4, 2.5_

- [ ] 5. Checkpoint - Ensure all tests pass
  - Verify all implementation subtasks are complete
  - Re-run bug condition test: `python scripts/test_deployment_infrastructure.py` - should PASS
  - Re-run preservation tests: `python scripts/test_local_preservation.py` - should PASS
  - Verify production site is accessible and functional
  - Verify local development still works:
    - Start backend: `uvicorn app.main:app --reload`
    - Start frontend: `cd frontend && npm run dev`
    - Test API calls locally
  - Document any issues or questions for user review
  - Mark complete when all validations pass

---

## Notes

- **GitHub Secrets Required**: Before workflow can succeed, set these secrets in GitHub repository settings:
  - `VERCEL_TOKEN`: Get from Vercel dashboard → Settings → Tokens
  - `VERCEL_ORG_ID`: Get from Vercel project settings or `.vercel/project.json` after manual deploy
  - `VERCEL_PROJECT_ID`: Get from Vercel project settings or `.vercel/project.json` after manual deploy

- **Vercel Environment Variables**: Set these in Vercel dashboard if needed:
  - Database connection strings (if using external database)
  - API keys for external services
  - Email service credentials

- **Testing Strategy**: This plan follows the bug condition methodology:
  1. **Exploration (Task 1)**: Write test that fails on unfixed code, demonstrating the bug
  2. **Preservation (Task 2)**: Write tests that pass on unfixed code, capturing behavior to preserve
  3. **Implementation (Task 3)**: Apply the fix with specification references
  4. **Validation (Task 3.8-3.9)**: Verify exploration test now passes, preservation tests still pass
  5. **End-to-End (Task 4)**: Test the complete deployment pipeline in production

- **Troubleshooting**: If deployment fails, refer to design.md "Troubleshooting Guide" section for common issues and solutions
