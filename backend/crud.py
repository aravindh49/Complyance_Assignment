from sqlalchemy.orm import Session
from . import models, schemas
from .calculations import run_simulation

def get_scenario(db: Session, scenario_id: int):
    """Retrieve a single scenario by its ID."""
    return db.query(models.Scenario).filter(models.Scenario.id == scenario_id).first()

def get_scenarios(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of all scenarios."""
    return db.query(models.Scenario).offset(skip).limit(limit).all()

def create_scenario(db: Session, scenario_data: schemas.ScenarioCreate):
    """
    Create a new scenario entry in the database.
    This involves running the simulation and storing both inputs and outputs.
    """
    # Run simulation to get calculated values
    simulation_results = run_simulation(scenario_data)

    # Combine input data and simulation results
    db_scenario_data = {
        **scenario_data.dict(),
        **simulation_results.dict()
    }

    # Create a new Scenario model instance
    db_scenario = models.Scenario(**db_scenario_data)
    
    # Add to session, commit, and refresh to get the new ID
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    
    return db_scenario
