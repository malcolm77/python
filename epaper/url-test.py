import requests

def get_gpu_info():
  gpu_info = [-1,-1,-1]
  try:
    url = requests.get("http://mcpc:9835/metrics",timeout=5)
    for line in url.text.splitlines():
      if "nvidia_smi_utilization_gpu_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
        try:
          gpu_info[0] = int(line[-2:])   # attempt to convert the last 2 characters of the line to an int
        except:
          gpu_info[0] = 0                # if that fails, then make the value 0 instead
      elif "nvidia_smi_temperature_gpu{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
        try:
          gpu_info[1]= int(line[-2:])
        except:
          gpu_info[1]= 0
      elif "nvidia_smi_fan_speed_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
        try:
          gpu_info[2] = int(line[-2:])
        except:
          gpu_info[2] = 0
  except:
    gpu_info = [-1,-1,-1]
   
  return gpu_info


print (get_gpu_info())

