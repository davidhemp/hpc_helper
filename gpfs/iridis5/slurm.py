import subprocess

def decode_node_list(node_str):
    """ Converts the output from Slurm into a full list of nodes for that job"""
    node_list = []
    if "[" in node_str:
        prefix = node_str.split("[")[0]
        just_node_numbers = node_str.split("[")[1].strip("[]")
        for node_numbers in just_node_numbers.split(","):
            if "-" in node_numbers:
                # Convert a node range into a list.
                node_range = node_numbers.split("-")
                for i in range(int(node_range[0]), int(node_range[1])+1, 1):
                    node_name = prefix + str(i).rjust(len(node_range[0]), '0')
                    node_list.append(node_name)
            else:
                node_list.append(prefix + node_numbers)
    else:
        node_list = [node_str]
    return node_list

def get_node_status():
    """Converts the squeue output for running jobs into a dictionary.
    Output: dict [dict, set]
        Primary key is the node name. Each element has dictionary for the jobs running
        and a set of the users using that node. dict[node_name] = [jobids, users]
    """
    # Build an empty dictionary with all known nodes.
    all_nodes = subprocess.check_output(["sinfo", "-o%N", "-h"]).decode().strip("\n")
    node_status = {}
    for node_range in all_nodes.split(","):
        node_list = decode_node_list(node_range)
        for node in node_list:
            node_status[node] = {"jobids" : [], "users" : set()}

    # Update the status of all running nodes to include jobs and usernames
    data = subprocess.check_output(["squeue", "-t", "running", "-h"]).decode()

    for line in data.split("\n")[:-1]:
        node_list = decode_node_list(line.split()[7])
        jobid = line.split()[0]
        user = line.split()[3]
        for node in node_list:
            node_status[node]["jobids"].append(jobid)
            node_status[node]["users"].add(user)
    return node_status
