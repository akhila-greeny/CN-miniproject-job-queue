# server.py — receives jobs from clients, assigns them to workers via a queue

import socket, threading, json, queue

HOST, PORT = '127.0.0.1', 8080
job_queue = queue.Queue()
in_progress = {}
lock = threading.Lock()

def handle_client(conn, msg):
    job = json.loads(msg)
    with lock: job_queue.put(job)
    print(f"[SERVER] Job queued: {job}")
    conn.send(b"JOB_RECEIVED")
    conn.close()

def handle_worker(conn):
    conn.send(b"READY")
    if conn.recv(1024).decode() != "GET_JOB":
        conn.close(); return

    with lock:
        if job_queue.empty():
            conn.send(b"NO_JOB"); conn.close(); return
        job = job_queue.get()
        in_progress[job["job_id"]] = job

    conn.send(json.dumps(job).encode())
    print(f"[SERVER] Assigned job {job['job_id']}")

    result = conn.recv(1024).decode()
    with lock:
        if result == "DONE":
            del in_progress[job["job_id"]]
            print(f"[SERVER] Job {job['job_id']} done")
        else:
            # worker crashed — requeue the job
            job_queue.put(in_progress.pop(job["job_id"]))
            print(f"[SERVER] Job {job['job_id']} requeued")
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT)); server.listen(10)
print(f"[SERVER] Running on {HOST}:{PORT}")

while True:
    conn, _ = server.accept()
    msg = conn.recv(1024).decode()
    # distinguish workers from clients by their first message
    fn = handle_worker if msg == "WORKER" else handle_client
    args = (conn,) if msg == "WORKER" else (conn, msg)
    threading.Thread(target=fn, args=args, daemon=True).start()
