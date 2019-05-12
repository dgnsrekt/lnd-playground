import prompt_toolkit
from lnd_grpc.lnd_grpc import Client
from random import choice

from names import NAMES
from paths import NODE_PATH

from time import sleep


def check_name_valid(name):
    if name in NAMES:
        return True
    return False


def get_node_index(name):
    return NAMES.index(name)


def get_node_ports(idx):
    port = 9000 + idx
    rpcport = 10000 + idx
    restport = 8000 + idx
    return port, rpcport, restport


def get_node_folder_location(name):
    folder = NODE_PATH / name / ".lnd"
    return folder


def get_node_cert_location(lnd_path):
    path = lnd_path / "tls.cert"
    print(path, path.exists())
    return path


def get_node_admin_macaroon(lnd_path):
    return lnd_path / "data" / "chain" / "bitcoin" / "testnet" / "admin.macaroon"


# name = choice(NAMES)
name = "alice"

if check_name_valid(name):
    index = get_node_index(name)
    folder = get_node_folder_location(name)
    tls_cert = str(get_node_cert_location(folder))
    macaroon = str(get_node_admin_macaroon(folder))
    port, rpcport, restport = get_node_ports(index)
    print(name, index, port, rpcport, restport)
    print(tls_cert)
    client = Client(
        lnd_dir=str(folder),
        tls_cert_path=tls_cert,
        grpc_port=str(rpcport),
        network="testnet",
        macaroon_path=macaroon,
    )
    # client.init_wallet(wallet_password="password")
    # client.unlock_wallet()
    # client.unlock_wallet(wallet_password="password")
    print(client.get_info())

else:
    raise KeyError(f"{node_arg} does not exist.")
