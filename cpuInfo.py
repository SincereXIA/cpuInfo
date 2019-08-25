from mointor import Mointor
from datetime import datetime
import psutil
import time
import socket
import fcntl
import struct

class CPUInfo(object):
    _time_format_style_ = "%y-%m-%d %H:%M"
    _mointor_ = Mointor()

    def __init__(self):
        self.home_page()

    def _get_date_time_(self)->str:
        today = datetime.today()
        return today.strftime(self._time_format_style_)
    def _get_uptime_(self)->str:
        delta_time = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        delta_time = str(delta_time)
        return delta_time[0:delta_time.rfind(':')]


    def _get_ip_address_(self):
        info = psutil.net_if_addrs()['wlan0'][0]
        return info.address

    def _get_cpu_tmp_(self):
        return str(psutil.sensors_temperatures()['cpu-thermal'][0].current)
    def _get_cpu_load_(self):
        return str(psutil.getloadavg())


    def home_page(self):
        self._mointor_.setfont("pixelmix.ttf", 8)
        self._mointor_.println(self._get_date_time_())
        self._mointor_.println("UpTime: " + self._get_uptime_())
        self._mointor_.println(self._get_ip_address_())
        self._mointor_.println("temp: "+ self._get_cpu_tmp_())
        self._mointor_.println(self._get_cpu_load_())

if __name__ == '__main__':
    cpuinfo = CPUInfo()
    while True:
        cpuinfo.home_page()
