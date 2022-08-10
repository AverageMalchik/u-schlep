from os import scandir, rename, path
from time import sleep
import curses
from curses import wrapper
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
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def on_modified(self, event):
        print(event.src_path.split('\\')[2]+" was modified")


def watch_source():
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
            entries = sorted(entries, key=lambda x: int(x.name.split('.')[0]))
        finally:
            for entry in entries:
                print(entry.name)
    observer = Observer()
    event_handler = Schlepper(source=src_path, destination=dest_path)
    observer.schedule(event_handler, src_path, recursive=False)
    observer.start()
    try:
        while observer.is_alive():
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    COLOR_1 = curses.color_pair(1)
    COLOR_2 = curses.color_pair(2)
    pad = curses.newpad(100, 100)
    stdscr.refresh()

    header = config.HEADER
    for i in range(header.__len__()):
        stdscr.clear()
        stdscr.refresh()
        pad.clear()
        if i % 2 == 0:
            pad.addstr(header[i], COLOR_1)
        else:
            pad.addstr(header[i], COLOR_2)
        pad.refresh(0,0,0,0+i,5,header.__len__()+1)
        sleep(0.2)
            
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(header,COLOR_1|curses.A_UNDERLINE)
    stdscr.addstr(2,0,"Hello!")        
    stdscr.refresh()
    
    stdscr.getch()


wrapper(main)
