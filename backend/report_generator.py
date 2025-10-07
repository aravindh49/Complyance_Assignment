import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

from . import schemas

def generate_pdf_report(scenario: schemas.Scenario, email: str) -> str:
    """
    Generates a PDF report for a given scenario and saves it to the filesystem.
    
    Args:
        scenario: The scenario data (inputs and outputs).
        email: The user's email (for display in the report).

    Returns:
        The file path where the PDF was saved.
    """
    # Ensure the reports directory exists
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Sanitize scenario name for the filename
    safe_filename = "".join(c for c in scenario.scenario_name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join(reports_dir, f"{safe_filename}_{scenario.id}.pdf")

    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Invoicing ROI Simulation Report", styles['h1']))
    story.append(Spacer(1, 0.2 * inch))

    # Sub-header
    story.append(Paragraph(f"Scenario: {scenario.scenario_name}", styles['h2']))
    story.append(Paragraph(f"Report generated for: {email}", styles['Normal']))
    story.append(Spacer(1, 0.4 * inch))

    # --- Summary Section ---
    story.append(Paragraph("Key Results Summary", styles['h3']))
    summary_data = [
        ["Metric", "Value"],
        ["Total Net Savings", f"${scenario.net_savings:,.2f} (over {scenario.time_horizon_months} months)"],
        ["Return on Investment (ROI)", f"{scenario.roi_percentage:.2f}%" if scenario.roi_percentage is not None else "N/A"],
        ["Monthly Savings", f"${scenario.monthly_savings:,.2f}"],
        ["Payback Period", f"{scenario.payback_months:.2f} months" if scenario.payback_months is not None else "N/A"],
    ]
    summary_table = Table(summary_data, colWidths=[2.5 * inch, 2.5 * inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.4 * inch))

    # --- Inputs and Outputs Section ---
    story.append(Paragraph("Detailed Breakdown", styles['h3']))
    
    # Data for the detailed table
    details_data = [
        ["Category", "Parameter", "Value"],
        # Inputs
        ["Inputs", "Monthly Invoice Volume", f"{scenario.monthly_invoice_volume:,}"],
        ["", "AP Staff Count", f"{scenario.num_ap_staff}"],
        ["", "Avg. Hours per Invoice (Manual)", f"{scenario.avg_hours_per_invoice}"],
        ["", "AP Staff Hourly Wage", f"${scenario.hourly_wage:,.2f}"],
        ["", "Manual Error Rate", f"{scenario.error_rate_manual}%"],
        ["", "Avg. Cost per Error", f"${scenario.error_cost:,.2f}"],
        ["", "Implementation Cost", f"${scenario.one_time_implementation_cost:,.2f}"],
        ["", "Time Horizon", f"{scenario.time_horizon_months} months"],
        # Outputs
        ["Outputs", "Cumulative Savings", f"${scenario.cumulative_savings:,.2f}"],
        ["", "Net Savings", f"${scenario.net_savings:,.2f}"],
        ["", "Monthly Savings", f"${scenario.monthly_savings:,.2f}"],
        ["", "Payback Period (Months)", f"{scenario.payback_months:.2f}" if scenario.payback_months is not None else "N/A"],
        ["", "ROI", f"{scenario.roi_percentage:.2f}%" if scenario.roi_percentage is not None else "N/A"],
    ]

    details_table = Table(details_data, colWidths=[1.5 * inch, 3 * inch, 2 * inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Span 'Inputs' and 'Outputs' category cells
        ('SPAN', (0, 1), (0, 8)),
        ('SPAN', (0, 9), (0, 13)),
        ('VALIGN', (0, 1), (0, 8), 'MIDDLE'),
        ('VALIGN', (0, 9), (0, 13), 'MIDDLE'),
        ('BACKGROUND', (0, 1), (0, 8), colors.lightgrey),
        ('BACKGROUND', (0, 9), (0, 13), colors.lightblue),
    ]))
    story.append(details_table)

    doc.build(story)
    return filepath
