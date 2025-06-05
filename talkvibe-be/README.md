# TalkVibe Backend

TalkVibe is a community platform for English learners to practice speaking together through real-time video/audio rooms and text chat.

## Features

- **User Management**: Registration, authentication, profile management with JWT and OAuth
- **Practice Rooms**: Create/join video/audio rooms with WebRTC integration
- **Real-time Chat**: WebSocket-based messaging in rooms
- **Notifications**: Firebase Cloud Messaging (FCM) for push notifications
- **Session Tracking**: Practice history and statistics
- **Search & Recommendations**: Find users and rooms based on preferences
- **Multilingual Support**: Translation system for multiple languages

## Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with OAuth2 (Google/Facebook)
- **Real-time**: WebRTC (aiortc) + WebSockets
- **Notifications**: Firebase Cloud Messaging
- **Caching**: Redis
- **Rate Limiting**: SlowAPI

## Project Structure

```
talkvibe-be/
├── app/
│   ├── core/           # Core configuration and database
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic schemas for validation
│   ├── routers/        # API route definitions
│   ├── services/       # Business logic layer
│   ├── utils/          # Utility functions
│   └── main.py         # FastAPI application
├── tests/              # Unit tests
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis (optional, for caching)

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd talkvibe-be

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (generate with `openssl rand -hex 32`)
- `SUPABASE_URL` & `SUPABASE_KEY`: If using Supabase
- `FIREBASE_CREDENTIALS_PATH`: Path to Firebase service account JSON
- `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET`: For OAuth
- `REDIS_URL`: Redis connection string

### 4. Database Setup

```bash
# Run database migrations (if using Alembic)
alembic upgrade head

# Or create tables directly
python -c "
from app.core.database import init_db
import asyncio
asyncio.run(init_db())
"
```

### 5. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login with email/password
- `POST /api/users/logout` - Logout user
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `GET /api/users/search` - Search users

### Rooms
- `POST /api/rooms/create` - Create practice room
- `GET /api/rooms` - List rooms with filters
- `GET /api/rooms/{id}` - Get room details
- `PUT /api/rooms/{id}` - Update room details
- `DELETE /api/rooms/{id}` - Delete room
- `POST /api/rooms/{id}/join` - Join room
- `POST /api/rooms/{id}/leave` - Leave room
- `GET /api/rooms/search` - Search rooms

### Chat
- `POST /api/chats` - Send message
- `GET /api/chats/{roomId}` - Get room messages
- `PUT /api/chats/{messageId}` - Edit message
- `DELETE /api/chats/{messageId}` - Delete message
- `WS /ws/chat/{roomId}` - WebSocket chat connection

### Notifications
- `GET /api/notifications` - Get user notifications
- `POST /api/notifications/mark-read` - Mark as read
- `GET /api/notifications/unread-count` - Get unread count

### Sessions
- `GET /api/sessions` - Get practice history
- `GET /api/sessions/stats` - Get practice statistics

### Translations
- `GET /api/content/{language}` - Get content by language
- `GET /api/content/languages` - Get available languages

### WebSocket
- `WS /ws/chat/{roomId}?token={jwt}` - Real-time chat
- Supports: chat messages, typing indicators, WebRTC signaling

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_users.py
```

## Deployment

### Using Docker

```bash
# Build and run with Docker Compose (recommended)
docker-compose up -d

# Or build image manually
docker build -t talkvibe-backend .

# Run container
docker run -p 8000:8000 --env-file .env talkvibe-backend
```

### Quick Start with Docker Compose

```bash
# Clone repository
git clone <repository-url>
cd talkvibe-be

# Start all services (API, PostgreSQL, Redis, pgAdmin)
docker-compose up -d

# Initialize database
python start.py

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

Services will be available at:
- **API**: http://localhost:8000
- **Database**: localhost:5432
- **Redis**: localhost:6379
- **pgAdmin**: http://localhost:5050 (admin@talkvibe.com / admin)

### Using Render/Heroku

1. Set environment variables in platform dashboard
2. Deploy from Git repository
3. Ensure database is provisioned and accessible

### Environment Variables for Production

```bash
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=your-super-secret-key
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
