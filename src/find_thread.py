import threading

from finder import SchemeFinder


class FindingThread(threading.Thread):
    def run(self):
        return SchemeFinder().find()
