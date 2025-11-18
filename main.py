from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

app = FastAPI(title="Magallan Portfolio", description="Personal Job Card Website")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load translations from JSON files
def load_translations():
    translations = {}
    translations_dir = Path("translations")
    for lang_file in translations_dir.glob("*.json"):
        lang_code = lang_file.stem
        with open(lang_file, 'r', encoding='utf-8') as f:
            translations[lang_code] = json.load(f)
    return translations

TRANSLATIONS = load_translations()


def get_user_language(request: Request) -> str:
    """Detect user language from Accept-Language header or query parameter"""
    # First check query parameter
    lang = request.query_params.get("lang")
    if lang in TRANSLATIONS:
        return lang
    
    # Then check Accept-Language header
    accept_language = request.headers.get("accept-language", "")
    if accept_language:
        # Parse the header (e.g., "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7")
        for lang_code in accept_language.split(","):
            lang_code = lang_code.split(";")[0].strip().lower()
            if lang_code.startswith("ru"):
                return "ru"
            elif lang_code.startswith("en"):
                return "en"
    
    # Default to English
    return "en"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, lang: str = None):
    """Main job card page"""
    if lang is None:
        lang = get_user_language(request)
    
    if lang not in TRANSLATIONS:
        lang = "en"
    
    return templates.TemplateResponse(
        "job_card.html",
        {
            "request": request,
            "t": TRANSLATIONS[lang],
            "lang": lang,
            "available_langs": ["en", "ru"]
        }
    )


@app.get("/api/profile")
async def get_profile(lang: str = "en"):
    """API endpoint to get profile data as JSON"""
    if lang not in TRANSLATIONS:
        lang = "en"
    return TRANSLATIONS[lang]


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "magallan-portfolio"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
