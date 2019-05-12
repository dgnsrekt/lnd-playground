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
        f"{LND_PATH}",
        "--bitcoin.active",
        "--bitcoin.testnet",
        "--bitcoin.node=neutrino",
        "--neutrino.connect=faucet.lightning.community",
        f"--lnddir={node_folder}",
        f"--listen=localhost:{port}",
        f"--rpclisten=localhost:{rpcport}",
        f"--restlisten=localhost:{restport}",
        # "--no-macaroons",
        "--debuglevel=debug",
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
    procs.append(subprocess.Popen(cmd, stdout=subprocess.PIPE))

while True:
    for proc in procs:
        name = proc.args[5].split("/")[-2]
        proc.poll()
        line = str(proc.stdout.readline())
        print(f"{name}: ", line)
        if proc.returncode:
            proc.terminate()

for proc in procs:
    proc.terminate()

exit()

fldr = create_node_folder("alice")
lnd_cmd_alice = create_node_command(fldr, 9000, 10000, 8000)
fldr = create_node_folder("bob")
lnd_cmd_bob = create_node_command(fldr, 9001, 10001, 8001)

alice = subprocess.Popen(lnd_cmd_alice, stdout=subprocess.PIPE)
bob = subprocess.Popen(lnd_cmd_bob, stdout=subprocess.PIPE)

log.info("running Node...")
while True:
    alice.poll()
    bob.poll()
    line_a = str(alice.stdout.readline())
    line_b = str(bob.stdout.readline())
    print("alice:", line_a)
    print("bob:", line_b)
    # print("errors:", alice.errors)
    # print("returncode:", alice.returncode)
    if alice.returncode:
        alice.terminate()
        break
    if bob.returncode:
        bob.terminate()
        break

alice.terminate()
bob.terminate()

# try:
#     for line in iter(proc.stdout.readline, ""):
#         log.debug(clean_line(line))
#         if LOGLEVEL > 10:
#             print(".", end="", flush=True)
#         if SYNCED_LOG_LINE in str(line):
#             print()
#             log.info("node appears fully synced. shutting down...")
#             sleep(5)
#             proc.terminate()
#             proc.kill()
#             break
#     print()
# except (KeyboardInterrupt, SystemExit):
#     print("\nexiting removing master node")
#     shutil.rmtree(MASTER_NODE_LNDDIR_PATH, ignore_errors=True)
#     raise
#
# paths_to_remove = [MASTER_NODE_LND_DATAGRAPH, MASTER_NODE_LND_LOGS]
# for path in paths_to_remove:
#     if path.exists():
#         log.debug(f"removing {path}")
#         shutil.rmtree(path, ignore_errors=True)
#
# files_to_remove = [MASTER_NODE_TLS_KEY, MASTER_NODE_TLS_CERT]
# for file in files_to_remove:
#     if file.exists():
#         log.debug(f"removing {file}")
#         file.unlink()
