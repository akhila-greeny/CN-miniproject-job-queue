# 🧠 Distributed Job Queue System using TCP Sockets

## 📌 Overview
This project implements a distributed job queue system using TCP sockets in Python.  
It consists of three components: a Client, a Server, and multiple Workers.

- Clients submit jobs to the server  
- The server manages a queue of jobs  
- Workers request jobs, execute them, and report completion  

The system supports concurrency and basic fault tolerance, ensuring that no job is lost.

---

## ⚙️ Features
- Multi-client support using threading  
- Multiple workers for parallel processing  
- Thread-safe job queue  
- Fault tolerance (reassign jobs if worker crashes)  
- No job duplication  
- Simple TCP socket communication  

---

## 🏗️ System Architecture

Client  --->  Server  --->  Worker
   |            |            |
   |----Jobs----|            |
                |----Assign Job----> Worker
                |<---Result---------|

---

## 📁 Project Structure

job_queue/
│
├── server.py   # Handles job queue and connections
├── client.py   # Sends jobs to server
└── worker.py   # Processes jobs

---

## 🚀 How to Run

### 1️⃣ Start Server
python server.py

### 2️⃣ Start Worker(s)
python worker.py

### 3️⃣ Run Client
python client.py

---

## 🔄 Workflow

### Client
- Connects to server  
- Sends job in JSON format:
{ "job_id": 1, "task": "task_1" }

### Server
- Accepts connections from clients and workers  
- Stores jobs in a queue  
- Assigns jobs to workers  
- Tracks jobs in progress  
- Reassigns jobs if a worker crashes  

### Worker
- Requests job from server (GET_JOB)  
- Executes the job  
- Sends "DONE" after completion  

---

## 🛡️ Fault Tolerance
If a worker crashes before completing a job:
- The server detects failure  
- The job is moved back to the queue  
- Another worker processes it  

---

## 🧵 Concurrency
- The server uses multithreading  
- Each client/worker connection runs in a separate thread  
- Ensures multiple jobs can be processed simultaneously  

---

## 📚 Technologies Used
- Python  
- TCP Sockets  
- Multithreading  
- Queue  
- JSON  

---

## 🎯 Example Output

### Server
[SERVER] Job queued: {'job_id': 1, 'task': 'task_1'}
[SERVER] Assigned job 1
[SERVER] Job 1 done

### Worker
[WORKER] Got job 1
[WORKER] Finished job 1

### Client
[CLIENT] JOB_RECEIVED
[CLIENT] JOB_RECEIVED
[CLIENT] JOB_RECEIVED

---

## 🎓 Learning Outcomes
- Understanding TCP socket programming  
- Implementing client-server architecture  
- Handling concurrency with threads  
- Designing fault-tolerant systems  
- Managing shared resources safely  

---

## 📌 Conclusion
This project demonstrates how a distributed system can efficiently manage tasks using a centralized server, multiple workers, and concurrent client requests while ensuring reliability and scalability.
