import os, sys, threading, time
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants
import psutil
import atexit

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
        self.warned = False

    def warn(self):
        truncated = "%d" % (int(self.current_cpu_usage),)
        message = CPUMonitor.message % (truncated,)
        os.system(constants.DISPLAY_NOTIFICATION % (message,))

    def monitor(self):
        self.running = True
        while self.running:
            self.current_cpu_usage = psutil.cpu_percent()
            if self.current_cpu_usage > CPUMonitor.threshold:
                if not self.warned:
                    self.warn()
                    self.warned = True
            else:
                self.warned = False
            time.sleep(1)

    def stop(self):
        self.running = False

class MemoryMonitor(Monitor):

    message = "Your memory usage is %s percent"
    threshold = 80

    def __init__(self):
        self.running = False
        self.warned = False

    def warn(self):
        truncated = "%d" % (int(self.current_mem_usage),)
        message = MemoryMonitor.message % (truncated,)
        os.system(constants.DISPLAY_NOTIFICATION % (message,))

    def monitor(self):
        self.running = True
        while self.running:
            self.current_mem_usage = psutil.virtual_memory()[2]
            if self.current_mem_usage > MemoryMonitor.threshold:
                if not self.warned:
                    self.warn()
                    self.warned = True
            else:
                self.warned = False
            time.sleep(1)

    def stop(self):
        self.running = False

class TempMonitor(Monitor):

    message = "Your temperature usage is %s percent"
    threshold = 70

    def __init__(self):
        self.running = False
        self.warned = False
        self.temp_file = open("/sys/class/thermal/thermal_zone0/temp", 'r')

    def warn(self):
        truncated = "%d" % (int(self.current_temp),)
        message = MemoryMonitor.message % (truncated,)
        os.system(constants.DISPLAY_NOTIFICATION % (message,))

    def monitor(self):
        self.running = True
        while self.running:
            self.temp_file.seek(0)
            temp_str = self.temp_file.read().strip()
            self.current_temp = int(temp_str) / 1000
            if self.current_temp > TempMonitor.threshold:
                if not self.warned:
                    self.warn()
                    self.warned = True
            else:
                self.warned = False
            time.sleep(1)

    def stop(self):
        self.running = False
        self.temp_file.close()

monitor_threads = {}
cpu_mon = None
mem_mon = None
temp_mon = None

def start():
    global monitor_threads, cpu_mon, mem_mon, temp_mon

    if len(monitor_threads) > 0:
        return

    cpu_mon = CPUMonitor()
    mem_mon = MemoryMonitor()
    temp_mon = TempMonitor()

    monitor_threads["cpu_mon"] = threading.Thread(target=cpu_mon.monitor)
    monitor_threads["mem_mon"] = threading.Thread(target=mem_mon.monitor)
    monitor_threads["temp_mon"] = threading.Thread(target=temp_mon.monitor)

    for thread in monitor_threads:
        monitor_threads[thread].daemon = True
        monitor_threads[thread].start()

def stop():
    global cpu_mon, mem_mon, temp_mon

    cpu_mon.stop()
    mem_mon.stop()
    temp_mon.stop()

