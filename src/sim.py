import subprocess

def terminated_read(fd): #read input() prompts as well until \0
    text = []
    while True:
        r = fd.read(1)
        if r == "\0":
            break
        text += r
        
    return ''.join(text)

log = open("simlog.txt", "wt")
proc= subprocess.Popen(["/Library/Frameworks/Python.framework/Versions/3.10/bin/python3", "tester.py"],
                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)



