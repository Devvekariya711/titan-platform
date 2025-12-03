import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def extract_text_from_docx(docx_path):
    if not os.path.exists(docx_path):
        print(f"Error: File not found at {docx_path}")
        return

    try:
        with zipfile.ZipFile(docx_path) as zf:
            xml_content = zf.read('word/document.xml')
        
        tree = ET.fromstring(xml_content)
        
        # Define the namespace map
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        text_parts = []
        for p in tree.findall('.//w:p', ns):
            paragraph_text = []
            for t in p.findall('.//w:t', ns):
                if t.text:
                    paragraph_text.append(t.text)
            if paragraph_text:
                text_parts.append(''.join(paragraph_text))
        
        full_text = '\n'.join(text_parts)
        print(full_text)
        
    except Exception as e:
        print(f"Error extracting text: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <path_to_docx>")
    else:
        # Redirect stdout to a file with utf-8 encoding
        with open('extracted_output.txt', 'w', encoding='utf-8') as f:
            sys.stdout = f
            extract_text_from_docx(sys.argv[1])
