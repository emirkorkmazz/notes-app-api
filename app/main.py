from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import notes, auth

app = FastAPI(
    title=settings.PROJECT_NAME,    
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da belirli domain'ler belirtilmeli
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(notes.router, prefix=settings.API_V1_STR)
app.include_router(auth.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Ana endpoint"""
    return {
        "message": "Not Alma API'sine Hoş Geldiniz!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {"status": "healthy", "message": "API çalışıyor"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global hata yakalayıcı"""
    return HTTPException(
        status_code=500,
        detail="Sunucu hatası oluştu"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
