from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from . import crud, models, schemas, calculations, report_generator
from .database import SessionLocal, engine

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Invoicing ROI Simulator API",
    description="API to simulate ROI for invoicing automation and manage scenarios.",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, suitable for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/simulate", response_model=schemas.SimulationOutput, tags=["Simulation"])
def simulate_roi(simulation_data: schemas.SimulationInput):
    """
    Runs a new ROI simulation based on the provided data and returns the calculated results.
    This endpoint does not save the scenario.
    """
    results = calculations.run_simulation(simulation_data)
    return results

@app.post("/scenarios", response_model=schemas.Scenario, status_code=201, tags=["Scenarios"])
def create_scenario(scenario_data: schemas.ScenarioCreate, db: Session = Depends(get_db)):
    """
    Creates and saves a new scenario, including inputs and calculated results.
    """
    return crud.create_scenario(db=db, scenario_data=scenario_data)

@app.get("/scenarios", response_model=List[schemas.Scenario], tags=["Scenarios"])
def read_scenarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all saved scenarios.
    """
    scenarios = crud.get_scenarios(db, skip=skip, limit=limit)
    return scenarios

@app.get("/scenarios/{scenario_id}", response_model=schemas.Scenario, tags=["Scenarios"])
def read_scenario(scenario_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single scenario by its ID.
    """
    db_scenario = crud.get_scenario(db, scenario_id=scenario_id)
    if db_scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return db_scenario

@app.post("/report/generate", tags=["Reports"])
def generate_report(report_request: schemas.ReportRequest, db: Session = Depends(get_db)):
    """
    Generates a PDF report for a specific scenario and requires an email address.
    The report is saved on the server.
    """
    # 1. Fetch the scenario from the database
    scenario = crud.get_scenario(db, scenario_id=report_request.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # 2. Generate the PDF report
    try:
        # Convert the SQLAlchemy model to a Pydantic schema for the generator function
        scenario_schema = schemas.Scenario.from_orm(scenario)
        file_path = report_generator.generate_pdf_report(scenario_schema, report_request.email)
        return {
            "message": "Report generated successfully",
            "file_path": file_path
        }
    except Exception as e:
        # Log the exception e
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF report: {str(e)}")
