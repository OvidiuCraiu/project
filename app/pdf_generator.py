
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_contract_pdf(contract, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []
    
    story.append(Paragraph(contract.title, styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Party One: {contract.party_one}", styles['Normal']))
    story.append(Paragraph(f"Party Two: {contract.party_two}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Terms:", styles['Heading2']))
    story.append(Paragraph(contract.terms, styles['Normal']))
    
    doc.build(story)
