"""
Validation utilities for TalkVibe application.
"""
import re
import html
from typing import Optional
from email_validator import validate_email as email_validate, EmailNotValidError


def validate_email(email: str) -> bool:
    """Validate email address format."""
    try:
        email_validate(email)
        return True
    except EmailNotValidError:
        return False


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password cannot exceed 128 characters"
    
    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for at least one digit
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    
    # Check for at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, None


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS attacks."""
    if not text:
        return ""
    
    # HTML escape
    sanitized = html.escape(text)
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', sanitized)
    
    return sanitized.strip()


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """
    Validate username format.
    Returns (is_valid, error_message).
    """
    if not username:
        return False, "Username cannot be empty"
    
    if len(username) < 2:
        return False, "Username must be at least 2 characters long"
    
    if len(username) > 50:
        return False, "Username cannot exceed 50 characters"
    
    # Allow letters, numbers, underscores, and hyphens
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    
    return True, None


def validate_room_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate room name format.
    Returns (is_valid, error_message).
    """
    if not name:
        return False, "Room name cannot be empty"
    
    if len(name.strip()) < 3:
        return False, "Room name must be at least 3 characters long"
    
    if len(name) > 100:
        return False, "Room name cannot exceed 100 characters"
    
    # Check for inappropriate content (basic check)
    inappropriate_words = ["spam", "test123", "admin", "moderator"]
    if any(word in name.lower() for word in inappropriate_words):
        return False, "Room name contains inappropriate content"
    
    return True, None


def validate_file_upload(filename: str, file_size: int, content_type: str) -> tuple[bool, Optional[str]]:
    """
    Validate file upload parameters.
    Returns (is_valid, error_message).
    """
    # Check file size (10MB limit)
    max_size = 10 * 1024 * 1024
    if file_size > max_size:
        return False, f"File size cannot exceed {max_size // (1024 * 1024)}MB"
    
    # Check filename
    if not filename or len(filename) > 255:
        return False, "Invalid filename"
    
    # Check for dangerous file extensions
    dangerous_extensions = ['.exe', '.bat', '.cmd', '.scr', '.pif', '.com', '.js', '.vbs']
    if any(filename.lower().endswith(ext) for ext in dangerous_extensions):
        return False, "File type not allowed"
    
    # Check content type
    allowed_types = [
        'image/jpeg', 'image/png', 'image/gif', 'image/webp',
        'application/pdf', 'text/plain', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    
    if content_type not in allowed_types:
        return False, "File type not supported"
    
    return True, None


def clean_search_query(query: str) -> str:
    """Clean and sanitize search query."""
    if not query:
        return ""
    
    # Remove special characters that could be used for injection
    cleaned = re.sub(r'[^\w\s-]', '', query)
    
    # Limit length
    cleaned = cleaned[:100]
    
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    
    return cleaned
