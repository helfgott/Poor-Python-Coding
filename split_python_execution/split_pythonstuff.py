# miguel.ortiz
# answer for: https://stackoverflow.com/questions/52373206/start-two-shell-sudo-scripts-in-two-different-terminals-from-python3

import subprocess


subprocess.call(['gnome-terminal', '-x', 'python', '/home/mortiz/Documents/projects/python/split_python_execution/script1.py'])
subprocess.call(['gnome-terminal', '-x', 'python', '/home/mortiz/Documents/projects/python/split_python_execution/script2.py'])

