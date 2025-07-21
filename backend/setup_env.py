#!/usr/bin/env python3
"""
Setup script to create environment files for the Practice Pitch backend.
Run this script to set up your local development environment.
"""

import os

def create_env_file(filename, content):
    """Create an environment file with the given content."""
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Created {filename}")

def main():
    # Local environment file
    local_env_content = """# Local Development Environment
ENVIRONMENT=local
DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///./local.db

# Email Settings (console output for development)
EMAIL_BACKEND=console
SMTP_HOST=localhost
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
FROM_EMAIL=noreply@practicepitch.local

# Zoom API (get these from Zoom Marketplace)
ZOOM_API_KEY=your_zoom_api_key
ZOOM_API_SECRET=your_zoom_api_secret

# Security
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_HOSTS=*
"""

    # Production environment file template
    prod_env_content = """# Production Environment
ENVIRONMENT=production
DEBUG=False

# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/practicepitch_prod

# Email Settings (SMTP for production)
EMAIL_BACKEND=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=hello@practicepitch.com

# Zoom API (production credentials)
ZOOM_API_KEY=your_production_zoom_api_key
ZOOM_API_SECRET=your_production_zoom_api_secret

# Security (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=your_super_secret_key_here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
"""

    # Create the files
    if not os.path.exists('.env.local'):
        create_env_file('.env.local', local_env_content)
    else:
        print(".env.local already exists, skipping...")

    if not os.path.exists('.env.production'):
        create_env_file('.env.production', prod_env_content)
    else:
        print(".env.production already exists, skipping...")

    print("\nSetup complete! Your environment files are ready.")
    print("\nNext steps:")
    print("1. Review and update .env.local with your actual credentials")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the server: python app.py")

if __name__ == "__main__":
    main() 