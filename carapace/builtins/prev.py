import os
import sys
from carapace.constants import *

def prev(args):
	num=1

	if len(args) > 0:
		num = int(args[0])
		with open(HISTORY_PATH, 'r') as history_file:
			lines = history_file.readlines()
			line_num=len(lines)-num-1
			if(line_num)<=0:
				sys.stdout.write("Invalid argument\n")
			else :
				sys.stdout.write(lines[line_num])

	sys.stdout.flush()		
	return SHELL_STATUS_RUN