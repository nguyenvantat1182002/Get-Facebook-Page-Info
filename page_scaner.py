from PyQt5.QtCore import QThread, QRunnable, QThreadPool, QObject, QMutex, QMutexLocker, pyqtSignal
from queue import Queue
from facebook import Page

import random


class Scaner(QRunnable):
    def __init__(self, parent: QThread):
        super().__init__()

        self.parent = parent
        self.page_ids: Queue = self.parent.page_ids

    def run(self) -> None:
        while self.parent.running:
            if self.page_ids.empty():
                break

            with QMutexLocker(self.parent.mutex):
                user_agent = self.parent.get_random_user_agent()
                row, page_id = self.page_ids.get()
                self.page_ids.task_done()

            try:
                p = Page(page_id, user_agent)
                name = p.get_name()
                likes = p.get_likes()
                address = p.get_address()
                verified = p.is_verified()

                self.parent.update_page_name.emit(row, name if name is not None else '')
                self.parent.update_likes.emit(row, likes if likes is not None else '')
                self.parent.update_address.emit(row, address if address is not None else '')
                self.parent.update_verified.emit(row, str(verified))
            except Exception as e:
                print(e)

class PageScaner(QThread):
    update_page_name = pyqtSignal(int, str)
    update_likes = pyqtSignal(int, str)
    update_address = pyqtSignal(int, str)
    update_verified = pyqtSignal(int, str)

    def __init__(self, config: QObject):
        super().__init__()

        self.config = config
        self.running = True
        self.mutex = QMutex()
        self.page_ids = self.get_page_ids()

    def get_page_ids(self) -> Queue:
        max_page_count = self.config.get_max_page_count()
        q = Queue()

        for row in range(max_page_count):
            page_id = self.config.get_page_id(row)
            if not page_id:
                continue

            page_id = page_id.text()
            q.put([row, page_id])

        return q


    def get_random_user_agent(self) -> str:
        with open('user_agents.txt', encoding='utf-8') as file:
            return random.choice(file.readlines()).strip()

    def stop(self) -> None:
        self.running = False

    def run(self) -> None:
        pool = QThreadPool()
        pool.setMaxThreadCount(self.config.max_thread_count)

        for _ in range(pool.maxThreadCount()):
            task = Scaner(self)
            pool.start(task)

            QThread.msleep(500)

        pool.waitForDone(500)
