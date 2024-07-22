# main.py
import sys

if __name__ == "__main__":
    if len(sys.argv) >= 0:
      print(f"Arguments count: {len(sys.argv)}")
      for i, arg in enumerate(sys.argv):
          print(f"Argument {i:>6}: {arg}")
      # print (sys.argv[1])
