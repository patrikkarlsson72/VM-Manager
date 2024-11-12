import os
import markdown2

def convert_md_to_html():
    try:
        # Get file paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        md_path = os.path.join(current_dir, 'docs', 'how-to-guide.md')
        html_path = os.path.join(current_dir, 'docs', 'how-to-guide.html')
        
        # Read markdown content
        with open(md_path, 'r', encoding='utf-8') as md_file:
            content = md_file.read()
            
        # Convert markdown to HTML using markdown2
        html_content = markdown2.markdown(
            content,
            extras=[
                'fenced-code-blocks',
                'tables',
                'header-ids',
                'toc',
                'markdown-in-html'
            ]
        )
        
        # Create complete HTML document
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>VM Manager - User Guide</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{ 
            color: #2c3e50; 
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        h2 {{ 
            color: #34495e; 
            margin-top: 30px;
        }}
        h3 {{
            color: #2c3e50;
            margin-top: 20px;
        }}
        img {{ 
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            margin: 10px 0;
        }}
        code {{ 
            background-color: #f7f9fa;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: Consolas, monospace;
        }}
        pre {{ 
            background-color: #f7f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin: 5px 0;
        }}
        em {{
            font-style: italic;
            color: #666;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        # Write HTML file
        with open(html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(full_html)
            
        print(f"HTML file created successfully at: {html_path}")
        
        # Verify content
        with open(html_path, 'r', encoding='utf-8') as f:
            html_verify = f.read()
            print(f"HTML file size: {len(html_verify)} bytes")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    convert_md_to_html()