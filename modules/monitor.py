import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from modules.scanner import scan_file


class DownloadHandler(FileSystemEventHandler):

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback

    def process_file(self, file_path):

        temp_extensions = (".tmp", ".crdownload", ".part")

        if file_path.lower().endswith(temp_extensions):
            return

        print(f"\nNew file detected: {file_path}")

        time.sleep(2)

        if os.path.exists(file_path):
            result = scan_file(file_path)

            # send result to GUI
            if self.callback and isinstance(result, dict):
                msg = f"{result['prediction']}: {file_path}"
                self.callback(msg)

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.dest_path)
def start_monitoring(path, callback=None):

    event_handler = DownloadHandler(callback)

    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    observer.start()

    print("FortiShield is monitoring downloads...")

    try:
        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()