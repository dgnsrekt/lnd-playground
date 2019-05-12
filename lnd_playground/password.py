from paths import NODE_PATH, LND_PATH, LNCLI_PATH, MASTER_NODE_PATH
import shutil
import subprocess
from time import sleep

import logme

log = logme.log(scope="module", name="node_runner")
LOGLEVEL = log.logger.master_level


def create_node_folder(path):
    node_folder = path / ".lnd"
    return node_folder


def create_node_command(node_folder, port, rpcport, restport):
    lnd_cmd = [
        f"{LNCLI_PATH}",
        f"--lnddir={node_folder}",
        "--network=testnet",
        # "--bitcoin.active",
        # "--bitcoin.testnet",
        # "--bitcoin.node=neutrino",
        # "--neutrino.connect=faucet.lightning.community",
        # f"--listen=localhost:{port}",
        f"--rpcserver=localhost:{rpcport}",
        # f"--restlisten=localhost:{restport}",
        # "--no-macaroons",
        # "--debuglevel=debug",
        # "getinfo",
        "create",
    ]
    print(lnd_cmd)
    return lnd_cmd


def clean_line(line):
    lines = str(line).split(" ")
    cleaned = " ".join(lines[2:])
    return cleaned


procs = list()
nodes = [n for n in NODE_PATH.glob("*") if n != MASTER_NODE_PATH]
nodes = list(sorted(nodes))
for idx, node_loc in enumerate(nodes):
    folder = create_node_folder(node_loc)
    port = 9000 + idx
    rpcport = 10000 + idx
    restport = 8000 + idx
    cmd = create_node_command(folder, port, rpcport, restport)
    print(" ".join(cmd))
    # procs.append(subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE))
exit()
while True:
    for proc in procs:
        name = proc.args[1].split("/")[-2]
        proc.poll()
        line = str(proc.stdout.readline())
        proc.stdin.write(b"password")
        # print(f"{name}: ", line)
        break
        # if proc.returncode:
        # proc.terminate()
    print(name)
    break

for proc in procs:
    proc.terminate()
