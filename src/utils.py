import os
import json
import time
import requests
import re
import pandas as pd
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse, unquote


def save_links(urls: list, save_path: Path):
    """Save a list of URLs to a file atomically."""
    tmp_path = Path(save_path).with_suffix('.tmp')
    with open(tmp_path, 'w') as f:
        f.write("\n".join(urls) + "\n")
    os.replace(tmp_path, save_path)


def load_links(file_path: Path) -> list:
    """Load a list of URLs from a file."""
    if not os.path.exists(file_path):
        return set() # Return empty set if file does not exist
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f if line.strip())
    

def save_meta(base_url: str, urls: list, save_path: Path):
    """Save metadata dictionary to a file atomically."""
    payload = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "base_url": base_url,
        "url_count": len(urls)
    }
    tmp_path = Path(save_path).with_suffix('.tmp')
    with open(tmp_path, 'w') as f:
        json.dump(payload, f, indent=4)
    os.replace(tmp_path, save_path)


def save_pdf_to_disk(pdf_bytes: bytes, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pdf_bytes)
    return path


def fetch_pdf_bytes(url: str, timeout: int = 30, session=None) -> bytes:
    s = session or requests.Session()
    headers = {
        "User-Agent": "pdf-fetch/1.0",
        "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.8",
    }
    with s.get(url, headers=headers, timeout=timeout, stream=True) as r:
        r.raise_for_status()
        buf = BytesIO()
        for chunk in r.iter_content(chunk_size=1024 * 64):
            if chunk:
                buf.write(chunk)
        data = buf.getvalue()

        # Basic validation
        if not data.startswith(b"%PDF-"):
            ct = (r.headers.get("Content-Type") or "").lower()
            if "pdf" not in ct:
                raise ValueError(f"Not a PDF: {url} (Content-Type: {ct})")

    return data


def url_to_safe_pdf_name(url: str) -> str:
    p = urlparse(url)
    # Take only the path segment, drop query/fragment
    candidate = Path(unquote(p.path)).name or "download"
    # Replace anything not alnum, dot, underscore, hyphen
    candidate = re.sub(r"[^A-Za-z0-9._-]", "_", candidate)
    # Ensure .pdf suffix (only if it’s missing)
    if not candidate.lower().endswith(".pdf"):
        candidate += ".pdf"
    # Optional: cap length
    return candidate[:200]


def csv_to_json(csv_file, top_level_key, output_dir, output_file='output.json'):
    """Convert a CSV file to JSON format and save it to the specified directory."""
    # Read CSV
    df = pd.read_csv(csv_file)
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Convert df to dict
    items = df[top_level_key].dropna().to_list()
    # Add a top level key
    df_dict = {top_level_key: items}
    # Write to JSON file
    open(output_dir / output_file, 'w').write(json.dumps(df_dict, indent=4))
