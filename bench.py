import multiprocessing
import queue
import time
import math


def do_work(task_queue, results_queue):
    while True:
        try:
            task = task_queue.get(timeout=1)

        except queue.Empty:
            break

        result = math.factorial(task)
        results_queue.put(result)
        task_queue.task_done()


def run_benchmark(num_jobs):
    task_queue = multiprocessing.JoinableQueue()
    results_queue = multiprocessing.Queue()

    for i in range(num_jobs):
        task_queue.put(i + 1)

    num_processes = multiprocessing.cpu_count()
    print(f"Total CPU's: {num_processes}")

    # Crea un numero di processi
    start_time = time.time()
    processes = []

    for _ in range(num_processes):
        p = multiprocessing.Process(target=do_work, args=(task_queue, results_queue))
        processes.append(p)
        p.start()

    task_queue.join()

    print(f"Benchmark time {time.time() - start_time}")

    for p in processes:
        p.terminate()


if __name__ == "__main__":
    # I7 14700K         58.40 s
    # RYZEN 7 5800X     127.51 s

    num_jobs = 65536
    run_benchmark(num_jobs)
