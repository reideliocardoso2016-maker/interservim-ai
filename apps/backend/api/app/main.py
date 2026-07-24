from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import init_db, Base
from app.auth.router import router as auth_router
from app.products.router import router as products_router
from app.customers.router import router as customers_router
from app.conversations.router import router as conversations_router
from app.quotes.router import router as quotes_router
from app.ai.router import router as ai_router
from app.integrations.whatsapp.webhook import router as whatsapp_router
from app.marketing.router import router as marketing_router
from app.knowledge.router import router as knowledge_router
from app.analytics.router import router as analytics_router
from app.followups.router import router as followups_router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    init_db()
    Base.metadata.create_all(bind=init_db()[0])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}},
    )


app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(products_router, prefix=settings.api_prefix)
app.include_router(customers_router, prefix=settings.api_prefix)
app.include_router(conversations_router, prefix=settings.api_prefix)
app.include_router(quotes_router, prefix=settings.api_prefix)
app.include_router(ai_router, prefix=settings.api_prefix)
app.include_router(whatsapp_router, prefix=settings.api_prefix)
app.include_router(marketing_router, prefix=settings.api_prefix)
app.include_router(knowledge_router, prefix=settings.api_prefix)
app.include_router(analytics_router, prefix=settings.api_prefix)
app.include_router(followups_router, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {"name": settings.app_name, "version": "1.0.0", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
