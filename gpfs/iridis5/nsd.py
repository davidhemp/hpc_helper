import subprocess

def build_dictionary(temp_dict, return_dict):
    max_length = 60
    for nodeid in temp_dict.keys():
        if nodeid in return_dict.keys() :
            return_dict[nodeid].append(temp_dict[nodeid])
            if len(return_dict[nodeid]) > max_length:
                 return_dict[nodeid].pop(0)
        else:
            return_dict[nodeid] = [temp_dict[nodeid]]
    for nodeid in return_dict.keys():
        if nodeid not in temp_dict.keys():
            return_dict[nodeid].append(0)
            if len(return_dict[nodeid]) > max_length:
                 return_dict[nodeid].pop(0)
    # Sort by the last value
    try:
        del return_dict["0x01000000"]
    except KeyError:
        pass
    return_dict = {k: v for k, v in sorted(return_dict.items(), key=lambda item: sum(item[1]), reverse=True)}
    return return_dict

def nsd_requests(requests={}):
    temp_requests = {}
    for dssg in ["violet55", "violet56"]:
        rtn = subprocess.check_output(["ssh", dssg, "mmfsadm", "dump", "nsd"]).decode().split("\n")
        for line in rtn:
            if "nsdId" in line:
                nodeid = line.split()[7].strip(",")[3:-1]
                if nodeid in temp_requests.keys():
                    temp_requests[nodeid] += 1
                else:
                    temp_requests[nodeid] = 1
    return build_dictionary(temp_requests, requests)


def nsd_waiters(waiters={}):
    temp_waiters = {}
    max_length = 60
    for dssg in ["violet55", "violet56"]:
        rtn = subprocess.check_output(["ssh", dssg, "mmfsadm", "dump", "waiters"]).decode().split("\n")
        for line in rtn:
            if 'RDMA' in line:
                nodeid = line.split()[17].strip(",")[3:-1]
                if nodeid in temp_waiters.keys():
                    temp_waiters[nodeid] += 1
                else:
                    temp_waiters[nodeid] = 1
    return build_dictionary(temp_waiters, waiters)
