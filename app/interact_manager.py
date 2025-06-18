import subprocess
import threading
import re
import json
from datetime import datetime
from collections import defaultdict

# Track sessions per URL
sessions = {}
sessions_lock = threading.Lock()  # thread-safe access

def start_interactsh_session(user_id):
    proc = subprocess.Popen(
        ['interactsh-client'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        shell=True
    )

    url = None

    for line in proc.stdout:
        # print(f"[DEBUG] {line.strip()}", flush=True)  # DEBUG: Show output
        match = re.search(r'([a-z0-9]+\.oast\.\w+)', line.strip())
        if match:
            url = match.group(1)
            print(f"[INFO] Interactsh URL extracted: {url}", flush=True)
            break


    if not url:
        raise Exception("Could not get Interactsh URL")

    with sessions_lock:
        sessions[url] = {
            'user': user_id,
            'proc': proc,
            'interactions': []
        }

    threading.Thread(target=track_logs, args=(url, proc), daemon=True).start()
    return url



def track_logs(url, proc):
    for line in proc.stdout:
        try:
            data = json.loads(line.strip())

            if 'remote-address' in data and 'timestamp' in data:
                ip = data['remote-address']
                timestamp = data['timestamp']

                # Save interaction
                with sessions_lock:
                    sessions[url]['interactions'].append({
                        'ip': ip,
                        'timestamp': timestamp
                    })
        except json.JSONDecodeError:
            continue


def get_interactions(url, from_ts=None, to_ts=None):
    with sessions_lock:
        interactions = sessions.get(url, {}).get('interactions', [])

    if from_ts and to_ts:
        try:
            from_dt = datetime.strptime(from_ts, "%Y-%m-%d %H:%M:%S")
            to_dt = datetime.strptime(to_ts, "%Y-%m-%d %H:%M:%S")
            return [
                i for i in interactions
                if from_dt <= datetime.strptime(i['timestamp'], "%Y-%m-%d %H:%M:%S") <= to_dt
            ]
        except Exception as e:
            print(f"[ERROR] Timestamp parsing failed: {e}")
            return []
    
    return interactions
