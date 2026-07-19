# Vercel Deployment Fix Design

## Overview

The BharatProblemBase project is not properly deployed to Vercel, and there is no automated CI/CD pipeline. The deployment infrastructure exists (vercel.json, api/index.py) but is incomplete. This fix will establish a complete GitHub Actions → Vercel deployment pipeline, ensure proper production routing between frontend and backend, and update documentation with the live URL. The fix must preserve all local development workflows unchanged.

## Glossary

- **Bug_Condition (C)**: The condition that triggers the deployment failure - when the GitHub repository link is accessed or when code is pushed without automated deployment
- **Property (P)**: The desired behavior - working production URL, automated deployments, proper API routing
- **Preservation**: Local development setup, API functionality, database operations, and authentication flows that must remain unchanged
- **Vercel Serverless Function**: The Python backend deployed as a serverless function at `api/index.py` that wraps the FastAPI app
- **GitHub Actions Workflow**: Automated CI/CD pipeline that builds and deploys on push to main branch
- **Production API Routing**: How frontend `/api/*` requests are routed to the backend serverless function in Vercel's environment
- **VERCEL Environment Variable**: Boolean flag (`VERCEL=1`) indicating the app is running in Vercel's serverless environment

## Bug Details

### Bug Condition

The bug manifests when users attempt to access the deployed application or when developers push code expecting automated deployment. The deployment system is either missing the GitHub Actions workflow, has incorrect Vercel configuration, lacks production API routing setup, or has outdated documentation.

**Formal Specification:**
```
FUNCTION isBugCondition(input)
  INPUT: input of type DeploymentAction
  OUTPUT: boolean
  
  RETURN (input.action == "ACCESS_REPO_LINK" AND NOT deployedSiteExists())
         OR (input.action == "PUSH_TO_MAIN" AND NOT githubActionsTriggered())
         OR (input.action == "FRONTEND_API_CALL" AND NOT apiRoutingWorks())
         OR (input.action == "VIEW_README" AND NOT productionURLShown())
END FUNCTION
```

### Examples

- **Accessing GitHub Link**: User clicks website link from repository → gets 404 or non-existent URL
- **Pushing Code**: Developer pushes to main branch → no automated build/deploy occurs, manual deployment required
- **Frontend API Call in Production**: Frontend makes `/api/problems` request → fails because no base URL configured for production environment
- **README Documentation**: Developer reads README → sees only localhost:8000 instructions, no production URL

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- Local development workflow with `uvicorn app.main:app` or `start.bat` must continue working at `http://localhost:8000`
- Frontend dev server (`npm run dev`) must continue proxying `/api` to `http://localhost:8000` via Vite config
- Frontend production build (`npm run build`) must continue generating static assets in `frontend/dist`
- All API endpoints (`/api/problems`, `/api/auth/login`, etc.) must maintain identical request/response behavior
- SQLite database operations, seeding, and queries must remain unchanged
- JWT authentication, OTP verification, and security utilities must work identically

**Scope:**
All inputs that do NOT involve production deployment, GitHub Actions, or production API calls should be completely unaffected by this fix. This includes:
- Local development server operations
- Manual frontend builds
- Database migrations and seeding
- Unit tests and local testing
- Environment variable configuration for local setup

## Hypothesized Root Cause

Based on the bug description and code analysis, the most likely issues are:

1. **Missing GitHub Actions Workflow**: No `.github/workflows/deploy.yml` file exists
   - Repository has no automated CI/CD pipeline
   - Pushes to main do not trigger builds or deployments
   - Manual Vercel deployment is required (error-prone, not documented)

2. **Incomplete vercel.json Configuration**: Current config may not handle all routing edge cases
   - Static asset routing is configured but may need optimization
   - API routing to `api/index.py` exists but frontend may not know production API base URL
   - Build settings may be missing (frontend build command not specified in Vercel config)

3. **Missing Production Environment Handling**: Frontend assumes localhost API
   - `vite.config.js` only configures local proxy to `localhost:8000`
   - No environment-based API base URL configuration for production
   - Frontend makes relative `/api` calls that work locally but may fail in production

4. **Outdated Documentation**: README only shows local development
   - No production URL placeholder or instructions
   - No deployment documentation for maintainers
   - GitHub repository "About" section not configured with live URL

5. **Missing .vercelignore**: Build may upload unnecessary files
   - Virtual environments, cache files, or test data may be deployed
   - Increases deployment size and time

## Correctness Properties

Property 1: Bug Condition - Automated Deployment Pipeline

_For any_ code push to the main branch where GitHub Actions workflow exists and Vercel configuration is valid, the fixed deployment system SHALL automatically build the frontend, deploy both frontend and backend to Vercel, and make the application accessible at the production URL.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

Property 2: Preservation - Local Development Workflow

_For any_ local development action (starting uvicorn, running frontend dev server, building frontend, making API calls locally), the fixed code SHALL produce exactly the same behavior as the original code, preserving all local development workflows, API functionality, database operations, and authentication flows.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**

## Hypothesized Root Cause

Based on the bug description and code analysis, the deployment issues stem from:

1. **Missing GitHub Actions Workflow**: No automated CI/CD pipeline exists
2. **Incomplete Vercel Configuration**: vercel.json doesn't specify frontend build command
3. **Missing Production API URL**: Frontend hardcoded to use relative paths without environment awareness
4. **Documentation Gap**: No production URL or deployment instructions
5. **Missing .vercelignore**: Potentially deploying unnecessary files

## Fix Implementation

### Changes Required

Assuming our root cause analysis is correct:

**File 1**: `.github/workflows/deploy.yml` (NEW FILE)

**Purpose**: Automated CI/CD pipeline for Vercel deployment

**Specific Changes**:
1. **Workflow Trigger**: Configure to run on push to `main` branch
   - Use `on: push: branches: [main]` trigger
   - Ensures every main branch update triggers deployment
   
2. **Build Frontend Step**: Install dependencies and build React app
   - Run `npm install` in frontend directory
   - Run `npm run build` to generate production bundle
   - Ensure `frontend/dist` is created before deployment
   
3. **Deploy to Vercel Step**: Use official Vercel action
   - Use `amondnet/vercel-action@v25` or similar
   - Pass `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` as secrets
   - Deploy with `--prod` flag for production deployment
   - Deploy entire project root (includes api/, frontend/dist/, vercel.json)

4. **Environment Secrets**: Document required GitHub secrets
   - `VERCEL_TOKEN`: Personal access token from Vercel
   - `VERCEL_ORG_ID`: Vercel organization ID
   - `VERCEL_PROJECT_ID`: Vercel project ID

**File 2**: `vercel.json`

**Purpose**: Update Vercel configuration with explicit build settings

**Specific Changes**:
1. **Add Build Configuration**: Specify frontend build command
   - Add `"buildCommand": "cd frontend && npm install && npm run build"` to ensure Vercel builds frontend
   - Alternative: Keep builds array but ensure Vercel knows to build frontend
   
2. **Verify Routes Configuration**: Ensure proper routing priority
   - API routes (`/api/*`) should route to `api/index.py` (already configured)
   - Static assets (`/assets/*`) should route to `frontend/dist/assets/*` (already configured)
   - Filesystem handler for direct file access (already configured)
   - Catch-all route (`/(.*)`) to `frontend/dist/index.html` for SPA (already configured)
   
3. **Add Environment Variables Section** (optional): Document required env vars
   - Not strictly necessary (can be set in Vercel dashboard)
   - But helpful for documentation purposes

**File 3**: `frontend/src/api.js` (or wherever API client is defined)

**Purpose**: Make API base URL environment-aware

**Specific Changes**:
1. **Add Environment Detection**: Check if running in production
   - Detect production by checking `window.location.origin` or `import.meta.env.PROD`
   - Use relative `/api` paths (work in both local and Vercel due to vercel.json routing)
   - No changes needed if already using relative paths - Vercel routes will handle it
   
2. **Verify Current Implementation**: Check if API calls use relative or absolute URLs
   - If using `fetch('/api/problems')` → already works, no change needed
   - If using `fetch('http://localhost:8000/api/problems')` → needs environment handling
   
3. **Alternative Approach**: Use Vite environment variables
   - Create `.env.production` with `VITE_API_URL=/api`
   - Update API client to use `import.meta.env.VITE_API_URL`

**File 4**: `.vercelignore` (NEW FILE)

**Purpose**: Exclude unnecessary files from deployment

**Specific Changes**:
1. **Exclude Virtual Environments**: Prevent uploading Python venv
   - Add `.venv`, `.venv-1`, `venv`, `env`
   
2. **Exclude Development Files**: Prevent uploading dev artifacts
   - Add `node_modules`, `.git`, `__pycache__`, `*.pyc`
   - Add `.env` (secrets should be in Vercel dashboard)
   
3. **Exclude Scripts and Docs**: Only deploy runtime code
   - Add `scripts/`, `tests/` if they exist
   - Keep `frontend/dist` (needed for production)

**File 5**: `README.md`

**Purpose**: Update documentation with production URL and deployment instructions

**Specific Changes**:
1. **Add Production URL Section**: Show live site link
   - Add badge or link at top: `🌐 Live Site: https://your-project.vercel.app`
   - Or use placeholder: `🌐 Live Site: [Coming Soon]` until first deployment
   
2. **Add Deployment Section**: Document CI/CD workflow
   - Explain that pushes to main auto-deploy via GitHub Actions
   - Document required GitHub secrets setup
   - Link to Vercel dashboard for environment variables
   
3. **Update Quick Start**: Clarify local vs production
   - Keep existing local development instructions
   - Add section distinguishing local and production environments

**File 6**: `api/index.py` (VERIFY ONLY - likely no changes needed)

**Purpose**: Ensure Vercel serverless function properly wraps FastAPI app

**Verification**:
- Current code `from app.main import app` is correct
- Vercel's `@vercel/python` runtime expects this pattern
- No changes needed unless Vercel deployment fails

**File 7**: `app/main.py` (VERIFY ONLY - likely no changes needed)

**Purpose**: Ensure IS_VERCEL environment detection works correctly

**Verification**:
- `IS_VERCEL = os.environ.get("VERCEL") == "1"` is correct (Vercel sets this automatically)
- Static file serving is disabled in Vercel mode (correct - Vercel handles static files)
- CORS is wide open (`allow_origins=["*"]`) - acceptable for public API, consider tightening later
- No changes needed for deployment

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, verify the deployment infrastructure is complete by attempting deployment on unfixed code (will fail), then verify the fix works correctly by confirming automated deployment succeeds and preserving all local development functionality.

### Exploratory Bug Condition Checking

**Goal**: Surface deployment failures BEFORE implementing the fix. Confirm which specific pieces are missing or misconfigured.

**Test Plan**: Attempt to trigger GitHub Actions (will fail - workflow doesn't exist), attempt to deploy manually to Vercel (may fail - config incomplete), test frontend API calls in production (may fail - hardcoded localhost), check README for production URL (will fail - not documented).

**Test Cases**:
1. **GitHub Actions Test**: Push to main branch and check Actions tab (will fail - no workflow file)
2. **Manual Vercel Deploy Test**: Run `vercel --prod` manually (may fail - frontend not built, or may succeed but miss automation)
3. **Production API Test**: Deploy manually and test `/api/problems` from browser (may fail - frontend uses localhost)
4. **Documentation Test**: Check README and repo About section (will fail - no production URL)

**Expected Counterexamples**:
- No GitHub Actions workflow appears after push
- Manual deployment requires explicit frontend build step
- Production frontend shows API errors or CORS issues
- README shows no production URL

### Fix Checking

**Goal**: Verify that for all deployment actions where the bug condition holds, the fixed system produces the expected behavior.

**Pseudocode:**
```
FOR ALL action WHERE isBugCondition(action) DO
  result := performAction_fixed(action)
  ASSERT expectedBehavior(result)
END FOR
```

**Test Cases**:
1. **Automated Deployment Test**: 
   - Push code to main branch
   - Verify GitHub Actions workflow triggers
   - Verify workflow builds frontend successfully
   - Verify workflow deploys to Vercel
   - Verify deployment completes without errors

2. **Production Access Test**:
   - Visit production URL from README
   - Verify site loads with correct styling
   - Verify homepage displays problems list
   - Verify all navigation works

3. **Production API Test**:
   - Open production site
   - Test `/api/problems` endpoint returns data
   - Test `/api/problems/stats` returns statistics
   - Test search and filter functionality

4. **Documentation Test**:
   - Verify README shows correct production URL
   - Verify GitHub repo About section has live site link
   - Verify deployment instructions are clear

### Preservation Checking

**Goal**: Verify that for all local development actions where the bug condition does NOT hold, the fixed system produces the same result as the original system.

**Pseudocode:**
```
FOR ALL action WHERE NOT isBugCondition(action) DO
  ASSERT originalSystem(action) = fixedSystem(action)
END FOR
```

**Testing Approach**: Property-based testing is recommended for preservation checking because:
- It generates many test cases automatically across the local development workflow
- It catches edge cases that manual testing might miss (different Python versions, different terminal environments)
- It provides strong guarantees that local development is unchanged for all scenarios

**Test Plan**: Observe behavior on UNFIXED code first for local development workflows, then verify identical behavior after fix.

**Test Cases**:
1. **Local Server Preservation**: 
   - Run `uvicorn app.main:app --reload` on unfixed code → observe it starts on port 8000
   - Run same command on fixed code → verify identical behavior
   - Test API endpoints locally → verify identical responses

2. **Frontend Dev Server Preservation**:
   - Run `cd frontend && npm run dev` on unfixed code → observe it starts on port 5173 with proxy
   - Run same command on fixed code → verify identical behavior
   - Test that `/api` calls proxy to localhost:8000

3. **Frontend Build Preservation**:
   - Run `cd frontend && npm run build` on unfixed code → observe dist/ creation
   - Run same command on fixed code → verify identical dist/ structure and file hashes

4. **Database Operations Preservation**:
   - Run database seed script on unfixed code → observe data inserted
   - Run same script on fixed code → verify identical data structure and records

5. **Authentication Flow Preservation**:
   - Test signup/login/OTP flows locally on unfixed code → observe behavior
   - Test same flows on fixed code → verify identical JWT tokens and responses

### Unit Tests

- Test that GitHub Actions workflow YAML is valid (syntax check)
- Test that vercel.json is valid JSON with correct structure
- Test that .vercelignore excludes expected patterns (files shouldn't exist in deployment)
- Test that API base URL uses environment-appropriate value

### Property-Based Tests

- Generate random API endpoints and verify they return identical responses locally before and after fix
- Generate random frontend routes and verify they load correctly both locally and in production
- Generate random user interactions (search, filter, pagination) and verify they work identically

### Integration Tests

- Test full deployment pipeline: push to GitHub → Actions run → Vercel deploys → site is accessible
- Test full user journey in production: visit site → search problems → view details → pagination
- Test that local development still works after deployment changes: start server → build frontend → test API → verify all features work

### Manual Verification Checklist

After implementing the fix, manually verify:

- [ ] Push to main triggers GitHub Actions workflow
- [ ] Workflow logs show successful frontend build
- [ ] Workflow logs show successful Vercel deployment
- [ ] Production URL (from Vercel dashboard) loads successfully
- [ ] Frontend displays correctly with all styling
- [ ] API calls from frontend return data (check browser DevTools Network tab)
- [ ] Search, filters, and pagination work in production
- [ ] README displays correct production URL
- [ ] GitHub repo About section has website link
- [ ] Local development still works: `uvicorn app.main:app`
- [ ] Frontend dev server still works: `cd frontend && npm run dev`
- [ ] Frontend build still works: `cd frontend && npm run build`
- [ ] Local API calls still work at `http://localhost:8000/api/problems`

### Troubleshooting Guide

If deployment fails, check:

1. **GitHub Actions Failure**:
   - Verify secrets are set: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`
   - Check workflow logs for specific error messages
   - Verify Node.js and Python versions are compatible

2. **Vercel Build Failure**:
   - Check `vercel.json` syntax is valid JSON
   - Verify frontend build succeeds locally: `cd frontend && npm run build`
   - Check Vercel dashboard build logs

3. **Production API Errors**:
   - Verify `api/index.py` imports `app.main:app` correctly
   - Check Vercel function logs for Python errors
   - Verify environment variables are set in Vercel dashboard

4. **Frontend Routing Issues**:
   - Verify vercel.json routes are in correct priority order
   - Check that `frontend/dist/index.html` exists
   - Test routes manually: visit `https://your-site.vercel.app/api/health`

5. **Local Development Broken**:
   - Verify no changes were made to `app/main.py` local serving logic
   - Verify `vite.config.js` proxy configuration unchanged
   - Check that `IS_VERCEL` environment variable is not set locally
