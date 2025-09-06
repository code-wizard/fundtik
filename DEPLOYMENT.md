# Docker Deployment Guide for Fundtik

This guide provides detailed instructions for deploying Fundtik using Docker and Docker Compose.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Configuration](#configuration)
- [Production Deployment](#production-deployment)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying Fundtik, ensure you have the following installed:

- **Docker**: Version 20.10 or later
- **Docker Compose**: Version 2.0 or later
- **Git**: For cloning the repository
- **At least 2GB RAM**: Recommended for running containers

### Installation Commands

**macOS:**
```bash
# Install Docker Desktop
brew install --cask docker

# Install Docker Compose (usually included with Docker Desktop)
```

**Ubuntu/Debian:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Quick Start

For a basic deployment with default settings:

```bash
git clone https://github.com/code-wizard/fundtik.git
cd fundtik
docker-compose up --build
```

Visit http://localhost:8000 to access the application.

## Detailed Setup

### 1. Clone the Repository

```bash
git clone https://github.com/code-wizard/fundtik.git
cd fundtik
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
# Application Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Settings
DATABASE_URL=postgresql://fundtik:secure_password@db:5432/fundtik

# Optional: Email Settings (for production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Build and Start Containers

```bash
# Build and start in foreground
docker-compose up --build

# Or start in background
docker-compose up -d --build
```

### 4. Verify Deployment

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs web

# Access the application
curl http://localhost:8000
```

## Configuration

### Docker Compose Configuration

The `docker-compose.yml` file includes:

- **Web Service**: Django application with Daphne ASGI server
- **Database Service**: PostgreSQL database
- **Volumes**: Persistent data storage
- **Networks**: Isolated container networking

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable/disable debug mode | `False` |
| `SECRET_KEY` | Django secret key | Random string |
| `ALLOWED_HOSTS` | Comma-separated host list | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection URL | PostgreSQL config |

### Database Configuration

The application uses PostgreSQL in Docker deployment:

- **Database Name**: `fundtik`
- **Username**: `fundtik`
- **Password**: `password` (change in production)
- **Host**: `db` (container name)
- **Port**: `5432`

## Production Deployment

### Security Considerations

1. **Change Default Credentials:**
   ```yaml
   environment:
     - SECRET_KEY=your-actual-secret-key
     - DATABASE_URL=postgresql://fundtik:strong_password@db:5432/fundtik
   ```

2. **Configure HTTPS:**
   - Use a reverse proxy (nginx) for SSL termination
   - Set `SECURE_SSL_REDIRECT = True` in Django settings

3. **Database Security:**
   - Use strong passwords
   - Restrict database access
   - Regular backups

### Scaling

For high-traffic deployments:

```yaml
services:
  web:
    scale: 3  # Run 3 instances
    # Add load balancer configuration
```

### Monitoring

```bash
# Monitor container resources
docker stats

# Check application health
curl http://localhost:8000/health/

# View real-time logs
docker-compose logs -f web
```

## Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin master

# Rebuild and restart
docker-compose up --build -d

# Clean up old images
docker image prune -f
```

### Database Backup

```bash
# Backup database
docker-compose exec db pg_dump -U fundtik fundtik > backup.sql

# Restore database
docker-compose exec -T db psql -U fundtik fundtik < backup.sql
```

### Log Management

```bash
# View application logs
docker-compose logs web

# Follow logs in real-time
docker-compose logs -f web

# Export logs
docker-compose logs web > app_logs.txt
```

## Troubleshooting

### Common Issues

**1. Port Already in Use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"
```

**2. Database Connection Failed:**
```bash
# Check database container
docker-compose logs db

# Restart database
docker-compose restart db
```

**3. Static Files Not Loading:**
- Ensure WhiteNoise is properly configured
- Check `DEBUG` setting
- Verify static files were collected

**4. Memory Issues:**
```bash
# Increase Docker memory allocation
# Docker Desktop: Preferences > Resources > Memory
```

**5. Permission Errors:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Getting Help

- Check container logs: `docker-compose logs`
- Verify environment variables
- Ensure all prerequisites are met
- Test with local development setup first

### Performance Optimization

- Use production database settings
- Enable Django caching
- Configure proper logging levels
- Monitor resource usage
- Implement database indexing

---

For additional support, please check the main README.md or create an issue in the repository.
