import time
from concurrent.futures import ThreadPoolExecutor

job_thread = ThreadPoolExecutor(max_workers=2)


def test(s):
    print('task:', s)
    time.sleep(10)


for i in range(10):
    print('exe ', str(i))
    job_thread.submit(test,' num ' + str(i))
