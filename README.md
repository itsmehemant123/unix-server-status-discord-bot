## Server Info bot

### Setup

- Install dependencies with:

```bash
pip install -r requirements.txt
```

- Create `auth.json`, and place it inside the `config` folder. Its content should be:

```json
{
   "token": "<your_token>"
}
```

### How to run

- Run the script with:

```bash
python serverstatus_client.py
```

### Command (s)

- Show the GPU Usage with:
```
!gpuinfo
```
- Show the CPU and RAM Usage with:
```
!info
```
- Show the logged in users with
```
!users
```

### Improvements

- Show running processes.
```python
for proc in nvmlDeviceGetComputeRunningProcesses(handle):
   print(
      "pid %d using %d bytes of memory on device %d."
      % (proc.pid, proc.usedGpuMemory, dev_id)
   )
   proc_stat_file = os.stat("/proc/%d" % pid)
   # get UID via stat call
   uid = proc_stat_file.st_uid
   # look up the username from uid
   username = pwd.getpwuid(uid)[0]
```
- As of now, it just assumes NVidia GPU and the presence of `nvidia-smi`.