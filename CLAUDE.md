# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based file metadata management web application (not Django as the folder name suggests). The app allows users to upload files, manage metadata using Dublin Core standards, and provides both public browsing and admin functionality.

## Core Architecture

- **Backend**: Flask 3.0 with SQLAlchemy ORM
- **Database**: SQLite for lightweight storage
- **Frontend**: Bootstrap 5.3 with custom CSS/JavaScript
- **File Storage**: Local filesystem with organized uploads directory
- **Metadata Standard**: Dublin Core for structured metadata

### Key Files Structure

- `app.py` - Main Flask application with routes and business logic
- `database.py` - SQLAlchemy models (File, ActivityLog) and database initialization
- `wsgi.py` - Production WSGI configuration with extensive error handling
- `wsgi_simple.py` - Simplified WSGI for Docker deployments
- `requirements.txt` - Python dependencies
- `templates/` - Jinja2 templates for all pages
- `static/` - CSS, JavaScript, and other static assets
- `uploads/` - User-uploaded files (not in git)

## Common Commands

### Development Setup
```bash
# Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies  
pip install -r requirements.txt

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Run development server
python app.py
# OR
flask run
```

### Environment Variables
Configure these in `.env` file or system environment:
- `SECRET_KEY` - Flask secret key (required for security)
- `ADMIN_USERNAME` - Admin login username (default: admin)
- `ADMIN_PASSWORD` - Admin password (default: adminpass123!)
- `DATABASE_URL` - Database connection (default: sqlite:///metadatos.db)
- `UPLOAD_FOLDER` - File upload directory (default: uploads)

### Security Dependencies
Install additional security packages:
```bash
pip install Flask-WTF Flask-Limiter bleach
```

### Docker Commands
```bash
# Build and run with Podman/Docker
podman build -t metadatos-app .
podman run -d -p 5000:5000 --name metadatos-app metadatos-app

# Using docker-compose
podman-compose up -d
```

### Debugging
```bash
# Enable debug mode
export FLASK_DEBUG=True
flask run

# View logs
tail -f app.log

# Check configuration
python -c "from app import app; print(app.config)"
```

## Database Models

### File Model
- Stores file metadata with Dublin Core fields
- Includes file size, upload date, and type classification
- Properties for determining file type (image, document, media)
- Search functionality across title, description, and subject fields

### ActivityLog Model  
- Tracks admin actions (upload, delete, login, logout)
- Includes IP address and user agent for security auditing

## Key Features

- **File Upload**: Secure file handling with type validation and size limits
- **Dublin Core Metadata**: Standard metadata fields for better organization
- **Search**: Full-text search across file metadata
- **Admin Panel**: Protected admin interface for file management
- **Responsive UI**: Bootstrap-based responsive design
- **Error Handling**: Custom 404/500 pages and graceful error recovery
- **Security**: XSS protection, secure filename handling, password hashing

## Deployment Configurations

### PythonAnywhere
- Uses `wsgi.py` with comprehensive error handling
- Configured for production environment variables
- Includes security headers and logging

### Docker/Podman
- Uses `wsgi_simple.py` for streamlined container deployment
- Health check endpoint at `/health`
- Persistent volumes for data, uploads, and logs

## File Type Support

Supports common file types including documents (PDF, DOC, etc.), images (JPG, PNG, etc.), media files (MP3, MP4, etc.), and archives (ZIP, RAR, etc.). File type icons are automatically assigned based on extension.

## Security Considerations

### Enhanced Security Implementation

**Authentication & Session Management:**
- Admin authentication with rate limiting (5 attempts per minute)
- Secure session configuration with HttpOnly and SameSite cookies
- Session expiration after 2 hours for security
- Detailed logging of all authentication events with IP addresses

**CSRF Protection:**
- Flask-WTF forms with CSRF tokens for all POST requests
- Automatic token validation on form submissions
- Hidden CSRF fields in all forms

**Input Validation & Sanitization:**
- Bleach library for HTML sanitization to prevent XSS
- WTForms validators for all user inputs
- Safe filename validation to prevent path traversal attacks
- Input length limits and content sanitization

**File Upload Security:**
- Werkzeug secure_filename() for safe file names
- File type validation with whitelist approach
- File size limits (16MB default)
- Dangerous filename pattern detection
- Original filename preservation with safe storage names

**Security Headers:**
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Content-Security-Policy with strict directives
- Strict-Transport-Security for HTTPS
- Referrer-Policy: strict-origin-when-cross-origin

**Rate Limiting:**
- Flask-Limiter for API endpoints
- Login attempts limited to 5 per minute
- File upload limited to 10 per minute
- File deletion limited to 5 per minute

**Logging & Monitoring:**
- Comprehensive security event logging
- IP address tracking for all admin actions
- User agent logging for security analysis
- File integrity verification functions
- Detailed error logging with context

**Password Security:**
- Werkzeug password hashing (PBKDF2)
- Secure password storage
- No plaintext password logging