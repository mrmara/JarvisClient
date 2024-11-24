from src.jclient import jclient
j = jclient(test=True)
while True:
    cmd = input("Write command\n")
    print(f"commanding {cmd}")
    j.invoke_command(cmd)