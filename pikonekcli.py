#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import yaml

sys.path.append('/etc/pikonek/pikonek/')

from pikonek.netconfig import main as NetConfig
from pikonek.wireless import main as WirelessConfig
from pikonek.dhcp import main as DhcpConfig
from pikonek.admin import main as Admin
from pikonek.core import main as CoreConfig
from pikonek.captive import main as CaptiveConfig
from pikonek.config import Config

logger = logging.getLogger(__name__)
_PIKONEK_NET_MAP_FILE =  '{}pikonek_net_mapping.yaml'.format(Config.PIKONEK_CONFIG_PATH)
_PIKONEK_DHCP_FILE =  '{}pikonek_dhcp_mapping.yaml'.format(Config.PIKONEK_CONFIG_PATH)
_PIKONEK_WPA_FILE =  '{}pikonek_wpa_mapping.yaml'.format(Config.PIKONEK_CONFIG_PATH)
_PIKONEK_CORE_FILE = '{}pikonek.yaml'.format(Config.PIKONEK_CONFIG_PATH)

def parse_opts(argv):
    parser = argparse.ArgumentParser(
        description='Configure host network interfaces using a JSON'
        ' config file format.')
    parser.add_argument('-p', '--password', metavar='PASSWORD')
    parser.add_argument('-d', '--dhcp', metavar='DHCP CONFIG FILE')
    parser.add_argument('-n', '--network', metavar='NETWORK CONFIG FILE')
    parser.add_argument('-w', '--wpa', metavar='WPA CONFIG FILE')
    parser.add_argument('-c', '--core', metavar='CORE CONFIG FILE')
    parser.add_argument('-r', '--rule', metavar='CAPTIVE FIREWALL RULE')

    opts = parser.parse_args(argv[1:])

    return opts


def configure_logger(verbose=False, debug=False):
    LOG_FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
    DATE_FORMAT = '%Y/%m/%d %I:%M:%S %p'
    log_level = logging.WARN

    if debug:
        log_level = logging.DEBUG
    elif verbose:
        log_level = logging.INFO

    logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT,
                        level=log_level)

def main(argv=sys.argv):
    opts = parse_opts(argv)
    configure_logger(False, False)

    if opts.password:
        logging.info("Saving new password...")
        response = Admin.change_password(password=opts.password)
        if response == 1:
            logging.info("Error on saving new password.")
            return 1
    if opts.dhcp:
        logging.info("Configuring dhcp server, dnsmasq...")
        response = DhcpConfig.configure(config_file=opts.dhcp, activate=False)
        if response == 1:
            logging.error("Error configuring dhcp server.")
            return 1
    if opts.network:
        logging.info("Configuring network interfaces...")
        response = NetConfig.configure(config_file=opts.network, activate=False)
        if response == 1:
            logging.error("Error configuring network interfaces.")
            return 1
    if opts.wpa:
        logging.info("Configuring wpa config...")
        response = WirelessConfig.configure(config_file=opts.wpa, activate=False)
        if response == 1:
            logging.error("Error configuring wpa config.")
            return 1
    if opts.core:
        logging.info("Configuring pikonek core...")
        response = CoreConfig.configure(config_file=opts.core, activate=True)
        if response == 1:
            logging.error("Error configuring core config.")
            return 1
    if opts.rule:
        try:
            logging.info("Adding captive firewall rule...")
            CaptiveConfig.configure(config_file=opts.rule)
        except Exception as e:
            logging.error(e)
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
