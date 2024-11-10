import os

def test_write():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.join(current_dir, 'docs', 'test.txt')
        
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write("Test content")
            
        print(f"Test file written to: {test_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_write()