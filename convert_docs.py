import markdown
import os
from pathlib import Path

def convert_md_to_html():
    # Get the script's directory
    script_dir = Path(__file__).parent
    
    # Define paths
    md_path = script_dir / 'docs' / 'how-to-guide.md'
    html_path = script_dir / 'docs' / 'how-to-guide.html'
    
    # Create docs directory if it doesn't exist
    os.makedirs(md_path.parent, exist_ok=True)
    
    # Read markdown content
    with open(md_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    
    # CSS styling
    css = """
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
        }
        img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            margin: 10px 0;
        }
        code {
            background-color: #f7f9fa;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: Consolas, monospace;
        }
        pre {
            background-color: #f7f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f5f5f5;
        }
        .note {
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin: 20px 0;
        }
    </style>
    """
    
    # Convert markdown to HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>VM Manager - User Guide</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {css}
    </head>
    <body>
        {markdown.markdown(
            md_content,
            extensions=[
                'tables',
                'fenced_code',
                'codehilite',
                'toc'
            ]
        )}
    </body>
    </html>
    """
    
    # Write HTML file
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
    
    print(f"Successfully converted {md_path} to {html_path}")

if __name__ == "__main__":
    try:
        convert_md_to_html()
    except Exception as e:
        print(f"Error: {str(e)}")