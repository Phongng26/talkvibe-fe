-- TalkVibe Database Initialization Script
-- This script sets up the initial database structure and data

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for better performance
-- These will be created by SQLAlchemy, but we can add custom ones here

-- Example: Create a GIN index for full-text search on room topics
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_rooms_topic_gin 
-- ON rooms USING gin(to_tsvector('english', topic));

-- Example: Create a GIN index for array operations on participant_ids
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_rooms_participants_gin 
-- ON rooms USING gin(participant_ids);

-- Insert default translations (will be handled by the application)
-- This is just a placeholder for any custom SQL setup

-- Grant permissions (if needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO talkvibe;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO talkvibe;
