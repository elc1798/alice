import os, sys, threading, time
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, ".."))
import commands as COMMANDS
import psutil

class Monitor:

    def __init__(self):
        pass

    def warn(self):
        pass

    def monitor(self):
        pass

class CPUMonitor(Monitor):

    message = "Your CPU usage is %s percent"
    threshold = 80

    def __init__(self):
        self.running = False

    def warn(self):
        truncated = "%d" % (int(self.current_cpu_usage),)
        message = CPUMonitor.message % (truncated,)
        os.system(COMMANDS.SAY % (message,))

    def monitor(self):
        self.running = True
        while self.running:
            self.current_cpu_usage = psutil.cpu_percent()
            if self.current_cpu_usage > CPUMonitor.threshold:
                self.warn()
            time.sleep(1)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    cpu_mon = CPUMonitor()
    cpu_mon.monitor()
else:
    monitor_threads = {}
    cpu_mon = CPUMonitor()

    monitor_threads["cpu_mon"] = threading.Thread(target=cpu_mon.monitor)

    for thread in monitor_threads:
        monitor_threads[thread].daemon = True
        monitor_threads[thread].start()

