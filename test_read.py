import os

def test_markdown_read():
    try:
        # Get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Print current directory
        print(f"Current directory: {current_dir}")
        
        # Construct markdown file path
        md_path = os.path.join(current_dir, 'docs', 'how-to-guide.md')
        
        # Print markdown file path
        print(f"Looking for markdown file at: {md_path}")
        
        # Check if file exists
        if not os.path.exists(md_path):
            print(f"ERROR: File not found at {md_path}")
            return
            
        # Try to read the file
        with open(md_path, 'r', encoding='utf-8') as md_file:
            content = md_file.read()
            
        # Print first 500 characters of content
        print("\nFirst 500 characters of markdown content:")
        print("-" * 50)
        print(content[:500])
        print("-" * 50)
        print(f"\nTotal content length: {len(content)} characters")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_markdown_read()