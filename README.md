# Magallan Portfolio - Personal Job Card Website

A professional personal portfolio/job card website built with FastAPI and Jinja2 templates, designed to run at dev.magallan.online.

## Features

- � Bilingual support (English/Russian) with auto-detection
- �🎨 Modern, responsive design with dark mode support
- 📱 Mobile-friendly layout
- ⚡ Fast FastAPI backend
- 🐳 Docker containerized for easy deployment
- 🔧 Easy customization through JSON translation files
- 📊 Displays skills, experience, education, and projects
- 🔗 Social media integration
- 🖼️ Logo-based branding

## Project Structure

```
magallan.online-server/
├── main.py                 # FastAPI application (loads translations)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose setup
├── translations/          # Translation files
│   ├── en.json           # English translations
│   └── ru.json           # Russian translations
├── templates/
│   ├── layout.html        # Base template with navbar
│   ├── index.html         # Original Minecraft server page
│   └── job_card.html      # Portfolio/job card page
└── static/
    ├── css/
    │   ├── styles.css     # Custom styles
    │   └── theme.css      # Theme and dark mode styles
    └── images/
        └── logo.png       # Your logo (place here)
```

## Quick Start

### 1. Add Your Logo

Place your logo as `static/images/logo.png` (see `static/images/README.md` for specifications)

### 2. Customize Your Profile

Edit the translation files:
- `translations/en.json` - English version
- `translations/ru.json` - Russian version

Update profile information, skills, experience, education, and projects in both files.

### 3. Build and Run with Docker

```bash
# Build the Docker image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

The application will be available at `http://localhost:8002`

### 4. Configure Nginx

Add the following location block to your nginx configuration at `/etc/nginx/sites-available/magallan.online`:

```nginx
# Portfolio/Job Card site for dev.magallan.online
location / {
    # First try to serve the dev subdomain
    if ($host = dev.magallan.online) {
        proxy_pass http://localhost:8002;
        break;
    }
    
    # Otherwise serve the main website
    root /var/www/magallan.online;
    index index.html;
    try_files $uri $uri/ =404;
}
```

**Alternative (cleaner) approach** - Create a separate server block for dev.magallan.online:

```nginx
# Dev subdomain - Portfolio site
server {
    listen 443 ssl http2;
    server_name dev.magallan.online;

    # SSL Configuration (same as main domain)
    ssl_certificate /etc/letsencrypt/live/magallan.online-0001/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/magallan.online-0001/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Proxy to portfolio app
    location / {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Reload Nginx

```bash
# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

## Development

### Local Development without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Update Content

With docker-compose volumes mounted, you can edit files locally and they'll be reflected in the container:

- Edit `translations/*.json` to update profile data in English/Russian
- Edit `templates/job_card.html` to customize the layout
- Edit `static/css/styles.css` for custom styling
- Replace `static/images/logo.png` with your logo

After editing translation files or `main.py`, restart the container:
```bash
docker-compose restart
```

## API Endpoints

- `GET /` - Main portfolio page
- `GET /api/profile` - JSON API endpoint returning profile data
- `GET /health` - Health check endpoint

## Customization Tips

### Adding Your Logo

1. Create or prepare your logo (PNG format with transparency recommended)
2. Save as `static/images/logo.png`
3. Recommended size: ~200x60px, displayed at 40px height

### Adding a Profile Photo

1. Add your photo to `static/images/profile.jpg`
2. Uncomment the image tag in `templates/job_card.html`:
   ```html
   <img src="/static/images/profile.jpg" alt="{{ t.profile.name }}" class="profile-photo">
   ```

### Adding a Downloadable CV

1. Add your CV PDF to `static/cv.pdf`
2. Uncomment the download button in `templates/job_card.html`:
   ```html
   <a href="/static/cv.pdf" download class="download-cv">
       <i class="fas fa-download"></i>
       {{ t.download_cv }}
   </a>
   ```

### Updating Translations

Edit JSON files in `translations/`:
- `en.json` - English content
- `ru.json` - Russian content

All text content, skills, experience, education, and projects are stored here.

### Color Scheme

Edit the CSS variables in `templates/job_card.html` to change colors:
```css
:root {
    --primary-color: #5D6B6B;
    --secondary-color: #F7CBCA;
    --grey-accent: #7f8c8d;
}
```

## Troubleshooting

### Container not starting
```bash
# Check logs
docker-compose logs

# Check if port 8002 is already in use
netstat -tuln | grep 8002
```

### Nginx not proxying correctly
```bash
# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify the container is running
docker ps | grep magallan-portfolio
```

### Changes not reflecting
```bash
# Restart the container
docker-compose restart

# Or rebuild if you changed Dockerfile
docker-compose down
docker-compose up -d --build
```

## Security Notes

- The application runs on localhost:8002 and should only be accessed through nginx
- Make sure to keep your SSL certificates updated
- Consider adding rate limiting in nginx for production use
- Don't commit sensitive information to version control

## License

Personal project - customize as needed for your own use.

## Author

Magallan - [https://magallan.online](https://magallan.online)
