"""
Module for reading and validating the network configuration file.
"""
from schema import Schema, SchemaError, Optional
import yaml

from nettool import log


CONFIG_SCHEMA = Schema({
    "nodes": [
        {"name": str,
         "identity_chain_id": str,
         "server_priv_key": str,
         "server_public_key": str,
         Optional("seed"): bool}
    ]
})


def read_file(config_path):
    """
    Reads the network setup from the config file.
    """
    cfg = _read_yaml(config_path)
    _validate_schema(cfg)
    return NetworkConfig(cfg)


def _read_yaml(path):
    with open(path) as net_file:
        return yaml.load(net_file)


def _validate_schema(cfg):
    try:
        CONFIG_SCHEMA.validate(cfg)
    except SchemaError as exc:
        log.fatal(exc)


class NetworkConfig(object):
    """
    An object holding the configuration for the network.
    """

    def __init__(self, cfg):
        self.nodes = [NodeConfig(node_cfg) for node_cfg in cfg["nodes"]]


class NodeConfig(object):
    """
    An object holding the configuration for the network node.
    """

    def __init__(self, cfg):
        self.name = cfg["name"]
        self.identity_chain_id = cfg["identity_chain_id"]
        self.server_priv_key = cfg["server_priv_key"]
        self.server_public_key = cfg["server_public_key"]
        self.seed = cfg.get("seed", False)