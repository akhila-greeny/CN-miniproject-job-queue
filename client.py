# client.py — sends jobs to the server over TCP, one connection per job

import socket, json, time

HOST, PORT = '127.0.0.1', 8080

def send_job(job_id, task):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(json.dumps({"job_id": job_id, "task": task}).encode())
    print(f"[CLIENT] Job {job_id} -> {s.recv(1024).decode()}")
    s.close()

for i in range(1, 6):
    send_job(i, f"task_{i}")
    time.sleep(1)
