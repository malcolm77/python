
import requests


def get_gpu():
  url = requests.get("http://mcpc:9835/metrics")
  for line in url.text.splitlines():
    if "nvidia_smi_utilization_gpu_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
      try:
        print(line)
        # gpu = float(line[-4:])*100
        gpu = int(line[-2:])
        # print(str(gpu) + "%" )
      except:
        gpu = 0
  return str(gpu) + " %"


def get_gtemp():
  url = requests.get("http://mcpc:9835/metrics")
  for line in url.text.splitlines():
    if "nvidia_smi_temperature_gpu{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
      try:
        print(line)
        gtemp = int(line[-2:])
      except:
        gtemp = 0
  return str(gtemp) + " C"

# nvidia_smi_fan_speed_ratio
def get_gfan():
  url = requests.get("http://mcpc:9835/metrics")
  for line in url.text.splitlines():
    if "nvidia_smi_fan_speed_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
      try:
        print(line)
        gtemp = int(line[-2:])
      except:
        gtemp = 0
  return str(gtemp) + " %"

print(get_gpu())
print(get_gtemp())
print(get_gfan())


