# Bugfix Requirements Document

## Introduction

The GitHub repository for BharatProblemBase contains a link to access the deployed website, but this link is not working. The project is a full-stack application (FastAPI backend + React frontend) that needs to be properly deployed to Vercel with automated GitHub Actions workflow. Currently, there is no CI/CD automation in place, and the deployment configuration may not be properly set up for production use.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN a user clicks the website link from the GitHub repository THEN the system fails to navigate to a working deployed website

1.2 WHEN code is pushed to the GitHub repository THEN the system does not automatically trigger deployment to Vercel

1.3 WHEN the frontend build is deployed to Vercel THEN the system may not properly route API requests to the backend endpoint

1.4 WHEN the README is viewed THEN the system displays no valid production deployment URL

### Expected Behavior (Correct)

2.1 WHEN a user clicks the website link from the GitHub repository THEN the system SHALL navigate to a fully functional deployed website on Vercel

2.2 WHEN code is pushed to the main/master branch THEN the system SHALL automatically trigger a GitHub Actions workflow that builds and deploys to Vercel

2.3 WHEN the frontend is deployed to Vercel THEN the system SHALL properly route `/api/*` requests to the backend Vercel serverless function

2.4 WHEN the README is viewed THEN the system SHALL display the correct production deployment URL with a working link

2.5 WHEN the GitHub repository settings are configured THEN the system SHALL include the live site URL in the repository About section

### Unchanged Behavior (Regression Prevention)

3.1 WHEN developers run the application locally using `uvicorn` or `start.bat` THEN the system SHALL CONTINUE TO serve the application at `http://localhost:8000` with proper API proxying

3.2 WHEN the frontend development server runs locally THEN the system SHALL CONTINUE TO proxy `/api` requests to `http://localhost:8000` as configured in `vite.config.js`

3.3 WHEN the frontend is built using `npm run build` THEN the system SHALL CONTINUE TO generate static assets in the `frontend/dist` directory

3.4 WHEN existing API endpoints are called THEN the system SHALL CONTINUE TO return the same responses and behavior

3.5 WHEN the SQLite database is seeded or accessed THEN the system SHALL CONTINUE TO function with the same data structure and queries

3.6 WHEN authentication flows (signup, login, OTP verification) are used THEN the system SHALL CONTINUE TO work with JWT tokens and email verification
