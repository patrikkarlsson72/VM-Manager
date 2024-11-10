import os

def debug_read():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        md_path = os.path.join(current_dir, 'docs', 'how-to-guide.md')
        
        # Get file size
        file_size = os.path.getsize(md_path)
        print(f"File size: {file_size} bytes")
        
        # Try reading with different encodings
        encodings = ['utf-8', 'utf-8-sig', 'ascii', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                print(f"\nTrying with {encoding} encoding:")
                with open(md_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    print(f"Successfully read {len(content)} characters")
                    print("First 200 characters:")
                    print("-" * 50)
                    print(content[:200])
                    print("-" * 50)
                break
            except UnicodeDecodeError:
                print(f"Failed with {encoding} encoding")
                continue
        
        # Try reading in binary mode
        with open(md_path, 'rb') as f:
            binary_content = f.read()
            print(f"\nBinary read: {len(binary_content)} bytes")
            print("First few bytes:", binary_content[:20])
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    debug_read()