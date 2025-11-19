# Personal Job Card Website

A professional personal portfolio/job card website built with FastAPI and Jinja2 templates, designed to run at [dev.magallan.online](https://dev.magallan.online)

## Features

- 🌐 Bilingual support (English/Russian) with auto-detection
- 🎨 Modern, responsive design with dark mode support
- ⚡ FastAPI backend
- 🐳 Docker containerized for easy deployment
- 🔧 Easy customization through JSON translation files
- 📊 Displays skills, experience, education, and projects

## Project Structure

```
magallan.online-server/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose setup
├── translations/          # Translation files
│   ├── en.json           # English translations
│   └── ru.json           # Russian translations
├── templates/
│   ├── layout.html        # Base template with navbar
│   ├── index.html         # Original Minecraft server page
│   └── job_card.html      # Job card page
└── static/
    ├── css/
    │   ├── styles.css     # Custom styles
    │   └── theme.css      # Theme and dark mode styles
    └── images/
```

## API Endpoints

- `GET /` - Main portfolio page
- `GET /api/profile` - JSON API endpoint returning profile data
- `GET /health` - Health check endpoint
