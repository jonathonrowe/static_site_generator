import os
import shutil

def copy_contents(source, destination):
    try:
        if os.path.exists(source):
            if os.path.exists(destination):
                try:
                    shutil.rmtree(destination)
                    os.mkdir(destination)
                except OSError as e:
                    print(f"Error removing directory {destination}: {e}")
            else:
                os.mkdir(destination)

            entries = os.listdir(source)
            for entry in entries:
                full_source_path = os.path.join(source, entry)
                full_dest_path = os.path.join(destination, entry)

                if os.path.isfile(full_source_path):
                    shutil.copy(full_source_path, full_dest_path)
                else:
                    os.mkdir(full_dest_path)
                    copy_contents(full_source_path, full_dest_path)

    except Exception as e:
        print(f"Error: {e}")