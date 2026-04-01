    # worker.py — polls server for jobs, processes them, reports back DONE
# 20% random crash simulates real-world worker failures (tests server's requeue logic)

import socket, json, time, random

HOST, PORT = '127.0.0.1', 8080

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(b"WORKER")

        if s.recv(1024).decode() != "READY":
            s.close(); continue

        s.send(b"GET_JOB")
        data = s.recv(1024).decode()

        if data == "NO_JOB":
            print("[WORKER] No jobs, waiting..."); time.sleep(2); s.close(); continue

        job = json.loads(data)
        print(f"[WORKER] Got job {job['job_id']}")

        # simulate crash — close without sending DONE so server requeues the job
        if random.random() < 0.2:
            print("[WORKER] Crashed!"); s.close(); continue

        time.sleep(2)  # simulate actual processing time
        s.send(b"DONE")
        print(f"[WORKER] Finished job {job['job_id']}")

    except Exception as e:
        print(f"[WORKER] Error: {e}")
    finally:
        s.close(); time.sleep(1)
