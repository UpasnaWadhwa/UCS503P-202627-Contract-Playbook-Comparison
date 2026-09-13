from fpdf import FPDF
from common.schemas import ContractReport, ClauseVerdict
from reporting.report_builder import build_tabular_report

def write_pdf_report(report: ContractReport, output_path: str):
    """
    Generates a clean one-page-per-contract PDF report using fpdf2.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, f"Contract Report: {report.contract_id}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    
    # Table Header
    pdf.set_font("helvetica", "B", 10)
    
    # A4 width is 210mm. Margins are 10mm each. Total printable width is 190mm.
    col_widths = [35, 25, 65, 65]
    headers = ["Clause", "Status", "Explanation", "Citation"]
    
    for width, header in zip(col_widths, headers):
        pdf.cell(width, 10, header, border=1, align="C")
    pdf.ln()
    
    # Table Data
    pdf.set_font("helvetica", "", 9)
    rows = build_tabular_report(report)
    
    for row in rows:
        clause = row["Clause"]
        status = row["Status"]
        explanation = row["Explanation"]
        citation = row["Citation"]
        
        # Color code status
        if status == ClauseVerdict.MATCH.value:
            pdf.set_text_color(0, 128, 0)  # Green
        elif status == ClauseVerdict.DEVIATION.value:
            pdf.set_text_color(200, 100, 0) # Amber
        elif status == ClauseVerdict.MISSING.value:
            pdf.set_text_color(255, 0, 0)  # Red
        else:
            pdf.set_text_color(0, 0, 0) # Black
            
        # Standard cell for Clause and Status
        max_height = 0
        
        # Calculate max height needed for this row
        # Multi_cell doesn't return height directly in fpdf2 easily, so we estimate based on line breaks
        lines_expl = len(pdf.multi_cell(col_widths[2], 5, explanation, split_only=True))
        lines_cit = len(pdf.multi_cell(col_widths[3], 5, citation, split_only=True))
        lines_clause = len(pdf.multi_cell(col_widths[0], 5, clause, split_only=True))
        
        max_lines = max(lines_expl, lines_cit, lines_clause, 1)
        row_height = max_lines * 5
        
        x = pdf.get_x()
        y = pdf.get_y()
        
        # Draw Clause
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(col_widths[0], 5, clause, border=1, align="L", max_line_height=5)
        pdf.set_xy(x + col_widths[0], y)
        
        # Draw Status
        if status == ClauseVerdict.MATCH.value:
            pdf.set_text_color(0, 128, 0)
        elif status == ClauseVerdict.DEVIATION.value:
            pdf.set_text_color(200, 100, 0)
        elif status == ClauseVerdict.MISSING.value:
            pdf.set_text_color(255, 0, 0)
            
        pdf.multi_cell(col_widths[1], 5, status, border=1, align="C", max_line_height=5)
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(x + col_widths[0] + col_widths[1], y)
        
        # Draw Explanation
        pdf.multi_cell(col_widths[2], 5, explanation, border=1, align="L", max_line_height=5)
        pdf.set_xy(x + col_widths[0] + col_widths[1] + col_widths[2], y)
        
        # Draw Citation
        pdf.multi_cell(col_widths[3], 5, citation, border=1, align="L", max_line_height=5)
        
        # Move to next line
        pdf.set_y(y + row_height)
        
    pdf.output(output_path)
