# coding:utf-8

from threading import Lock, Thread
from six.moves.queue import Queue, Empty


class Control:

    def __init__(self):
        self._stop = False
        self._lock = Lock()

    def reset(self):
        self._stop = False

    def stop(self):
        with self._lock:
            self._stop = True

    def is_stop(self):
        with self._lock:
            return self._stop


class Worker(Thread):

    def __init__(self, task_queue, result_queue, except_queue, control, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._except_queue = except_queue
        self._control = control
        self._result = list()
        self._success_num = 0
        self._failed_num = 0

    def run(self):
        while True:
            try:
                func, args, kwargs = self._task_queue.get_nowait()
                if self._control.is_stop() or func is None:
                    self._task_queue.task_done()
                    continue
                result = func(*args, **kwargs)
                self._success_num += 1
                self._result_queue.put(result)
                self._task_queue.task_done()
            except Empty:
                break
            except Exception as e:
                self._failed_num += 1
                self._except_queue.put(e)
                self._task_queue.task_done()

    def get_result(self):
        return self._success_num, self._failed_num


class ThreadPool:

    def __init__(self, threads=5):
        self._threads = threads
        self._task_queue = Queue()
        self._result_queue = Queue()
        self._except_queue = Queue()
        self._lock = Lock()
        self._control = Control()
        self._workers = list()
        self._active = False
        self._finished = False

    def add_task(self, func, *args, **kwargs):
        self._task_queue.put((func, args, kwargs))

    def start(self):
        if not self._active:
            with self._lock:
                if not self._active:
                    self._finished = False
                    self._control.reset()
                    self._workers = list()
                    for i in range(self._threads):
                        work = Worker(self._task_queue, self._result_queue, self._except_queue, self._control)
                        self._workers.append(work)
                        work.start()
                    self._active = True

    def stop(self):
        self._control.stop()

    def wait_completion(self):
        self._task_queue.join()
        self._finished = True
        self._active = False

    def get_result(self):
        assert self._finished
        detail = [worker.get_result() for worker in self._workers]
        success_all = all([tp[1] == 0 for tp in detail])
        result_list = []
        while True:
            try:
                ret = self._result_queue.get_nowait()
                result_list.append(ret)
            except Empty:
                break
        except_list = []
        while True:
            try:
                except_ = self._except_queue.get_nowait()
                except_list.append(except_)
            except Empty:
                break
        return {'success_all': success_all, 'detail': detail, 'result': result_list, 'except': except_list}
