#!/usr/bin/env python3
"""
TalkVibe Backend Startup Script
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import init_db
from app.services.translation_service import TranslationService
from app.core.database import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def initialize_database():
    """Initialize database tables and seed data."""
    try:
        logger.info("Initializing database...")
        await init_db()
        logger.info("Database tables created successfully")
        
        # Seed default translations
        async with AsyncSessionLocal() as db:
            logger.info("Seeding default translations...")
            count = await TranslationService.seed_default_translations(db)
            logger.info(f"Seeded {count} default translations")
        
        logger.info("Database initialization completed")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def main():
    """Main startup function."""
    try:
        await initialize_database()
        logger.info("TalkVibe backend is ready to start!")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
