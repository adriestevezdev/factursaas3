from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.db.seed import seed_database, cleanup_seed_data, get_seed_stats
from app.middleware.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/seed", tags=["Database Seeding"])

@router.get("/stats")
async def get_seed_statistics():
    """Get statistics about seed data in the database"""
    try:
        stats = get_seed_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting seed stats: {e}")
        raise HTTPException(status_code=500, detail="Error getting seed statistics")

@router.post("/")
async def create_seed_data():
    """
    Create seed data in the database.
    This endpoint does not require authentication as it's for development purposes.
    """
    try:
        result = seed_database()
        return JSONResponse(content=result, status_code=201)
    except Exception as e:
        logger.error(f"Error creating seed data: {e}")
        raise HTTPException(status_code=500, detail="Error creating seed data")

@router.delete("/")
async def delete_seed_data():
    """
    Delete all seed data from the database.
    This endpoint does not require authentication as it's for development purposes.
    """
    try:
        result = cleanup_seed_data()
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Error deleting seed data: {e}")
        raise HTTPException(status_code=500, detail="Error deleting seed data")

@router.post("/reset")
async def reset_seed_data():
    """
    Reset seed data: delete existing seed data and create fresh seed data.
    This endpoint does not require authentication as it's for development purposes.
    """
    try:
        # First cleanup existing seed data
        cleanup_result = cleanup_seed_data()
        logger.info(f"Cleanup result: {cleanup_result}")
        
        # Then create fresh seed data
        seed_result = seed_database()
        logger.info(f"Seed result: {seed_result}")
        
        return JSONResponse(content={
            "message": "Seed data reset successfully",
            "cleanup": cleanup_result,
            "seed": seed_result
        }, status_code=200)
    except Exception as e:
        logger.error(f"Error resetting seed data: {e}")
        raise HTTPException(status_code=500, detail="Error resetting seed data")