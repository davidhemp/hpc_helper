import curses
import subprocess
from nsd import nsd_requests, nsd_waiters
import slurm

def curses_draw(scr, row, col, data_dic, node_map, node_status):
    for key, value in data_dic.items():
        if "violet" not in node_map[key]:
            if sum(value) > 0 and row < 45:
                scr.addstr(row, col, "{} : {}     ".format(node_map[key], sum(value)), curses.A_NORMAL)
                scr.addstr(row, col+20, "{} : {:.2f}     ".format(node_map[key], sum(value)/len(value)), curses.A_NORMAL)
                user_str = "".ljust(40, ' ')
                if "blue" not in node_map[key] and "cyan" not in node_map[key]:
                    node_name = node_map[key]
                    user_str = ", ".join(node_status[node_name]["users"]).ljust(45, ' ')
                scr.addstr(row, col+40, "{}".format(user_str), curses.A_NORMAL)
                row += 1
            else: return

def main_loop(scr, *args):
    # Set up scene
    scr.border(0)
    scr.nodelay(1)
    curses.cbreak()
    scr.addstr(3, 5, 'NSD requests and waiters for each node.', curses.A_BOLD)
    scr.addstr(5, 5, 'Data is based on a rolling 60 second window.', curses.A_NORMAL)
    scr.addstr(6, 5, 'ctrl-c or q to exit', curses.A_NORMAL)

    # mmfsadm is used to build the node map, e.g. <c1n41> = indigo55
    rtn = subprocess.check_output(["mmfsadm", "dump", "cfgmgr"]).decode().split("\n")
    node_map = {}
    for line in rtn:
        if "<c1n" in line[:20]:
            #Need to remove the <c1 or <c0. I assume this is related inbound and outofbound calls.
            node_id = line.split()[1][3:-1]
            node_map[node_id] = line.split()[2]

    requests = {}
    waiters = {}
    n = 0
    while True:
        #Get count nsd requests on each dssg node
        requests = nsd_requests(requests)
        #Get count of nsd waiters for each dssg node
        waiters = nsd_waiters(waiters)

        if n%60 == 0:
            node_status = slurm.get_node_status()
        n += 1
        # Fancy output
        #Left col for requests
        scr.addstr(8, 5, "NSD requests", curses.A_NORMAL)
        scr.addstr(9, 5, "Total", curses.A_NORMAL)
        scr.addstr(9, 25, "Per Second", curses.A_NORMAL)
        curses_draw(scr, 11, 5, requests, node_map, node_status )

        #right col for waiters
        scr.addstr(8, 100, "NSD waiters", curses.A_NORMAL)
        scr.addstr(9, 100, "Total", curses.A_NORMAL)
        scr.addstr(9, 125, "Per Second", curses.A_NORMAL)
        curses_draw(scr, 11, 100, waiters, node_map, node_status)

        # wait 1 second to prevent spamming dssg's
        curses.napms(1000)
        ch = scr.getch()
        if ch == ord('q'):
            break

if __name__ == "__main__":
    try:
        curses.wrapper(main_loop)
    except KeyboardInterrupt:
        pass
