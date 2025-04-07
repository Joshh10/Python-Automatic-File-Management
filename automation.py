from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = r"C:\Users\jlaws\Downloads"
video_dir = r"C:\Users\jlaws\Videos"
image_dir = r"C:\Users\jlaws\OneDrive\Pictures"
docs_dir = r"C:\Users\jlaws\OneDrive\Documents"
code_dir = r"C:\Users\jlaws\OneDrive\Documents\CodeFiles"


image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

program_extensions = [".py", ".html", ".cpp", ".js", ".css", ".json", ".c", ".jsx"]


def make_unique(dest, name):
    filename, extension = splitext(name)
    count = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(count)}){extension}"
        count += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.search_video(entry, name)
                self.search_image(entry, name)
                self.check_docs(entry, name)
                self.check_program(entry, name)
                

    def search_video(self, entry, name): 
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(video_dir, entry, name)
                logging.info(f"Moved video file: {name}")

    def search_image(self, entry, name): 
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(image_dir, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_docs(self, entry, name):  
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(docs_dir, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_program(self, entry, name):  
        for program_extension in program_extensions:
            if name.endswith(program_extension) or name.endswith(program_extension.upper()):
                move_file(code_dir, entry, name)
                logging.info(f"Moved document file: {name}")
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()