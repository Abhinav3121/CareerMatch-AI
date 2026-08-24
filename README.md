# CareerMatch AI

AI-powered resume analysis and job matching platform built with FastAPI, React, and PostgreSQL.

## Overview

CareerMatch AI helps users analyze resumes, manage job opportunities, and compare resume skills with job requirements. The application provides user authentication, resume upload and text extraction, resume analysis, job management, recommendations, and match-history tracking.

The project is designed as a full-stack career assistance platform with a Python/FastAPI backend and a React/Vite frontend.

## Features

- User registration and login
- JWT-based authentication
- Secure password hashing
- Protected user endpoints
- Resume upload for PDF and DOCX files
- Resume text extraction
- Resume analysis and scoring
- Job creation and management
- Resume-to-job skill matching
- Matched and missing skill identification
- Job recommendations
- Match history
- PostgreSQL database persistence
- React frontend with Axios API integration
- Configurable backend CORS origins
- Environment-based API configuration
- Backend unit tests for models, schemas, and security

## Technology Stack

### Backend

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- PyJWT
- pwdlib
- PyMuPDF
- python-docx
- Uvicorn

### Frontend

- React
- Vite
- Axios
- JavaScript
- CSS

## Project Structure

```text
CareerMatch-AI/
├── backend/
│   ├── app/
│   │   ├── api/          # API route handlers
│   │   ├── core/         # Configuration and authentication
│   │   ├── models/       # SQLAlchemy database models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   └── services/     # Resume processing and matching logic
│   ├── tests/            # Backend unit tests
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/        # Application pages
│   │   └── services/     # API client
│   └── .env.example
├── LICENSE
└── README.md
