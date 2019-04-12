import json
import time
import re
import sys
import subprocess



def get_logsets(logset_id):
    cmd1 = ["lecli", "get", "logset", logset_id]
    logset = subprocess.check_output(cmd1)

    return json.loads(logset)


def get_required_logs(log_prefix, log_suffix, logset_data):
    logs_to_delete = []
    logset = logset_data["logset"]
    logsinfo = logset["logs_info"]
    if len(logsinfo) > 0:
        for logs in logsinfo:
            if re.match(log_prefix,logs["name"]) and logs["name"].endswith(log_suffix):
                logs_to_delete.append(logs)
    else:
        print "No logs found under given logset"
        return 0

    return logs_to_delete


def delete_logs(logs_to_delete, dry_run=False):
    dry_output = []
    if len(logs_to_delete)> 0:
        if dry_run:
            print "Running in dry mode"
            for l in logs_to_delete:
                dry_output.append(l["name"])
            print "Logs to delete %s " % dry_output

        else:
            for l in logs_to_delete:
                print "Logs to delete %s - id : %s" % (l["name"], l["id"])
                cmd1 = ["lecli", "delete", "log", l["id"]]
                try:
                    out = subprocess.check_output(cmd1)
                    print "sleeping for 2 second"
                    time.sleep(1)
                except subprocess.CalledProcessError as grepexc:
                    print "error code", grepexc.returncode, grepexc.output

    else:
        print "No logs found with given prefix and suffix"
        return 1


if __name__=="__main__":
    if len(sys.argv) < 3:
        print "Either logsetid or log prefix or log suffic is missing"
        print "Example python log_set.py <log-setid> <test-pool-*> <quadra>"
        print "This will get all the logs with given prefix and suffix under given log set id"
        exit(1)

    data = get_logsets(sys.argv[1])
    logs_to_delete = get_required_logs(sys.argv[2], sys.argv[3], data)
    delete_logs(logs_to_delete, dry_run=False)
