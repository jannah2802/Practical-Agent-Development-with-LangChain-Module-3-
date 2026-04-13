def read_transcript(filename):
    """Tries multiple encodings until one works"""
    encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            print(f"Tried {encoding}... failed")
            continue
    
    raise ValueError("Could not decode file with any common encoding")