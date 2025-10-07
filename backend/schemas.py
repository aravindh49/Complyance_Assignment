from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# --- Simulation Schemas ---

class SimulationInput(BaseModel):
    """Pydantic model for validating simulation input data."""
    monthly_invoice_volume: int = Field(..., gt=0, description="Number of invoices processed per month.")
    num_ap_staff: int = Field(..., gt=0, description="Number of staff in Accounts Payable.")
    avg_hours_per_invoice: float = Field(..., gt=0, description="Average hours to process one invoice manually.")
    hourly_wage: float = Field(..., gt=0, description="Average hourly wage for an AP staff member.")
    error_rate_manual: float = Field(..., ge=0, le=100, description="Percentage of invoices with errors in manual processing.")
    error_cost: float = Field(..., gt=0, description="Average cost to fix one error.")
    time_horizon_months: int = Field(..., gt=0, description="Number of months to project savings over.")
    one_time_implementation_cost: float = Field(..., ge=0, description="One-time cost to implement the automation solution.")

class SimulationOutput(BaseModel):
    """Pydantic model for returning simulation results."""
    monthly_savings: float
    payback_months: Optional[float]
    roi_percentage: Optional[float]
    net_savings: float
    cumulative_savings: float

# --- Scenario Schemas (for DB operations) ---

class ScenarioBase(SimulationInput):
    """Base schema for a scenario, includes all inputs."""
    scenario_name: str = Field(..., min_length=1, max_length=100)

class ScenarioCreate(ScenarioBase):
    """Schema used for creating a new scenario. No extra fields needed."""
    pass

class Scenario(ScenarioBase):
    """Schema for returning a scenario from the DB, includes ID and calculated outputs."""
    id: int
    monthly_savings: float
    payback_months: Optional[float]
    roi_percentage: Optional[float]
    net_savings: float
    cumulative_savings: float

    class Config:
        from_attributes = True

# --- Report Generation Schema ---

class ReportRequest(BaseModel):
    """Schema for the PDF report generation request."""
    scenario_id: int
    email: EmailStr
