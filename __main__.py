import logging
import sys
import time

import click
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from solarlog_exporter.core import start_import


@click.command()
@click.option('-v', '--verbose', is_flag=True, help="Debug output")
@click.option('-o', '--observer', is_flag=True, help="Runs with watchdog observer, that scans the directory for new "
                                                     "files")
@click.option('-d', '--directory', required=True, type=click.Path(resolve_path=True), help="Directory that should be "
                                                                                           "scanned for solarlog files")
def main(verbose, observer, directory):
    """
    Run main application with can interface
    """
    # Verbose output
    if verbose is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # watchdog
    if observer is True:
        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True

        event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        event_handler.on_created = start_import(directory)
        event_handler.on_modified = start_import(directory)
        observer = Observer()
        observer.schedule(event_handler, directory, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()
    else:
        start_import(directory)


if __name__ == "__main__":
    sys.exit(main())
