from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import markdown
import re

class PDFGuideGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        
        # Simply use the direct path from project root
        self.md_file = 'docs/how-to-guide.md'
        # Or for more robustness:
        # self.md_file = os.path.join(os.path.dirname(__file__), 'docs', 'how-to-guide.md')
        
    def setup_styles(self):
        """Setup custom styles for the PDF"""
        # Custom styles using system fonts
        style_definitions = {
            'Heading1': ParagraphStyle(
                name='Heading1',
                fontName='Helvetica-Bold',
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor('#1a73e8')
            ),
            'Heading2': ParagraphStyle(
                name='Heading2',
                fontName='Helvetica-Bold',
                fontSize=18,
                spaceAfter=20,
                textColor=colors.HexColor('#202124')
            ),
            'BodyText': ParagraphStyle(
                name='BodyText',
                fontName='Helvetica',
                fontSize=12,
                spaceAfter=12,
                leading=16
            ),
            'Note': ParagraphStyle(
                name='Note',
                fontName='Helvetica-Oblique',
                fontSize=11,
                textColor=colors.HexColor('#666666'),
                spaceAfter=12,
                leading=14
            )
        }

        # Only add styles if they don't already exist
        for style_name, style in style_definitions.items():
            if style_name not in self.styles:
                self.styles.add(style)

    def convert_markdown_to_pdf(self, markdown_file, output_pdf, images_dir):
        """Convert markdown file to PDF"""
        # Read markdown content
        with open(markdown_file, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        # Create PDF document
        doc = SimpleDocTemplate(
            output_pdf,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Create story (content) for the PDF
        story = []

        # Add logo if it exists
        logo_path = os.path.join(images_dir, "vm_logo.png")
        if os.path.exists(logo_path):
            img = Image(logo_path)
            img.drawHeight = 1.5*inch
            img.drawWidth = 1.5*inch
            story.append(img)
            story.append(Spacer(1, 20))

        # Split content into sections
        sections = markdown_content.split('\n## ')
        
        # Process title section
        title_section = sections[0].replace('# ', '')
        story.append(Paragraph(title_section.strip(), self.styles['Heading1']))
        story.append(Spacer(1, 20))

        # Process remaining sections
        for section in sections[1:]:
            # Split section into title and content
            section_parts = section.split('\n', 1)
            if len(section_parts) == 2:
                title, content = section_parts
                
                # Add section title
                story.append(Paragraph(title.strip(), self.styles['Heading2']))
                
                # Process content paragraphs
                paragraphs = content.strip().split('\n\n')
                for para in paragraphs:
                    # Skip empty paragraphs
                    if not para.strip():
                        continue
                    
                    # Handle lists
                    if para.startswith(('- ', '1. ')):
                        lines = para.split('\n')
                        for line in lines:
                            # Indent list items
                            if line.startswith('- '):
                                story.append(Paragraph('• ' + line[2:], self.styles['BodyText']))
                            elif re.match(r'\d+\. ', line):
                                story.append(Paragraph(line, self.styles['BodyText']))
                    # Handle notes (italics)
                    elif para.startswith('*') and para.endswith('*'):
                        story.append(Paragraph(para[1:-1], self.styles['Note']))
                    # Handle regular paragraphs
                    else:
                        story.append(Paragraph(para, self.styles['BodyText']))
                
                # Try to add corresponding image
                image_name = title.lower().replace(' ', '-') + '.png'
                image_path = os.path.join(images_dir, image_name)
                if os.path.exists(image_path):
                    img = Image(image_path)
                    # Scale image to fit page width while maintaining aspect ratio
                    img.drawWidth = 6*inch  # Max width
                    img._restrictSize(6*inch, 8*inch)
                    story.append(img)
                    story.append(Spacer(1, 12))

        # Build PDF
        doc.build(story)

def generate_pdf_guide():
    """Generate the PDF how-to guide"""
    try:
        # Setup paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        docs_dir = os.path.join(current_dir, 'docs')
        images_dir = os.path.join(docs_dir, 'images')
        markdown_file = os.path.join(docs_dir, 'how-to-guide.md')
        output_pdf = os.path.join(docs_dir, 'VM-Manager-How-To-Guide.pdf')

        # Create PDF generator and convert markdown to PDF
        generator = PDFGuideGenerator()
        generator.convert_markdown_to_pdf(markdown_file, output_pdf, images_dir)
        
        print(f"PDF guide generated successfully: {output_pdf}")
        return True
        
    except Exception as e:
        print(f"Error generating PDF guide: {str(e)}")
        return False

if __name__ == "__main__":
    generate_pdf_guide()
