from fastapi import FastAPI
from routers.documents import router as document_router
app = FastAPI(title="smart-document-manager")
app.include_router(document_router)

