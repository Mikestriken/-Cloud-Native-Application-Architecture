# Resume Job Matcher

A web application that matches user resumes with job descriptions using LLM-powered semantic matching.

## Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Resume Upload**: Upload resumes in PDF format or paste plain text
- **Job Matching**: Matches resumes with relevant job listings using Google's Gemini LLM
- **Match Ranking**: View top 5 job matches with relevance scores
- **Job Details**: View detailed job descriptions for matched jobs

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: PostgreSQL 
- **ORM**: SQLAlchemy
- **AI API**: Google Gemini API
- **Authentication**: JWT tokens
- **Containerization**: Docker & Docker Compose

## Project Structure

```
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── db.py           # Database connection setup
│   │   ├── llm.py          # Gemini API integration
│   │   ├── models.py       # SQLAlchemy models
│   │   └── schemas.py      # Pydantic schemas
│   ├── main.py             # FastAPI application
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Streamlit frontend
│   ├── app.py              # Streamlit app
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml      # Docker services setup
└── README.md
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Google Gemini API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Setup and Running

1. Clone the repository
   ```
   git clone <repository-url>
   cd resume-job-matcher
   ```

2. Set up environment variables
   - Edit `docker-compose.yml` to add your Gemini API key
   - Change the `SECRET_KEY` for production use

3. Start the application
   ```
   docker-compose up
   ```

4. Access the application
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Usage

1. Register a new account or login with existing credentials
2. Upload your resume (PDF) or paste plain text
3. View your top 5 job matches
4. Click on job titles to view detailed descriptions
5. Refresh matches at any time

## Development

To run the application in development mode:

```
docker-compose up --build
```

The application has hot-reloading enabled for both frontend and backend.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
