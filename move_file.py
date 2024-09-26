import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def on_created(event):
    if event.src_path.endswith('.md'):
        print(f"New file created: {event.src_path}")
        main()

def main():
    # list files in folder
    directory = '/home/mimo/Zettelkasten/Zettelkasten/'
    files = file_list(directory)

    # Check file template | Definisjoner / Filosofi
    definisjoner, filosofi= check_file(files, directory)

    # Check if files exist
    if len(definisjoner) >=1:
        move_file(definisjoner, filosofi)
        print("Fil ble flyttet")
    else:
        print("Ingen filer med tag: [[Definisjoner]] / [[Filosofi]]")


def file_list(dir):
    file_paths = []
    for filename in os.listdir(dir):
        if filename.endswith('.md'):
            file_path = os.path.join(dir, filename)
            file_paths.append(file_path)

    return file_paths


def check_file(files, dir):
    definisjoner_lst = []
    filosofi_lst = []

    for file in files:
        with open(file, 'r') as f:
            words = f.read().split()
            for word in words:
                if word == "[[Definisjoner]]":
                    definisjoner_lst.append(file)
                elif word == "[[Filosofi]]":
                    filosofi_lst.append(file)
                else:
                    None

    return definisjoner_lst, filosofi_lst


def move_file(defi, filo):
    for path in defi:
        filename = path.removeprefix('/home/mimo/Zettelkasten/Zettelkasten/')
        new_path = f"/home/mimo/Zettelkasten/Definisjoner/{filename}"
        os.rename(path, new_path)

    for path in filo:
        filename = path.removeprefix('/home/mimo/Zettelkasten/Zettelkasten/')
        new_path = f"/home/mimo/Zettelkasten/Zettelkasten/Filosofi/{filename}"
        os.rename(path, new_path)

if __name__ == "__main__":
    path = '/home/mimo/Zettelkasten/Zettelkasten/'
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created  # Assign the function directly
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
