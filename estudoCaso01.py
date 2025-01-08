import os
import shutil
from datetime import datetime, timedelta

def get_file_info(filepath):

    status = os.stat(filepath)
    created = datetime.fromtimestamp(status.st_ctime)
    modified = datetime.fromtimestamp(status.st_mtime)
    size = status.st_size
    return {
        'name': os.path.basename(filepath),
        'size': size,
        'created': created,
        'modified': modified
    }

def format_file_info(fileinfo):

    return(f"Nome: {fileinfo['name']}, "
        f"Tamanho: {fileinfo['size']} bytes, "
        f"Creation Date: {fileinfo['created'].strftime('%Y-%m-%d %H:%M:%S')}, "
        f"Modification Date: {fileinfo['modified'].strftime('%Y-%m-%d %H:%M:%S')}")

def main():

    source_dir = "/home/valcann/backupsFrom"
    destination_dir = "/home/valcann/backupsTo"
    log_dir = "/home/valcann"

    for directory in [source_dir, destination_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    limitDate = datetime.now() - timedelta(days=3)

    with open(os.path.join(log_dir, "backupsFrom.log"), "w") as log_file:
        log_file.write(f"Log created in: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for filename in os.listdir(source_dir):
            filepath = os.path.join(source_dir, filename)
            if os.path.isfile(filepath):
                fileinfo = get_file_info(filepath)
                log_file.write(f"{format_file_info(fileinfo)}\n")

    copied = []
    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        if os.path.isfile(filepath):
            fileinfo = get_file_info(filepath)

        if fileinfo['created'] < limitDate:
            os.remove(filepath)
        else:
            destination_path = os.path.join(destination_dir, filename)
            shutil.copy2(filepath, destination_path)
            copied.append(fileinfo)

    with open(os.path.join(log_dir, "backupsTo.log"), "w") as log_file:
        log_file.write(f"Log created in: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        log_file.write(f"Total files copied: {len(copied)}\n\n")
        for fileinfo in copied:
            log_file.write(f"{format_file_info(fileinfo)}\n")

if __name__ == "__main__":
    try:
        main()
        print("Backup completed successfully!")
    except Exception as e:
        print(f"Backup Failed: {str(e)}")
