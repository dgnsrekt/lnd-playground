from multiprocessing import Process
from paths import LND_PATH, LNCLI_PATH
from os import system

# https://lyceum-allotments.github.io/2017/03/python-and-pipes-part-6-multiple-subprocesses-and-pipes/
def run_lnd(directory):
    system(
        f"{LND_PATH} --bitcoin.active --bitcoin.testnet"
        " --debuglevel=info --bitcoin.node=neutrino"
        " --neutrino.connect=faucet.lightning.community"
        f" --lnddir={directory}"
    )


for d in ["nodes/alice/.lnd", "nodes/bob/.lnd"]:
    p = Process(target=run_lnd, args=(d,))
    p.start()
p.join()
