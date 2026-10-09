from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, apply_pragmas
from app.models import mortality as m
from app.routers import mortality as r_mortality
from app.routers import ml as r_ml
from app.routers import upload as r_upload
from app.routers import ingest as r_ingest
from app.routers import facets as r_facets
from app.routers import export as r_export
from app.routers import countries as r_countries

apply_pragmas()
m.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mortality Explorer API", version="1.0.0", docs_url="/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(r_mortality.router)
app.include_router(r_ml.router)
app.include_router(r_upload.router)
app.include_router(r_ingest.router)
app.include_router(r_facets.router)
app.include_router(r_export.router)
app.include_router(r_countries.router)

@app.get("/health")
def health():
    return {"status": "ok"}
