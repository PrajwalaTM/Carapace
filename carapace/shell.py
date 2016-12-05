import sys
import shlex
import os
from carapace.constants import *
from carapace.builtins import *

built_in_cmds = {}

# Register a built-in function to built-in command hash map
def register_command(name, func):
    built_in_cmds[name] = func

# Register all built-in commands here
def init():
    register_command("cd", cd)
    register_command("exit", exit)
    register_command("history", history)
    register_command("prev",prev)


def shell_loop():
    # Start the loop here
    status = SHELL_STATUS_RUN
    flag=1
    while status == SHELL_STATUS_RUN:
        # Display a command prompt
        if(flag==1):
        	sys.stdout.write("Welcome to Carapace!\n Type prev <line_num> to view the line_num th previous command.\n All standard unix commands are available.\n")
        	flag=0
        sys.stdout.write('> ')
        sys.stdout.flush()

        # Read command input
        cmd = sys.stdin.readline()
        
        cmd_tokens = tokenize(cmd)
        status = execute(cmd_tokens)


def tokenize(string):
    return shlex.split(string)


def execute(cmd_tokens):
    # Fork a child shell process
    # If the current process is a child process, its `pid` is set to `0`
    # else the current process is a parent process and the value of `pid`
    # is the process id of its child process.
    # Extract command name and arguments from tokens
    with open(HISTORY_PATH, 'a') as history_file:
        history_file.write(' '.join(cmd_tokens) + os.linesep)

    cmd_name = cmd_tokens[0]
    cmd_args = cmd_tokens[1:]
    #if (cmd_name=='\027[A'):
   # sys.stdout.write(cmd_name)
    # If the command is a built-in command, invoke its function with arguments
    if cmd_name in built_in_cmds:
        return built_in_cmds[cmd_name](cmd_args)


    pid = os.fork()

    if pid == 0:
    # Child process
        # Replace the child shell process with the program called with exec
        os.execvp(cmd_tokens[0], cmd_tokens)
    elif pid > 0:
    # Parent process
        while True:
            # Wait response status from its child process (identified with pid)
            wpid, status = os.waitpid(pid, 0)

            # Finish waiting if its child process exits normally
            # or is terminated by a signal
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break

    # Return status indicating to wait for next command in shell_loop
    return SHELL_STATUS_RUN

def main():
	init()
	shell_loop()


if __name__ == "__main__":
    main()

