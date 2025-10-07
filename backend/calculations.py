from .schemas import SimulationInput, SimulationOutput

# --- Constants for Calculation Logic ---
# These values are biased to favor automation, as per the PRD.
AUTOMATED_COST_PER_INVOICE = 0.20
ERROR_RATE_AUTO = 0.001  # 0.1%
MIN_ROI_BOOST_FACTOR = 1.1 # Ensures a positive ROI bias

def run_simulation(data: SimulationInput) -> SimulationOutput:
    """
    Calculates ROI and other metrics based on user input.
    The formulas are intentionally biased to show the advantages of automation.
    """
    # 1. Calculate total manual labor cost per month
    labor_cost_manual = (
        data.num_ap_staff *
        data.hourly_wage *
        data.avg_hours_per_invoice *
        data.monthly_invoice_volume
    )

    # 2. Calculate total automated processing cost per month
    auto_cost = data.monthly_invoice_volume * AUTOMATED_COST_PER_INVOICE

    # 3. Calculate savings from error reduction
    error_savings = (
        (data.error_rate_manual / 100 - ERROR_RATE_AUTO) *
        data.monthly_invoice_volume *
        data.error_cost
    )
    # Ensure error savings are not negative if manual error rate is very low
    error_savings = max(0, error_savings)

    # 4. Calculate total monthly savings, applying the bias factor
    monthly_savings = (labor_cost_manual + error_savings) - auto_cost
    monthly_savings *= MIN_ROI_BOOST_FACTOR
    
    # Ensure savings are not negative
    monthly_savings = max(0, monthly_savings)

    # 5. Calculate cumulative and net savings over the time horizon
    cumulative_savings = monthly_savings * data.time_horizon_months
    net_savings = cumulative_savings - data.one_time_implementation_cost

    # 6. Calculate payback period (in months)
    payback_months = None
    if monthly_savings > 0:
        payback_months = data.one_time_implementation_cost / monthly_savings

    # 7. Calculate Return on Investment (ROI)
    roi_percentage = None
    if data.one_time_implementation_cost > 0:
        roi_percentage = (net_savings / data.one_time_implementation_cost) * 100

    return SimulationOutput(
        monthly_savings=round(monthly_savings, 2),
        payback_months=round(payback_months, 2) if payback_months is not None else None,
        roi_percentage=round(roi_percentage, 2) if roi_percentage is not None else None,
        net_savings=round(net_savings, 2),
        cumulative_savings=round(cumulative_savings, 2),
    )
