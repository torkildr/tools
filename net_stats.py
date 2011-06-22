#!/opt/bin/python2.4

import time

output_file = "transfer.txt"
raw_file = "stats.txt"

file_headers = ["bytes", "packets", "errs", "drop", "fifo", "frame", "compressed", "multicast"]

def extract_info(file):
    f = open(file, "r")

    stats = {}

    for line in f:
        dev_line = line.split(":")

        if len(dev_line) > 1:
            rx = {}
            tx = {}

            i=0
            for value in dev_line[1].split():
            	int_value = 0
                try:
                    int_value = int(value)
                except:
                	pass

                field = file_headers[i % len(file_headers)]

                if i < len(file_headers):
                    rx[field] = int_value
                else:
                	tx[field] = int_value

                i += 1

            dev = dev_line[0].strip()
            stats[dev] = {}

            stats[dev]["rx"] = rx
            stats[dev]["tx"] = tx

    f.close()
    return stats

def byteToReadable(bytes):
    labels = ["B", "kB", "MB", "GB", "TB"]

    exp = 0
    for label in labels:
        if bytes < 1024**(exp+1) or label == labels[-1]:
        	return "%.2f %s" % (float(bytes) / 1024**exp, label)
        exp += 1

def save_info(file, info):
    f = open(file, "a")

    up = byteToReadable(info["eth0"]["tx"]["bytes"])
    down = byteToReadable(info["eth0"]["rx"]["bytes"])

    date = time.strftime("%d.%m.%Y %H:%M")

    f.write("%-30s %-20s %-20s\n" % (date, "Up: %s" % up, "Down: %s" % down))

    f.close()

def raw_info(file, info):
    f = open(file, "a")

    up = info["eth0"]["tx"]["bytes"]
    down = info["eth0"]["rx"]["bytes"]

    date = time.time()

    f.write("%f;%d;%d\n" % (date, up, down))

    f.close()

if __name__ == "__main__":
    info = extract_info("/proc/net/dev")
    save_info(output_file, info)
    raw_info(raw_file, info)

