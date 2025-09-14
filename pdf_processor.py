import pdfplumber
import re
from typing import List, Dict

def extract_and_clean(pdf_path: str) -> List[Dict]:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(layout=True)
            if not text:
                continue
            lines = text.split('\n')
            height = page.height
            chars = page.chars or []
            content_lines = [
                line for i, line in enumerate(lines)
                if not chars or (chars[0]['y0'] > 0.1 * height and chars[-1]['y1'] < 0.9 * height)
            ]
            cleaned = '\n'.join(content_lines).strip()
            cleaned = re.sub(r'Page \d+', '', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            if cleaned:
                pages.append({'page_num': page.page_number, 'text': cleaned})
    return pages