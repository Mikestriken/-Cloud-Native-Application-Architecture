"""
LLM integration with Google's Gemini API for resume-job matching
"""
import os
import asyncio
import google.generativeai as genai
from sqlalchemy.orm import Session
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from app.models import Job, Match

# Configure Gemini API with key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
model = genai.GenerativeModel('gemini-1.5-flash')

async def compute_resume_job_match(resume_text, job_description):
    """
    Use Gemini to compute the match between a resume and job description
    Returns a relevance score between 0.0 and 1.0
    """
    logger.debug(f"Resume length: {len(resume_text)} characters")
    logger.debug(f"Job description length: {len(job_description)} characters")
    
    prompt = f"""
    You are an AI talent matcher analyzing the fit between a resume and a job description.
    Evaluate how well this candidate's resume matches the job requirements.
    
    Resume:
    ```
    {resume_text}
    ```
    
    Job Description:
    ```
    {job_description}
    ```
    
    Rate the match on a scale from 0.0 to 1.0, where:
    - 0.0 means no relevant skills or experience
    - 0.5 means somewhat qualified with some matching skills
    - 1.0 means perfect match with all required skills and experience
    
    Return only a single number representing the match score.
    """
    
    try:
        # Using asyncio to run synchronous Gemini API call in async context
        response = await asyncio.to_thread(
            model.generate_content,
            prompt
        )
        
        score_text = response.text.strip()
        # logger.info(f"Received response from Gemini API: '{score_text}'")
        
        # Extract numeric value from response
        try:
            score = float(score_text)
            # Ensure score is within valid range
            final_score = max(0.0, min(score, 1.0))
            # logger.info(f"Parsed match score: {final_score}")
            return final_score
        except ValueError:
            # Fallback if we can't parse the score
            logger.error(f"Failed to parse score from LLM response: '{score_text}'")
            logger.warning("Using default score of 0.5")
            return 0.5
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}", exc_info=True)
        # Return a default score if API call fails
        logger.warning("Using default score of 0.5 due to API error")
        return 0.5

async def match_resume_with_jobs(resume_text, resume_id, db: Session):
    """
    Match a resume with all jobs in the database
    Save the matches in the database directly and return confirmation
    """
    logger.info(f"Starting to match resume ID {resume_id} with jobs")
    
    # First, clear any existing matches for this resume
    logger.info(f"Clearing existing matches for resume ID {resume_id}")
    existing_matches = db.query(Match).filter(Match.resume_id == resume_id).all()
    if existing_matches:
        logger.info(f"Found {len(existing_matches)} existing matches to remove")
        for match in existing_matches:
            db.delete(match)
        db.commit()
        logger.info("Existing matches cleared successfully")
    
    # Get all jobs to match against
    jobs = db.query(Job).all()
    logger.info(f"Found {len(jobs)} jobs to compare against resume")
    
    match_count = 0
    
    # Process jobs in batches to avoid rate limits
    BATCH_SIZE = 3
    
    for i in range(0, len(jobs), BATCH_SIZE):
        current_batch_of_jobs = jobs[i:i+BATCH_SIZE]
        logger.info(f"Processing batch {i//BATCH_SIZE + 1}, jobs {i+1}-{min(i+BATCH_SIZE, len(jobs))}")
        
        tasks = [compute_resume_job_match(resume_text, job.description) for job in current_batch_of_jobs]
        current_batch_of_scores = await asyncio.gather(*tasks)
        
        # Add each match to the database
        for job, score in zip(current_batch_of_jobs, current_batch_of_scores):
            logger.info(f"Match score for job {job.id} ({job.title}): {score}")
            
            # Create and add the match to the database
            match = Match(
                resume_id=resume_id,
                job_id=job.id,
                score=score
            )
            db.add(match)
            match_count += 1
        
        # Commit after each batch to avoid large transactions
        db.commit()
        logger.info(f"Committed batch {i//BATCH_SIZE + 1} of matches to database")
    
    logger.info(f"Completed matching. Added {match_count} matches to database for resume ID {resume_id}")
    
    # Return the top 5 matches for immediate use
    top_matches = db.query(Match).filter(Match.resume_id == resume_id).order_by(Match.score.desc()).limit(5).all()
    logger.info(f"Retrieved top {len(top_matches)} matches for response")
    
    return top_matches 