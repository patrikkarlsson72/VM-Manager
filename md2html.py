import markdown
import os

def convert_md_to_html():
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define input and output paths
        md_path = os.path.join(current_dir, 'docs', 'how-to-guide.md')
        html_path = os.path.join(current_dir, 'docs', 'how-to-guide.html')
        
        # Read markdown content
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Initialize markdown converter with extensions
        md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',
            'toc',
            'attr_list',
            'def_list',
            'footnotes'
        ])
        
        # Convert to HTML
        html_content = md.convert(md_content)
        
        # HTML template with enhanced styling
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VM Manager - How To Guide</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap">
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #0366d6;
            --background-color: #ffffff;
            --code-background: #f8f9fa;
            --border-color: #e1e4e8;
            --text-color: #24292e;
            --text-secondary: #586069;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
            color: var(--text-color);
            background-color: var(--background-color);
        }}

        .content {{
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        h1, h2, h3, h4 {{
            color: var(--primary-color);
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-weight: 600;
            line-height: 1.25;
            scroll-margin-top: 2rem;
        }}

        h1 {{
            font-size: 2.5rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}

        h2 {{
            font-size: 2rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.3rem;
        }}

        h3 {{
            font-size: 1.5rem;
            color: #34495e;
        }}

        img {{
            max-width: 100%;
            height: auto;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 5px;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }}

        img:hover {{
            transform: scale(1.01);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}

        code {{
            background-color: var(--code-background);
            padding: 0.2em 0.4em;
            border-radius: 6px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.9em;
            color: #d63384;
        }}

        pre {{
            background-color: var(--code-background);
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid var(--border-color);
            margin: 1rem 0;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            color: var(--text-color);
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        th, td {{
            border: 1px solid var(--border-color);
            padding: 0.75rem;
            text-align: left;
        }}

        th {{
            background-color: var(--code-background);
            font-weight: 600;
        }}

        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        tr:hover {{
            background-color: #f1f3f5;
        }}

        blockquote {{
            border-left: 4px solid var(--secondary-color);
            padding: 0.5rem 1rem;
            color: var(--text-secondary);
            margin: 1rem 0;
            background-color: var(--code-background);
            border-radius: 0 8px 8px 0;
        }}

        ul, ol {{
            padding-left: 1.5rem;
            margin: 1rem 0;
        }}

        li {{
            margin: 0.5rem 0;
        }}

        a {{
            color: var(--secondary-color);
            text-decoration: none;
            transition: color 0.2s ease;
        }}

        a:hover {{
            color: #0056b3;
            text-decoration: underline;
        }}

        strong {{
            color: var(--primary-color);
            font-weight: 600;
        }}

        em {{
            color: var(--text-secondary);
        }}

        .toc {{
            background-color: var(--code-background);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            border: 1px solid var(--border-color);
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            .content {{
                padding: 1rem;
            }}

            h1 {{
                font-size: 2rem;
            }}

            h2 {{
                font-size: 1.75rem;
            }}

            h3 {{
                font-size: 1.25rem;
            }}

            pre {{
                max-width: calc(100vw - 2rem);
            }}
        }}

        /* Print styles */
        @media print {{
            body {{
                padding: 0;
                font-size: 12pt;
            }}

            .content {{
                box-shadow: none;
                padding: 0;
            }}

            img {{
                max-width: 500px;
            }}
        }}
    </style>
</head>
<body>
    <div class="content">
        {html_content}
    </div>
</body>
</html>
"""
        
        # Write the HTML file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print("HTML file created successfully!")
        print(f"File size: {len(html_template)} bytes")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    convert_md_to_html()