import subprocess

def nsd_waiters(waiters=[{},{}]):
    for dssg in ["violet55", "violet56"]:
        rtn = subprocess.check_output(["ssh", dssg, "mmfsadm", "dump", "waiter"]).decode().split("\n")
        for line in rtn:
            if "RDMA" in line:
                mode = line.split()[11]
                nodeid = line.split()[17][3:-1]
                try:
                    waiters[0][nodeid] += 1
                except KeyError:
                    waiters[0][nodeid] = 1
    waiters[0] = {k: v for k, v in sorted(waiters[0].items(), key=lambda item: item[1], reverse=True)}
    return waiters

if __name__ == "__main__":
    n = 0
    while n < 10:
        waiters = nsd_waiters()
        print(waiters)
        n += 1
