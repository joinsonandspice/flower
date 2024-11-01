import json
from flower.events import EventsState

def export_tasks_and_workers(events_state):
    data = {
        "tasks": [],
        "workers": []
    }

    for task_id, task in events_state.tasks.items():
        data["tasks"].append({
            "id": task_id,
            "name": task.name,
            "args": task.args,
            "kwargs": task.kwargs,
            "result": task.result,
            "state": task.state,
            "received": task.received,
            "started": task.started,
            "succeeded": task.succeeded,
            "failed": task.failed,
            "retried": task.retried,
            "retries": task.retries,
            "worker": task.worker.hostname if task.worker else None,
            "traceback": task.traceback
        })

    for worker_name, worker in events_state.workers.items():
        data["workers"].append({
            "name": worker_name,
            "hostname": worker.hostname,
            "pid": worker.pid,
            "freq": worker.freq,
            "heartbeats": worker.heartbeats,
            "clock": worker.clock,
            "active": worker.active,
            "processed": worker.processed,
            "loadavg": worker.loadavg,
            "sw_ident": worker.sw_ident,
            "sw_ver": worker.sw_ver,
            "sw_sys": worker.sw_sys
        })

    return json.dumps(data)

def import_tasks_and_workers(events_state, data):
    # data = json.loads(data)

    for task_data in data["tasks"]:
        task = events_state.tasks.get(task_data["id"])
        if not task:
            task = events_state.Task()
            events_state.tasks[task_data["id"]] = task

        task.name = task_data["name"]
        task.args = task_data["args"]
        task.kwargs = task_data["kwargs"]
        task.result = task_data["result"]
        task.state = task_data["state"]
        task.received = task_data["received"]
        task.started = task_data["started"]
        task.succeeded = task_data["succeeded"]
        task.failed = task_data["failed"]
        task.retried = task_data["retried"]
        task.retries = task_data["retries"]
        task.worker = events_state.Worker(task_data["worker"]) if task_data["worker"] else None
        task.traceback = task_data["traceback"]

    for worker_data in data["workers"]:
        worker = events_state.workers.get(worker_data["name"])
        if not worker:
            worker = events_state.Worker(worker_data["name"])
            events_state.workers[worker_data["name"]] = worker

        worker.hostname = worker_data["hostname"]
        worker.pid = worker_data["pid"]
        worker.freq = worker_data["freq"]
        worker.heartbeats = worker_data["heartbeats"]
        worker.clock = worker_data["clock"]
        worker.active = worker_data["active"]
        worker.processed = worker_data["processed"]
        worker.loadavg = worker_data["loadavg"]
        worker.sw_ident = worker_data["sw_ident"]
        worker.sw_ver = worker_data["sw_ver"]
        worker.sw_sys = worker_data["sw_sys"]
