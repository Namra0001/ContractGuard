from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

def generate_report(analysis_result: dict, output_path: str):
    """Generates a PDF report based on the analysis result."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "Contract Analysis Report")
    
    c.setFont("Helvetica", 12)
    y_position = height - 100
    
    for key, value in analysis_result.items():
        if y_position < 72:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 72
            
        c.drawString(72, y_position, f"{key.capitalize()}:")
        y_position -= 20
        
        if isinstance(value, list):
            for item in value:
                if y_position < 72:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = height - 72
                c.drawString(92, y_position, f"- {item}")
                y_position -= 15
        else:
            c.drawString(92, y_position, str(value))
            y_position -= 15
            
        y_position -= 10
        
    c.save()
