from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Scenario(Base):
    """
    SQLAlchemy model for the 'scenarios' table.
    Stores both the user inputs and the calculated results for a simulation.
    """
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    scenario_name = Column(String, index=True)

    # Input fields
    monthly_invoice_volume = Column(Integer)
    num_ap_staff = Column(Integer)
    avg_hours_per_invoice = Column(Float)
    hourly_wage = Column(Float)
    error_rate_manual = Column(Float)
    error_cost = Column(Float)
    time_horizon_months = Column(Integer)
    one_time_implementation_cost = Column(Float)

    # Calculated output fields
    monthly_savings = Column(Float)
    payback_months = Column(Float, nullable=True)
    roi_percentage = Column(Float, nullable=True)
    net_savings = Column(Float)
    cumulative_savings = Column(Float)
