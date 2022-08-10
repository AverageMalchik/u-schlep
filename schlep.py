from os import scandir,rename,path
from time import sleep
import sys
import logging
import config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def rename():
    pass

def move():
    pass

class Schlepper(FileSystemEventHandler):
    def __init__(self,source,destination):
        self.source = source
        self.destination = destination
    
    def on_modified(self, event):
        print(event.src_path.split('\\')[2]+" was modified")
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    try:
        src_path = sys.argv[1] 
        dest_path = sys.argv[2]
    except IndexError:
        src_path = config.DEFAULT_SRC 
        dest_path = config.DEFAULT_DEST
    with scandir(src_path) as it:
        entries = list(it)
        try:
            entries = sorted(entries,key=lambda x: int(x.name.split('.')[0]))
        finally:
            for entry in entries:
                print(entry.name)
    observer = Observer()
    event_handler = Schlepper(source=src_path,destination=dest_path)
    observer.schedule(event_handler,src_path,recursive=False)
    observer.start()
    try:
        while observer.is_alive():
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    