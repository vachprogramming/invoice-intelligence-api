from fastapi import FastAPI

# Initializing FastAPI app with project metadata for auto-generated docs
app = FastAPI(
    title="Invoice Intelligence API",
    description="A portfolio project for extracting data from German invoices.",
    version="0.1.0"
)

# Root endpoint: simple health check
# Returns 200 OK if the server is running
@app.get("/")
def read_root():
    return {
        "project": "Invoice Intelligence",
        "status": "online",
        "author": "Student Candidate" 
    }