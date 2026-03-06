import os
import sys

with open('env_check.txt', 'w') as f:
    f.write(f"CWD: {os.getcwd()}\n")
    f.write(f"Python: {sys.executable}\n")
    f.write(f"Files: {os.listdir('.')}\n")
