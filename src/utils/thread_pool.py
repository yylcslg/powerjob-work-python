
from concurrent.futures import ThreadPoolExecutor

from src.utils.Properties import pro

worker_report_thread = ThreadPoolExecutor(max_workers=3)
job_process_thread = ThreadPoolExecutor(max_workers= int(pro.get('max_job_thread')))




