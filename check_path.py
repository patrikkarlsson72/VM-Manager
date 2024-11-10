import os

def check_path():
    try:
        # Get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Current directory: {current_dir}")
        
        # List all files in current directory
        print("\nFiles in current directory:")
        print(os.listdir(current_dir))
        
        # Check docs directory
        docs_path = os.path.join(current_dir, 'docs')
        if os.path.exists(docs_path):
            print("\nFiles in docs directory:")
            print(os.listdir(docs_path))
        else:
            print("\nDocs directory not found!")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_path()