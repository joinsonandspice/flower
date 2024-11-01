import json

from flower.events import EventsState

def export_tasks_and_workers(events_state: EventsState):
    data = {
        "tasks": []
    }

    for _, task in events_state.tasks.items():
        task_data = task.as_dict()
        task_data['worker'] = task.worker.hostname if task.worker else None
        data["tasks"].append(task_data)
    # for worker_name, worker in events_state.workers.items():
    #     data["workers"].append({
    #         "name": worker_name,
    #         "hostname": worker.hostname,
    #         "pid": worker.pid,
    #         "freq": worker.freq,
    #         "heartbeats": worker.heartbeats,
    #         "clock": worker.clock,
    #         "active": worker.active,
    #         "processed": worker.processed,
    #         "loadavg": worker.loadavg,
    #         "sw_ident": worker.sw_ident,
    #         "sw_ver": worker.sw_ver,
    #         "sw_sys": worker.sw_sys
    #     })

    return json.dumps(data)

def import_tasks_and_workers(events_state: EventsState, data):


    for task_data in data["tasks"]:
        task_id = task_data["uuid"]

        if not task_id:
            print("Importing task with no id, skipping")
            continue

        (task, is_new) = events_state.get_or_create_task(task_data["uuid"])
        if is_new:
            for field in task._fields:
                setattr(task, field, task_data.get(field))
            

            if task_data["worker"]:
                (worker, _) = events_state.get_or_create_worker(task_data["worker"])
                task.worker = worker


    # for worker_data in data.get("workers", []):
    #     worker = events_state.workers.get(worker_data["name"])
    #     if not worker:
    #         worker = events_state.Worker(worker_data["name"])
    #         events_state.workers[worker_data["name"]] = worker

    #     worker.hostname = worker_data["hostname"]
    #     worker.pid = worker_data["pid"]
    #     worker.freq = worker_data["freq"]
    #     worker.heartbeats = worker_data["heartbeats"]
    #     worker.clock = worker_data["clock"]
    #     worker.active = worker_data["active"]
    #     worker.processed = worker_data["processed"]
    #     worker.loadavg = worker_data["loadavg"]
    #     worker.sw_ident = worker_data["sw_ident"]
    #     worker.sw_ver = worker_data["sw_ver"]
    #     worker.sw_sys = worker_data["sw_sys"]

