from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import classify

app = FastAPI(
    title="RegAI - CDSCO Compliance Backend",
    description="Product-Ready API for classifying medical devices according to CDSCO regulations.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: Specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(classify.router, prefix="/api/v1", tags=["Classification"])

@app.get("/")
async def root():
    return {"message": "Welcome to RegAI CDSCO Compliance API. Visit /docs for Swagger UI."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
