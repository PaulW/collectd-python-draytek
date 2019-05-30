#!/usr/bin/env python

import os
import netsnmp
import signal
import collectd
from math import floor

PLUGIN_NAME = 'draytek'
DRAYTEK_MODEM_IP = "127.0.0.1"
SNMP_COMMUNITY = "public"
os.environ['MIBS'] = 'ADSL-LINE-MIB'

collectd.info('plugin_load: plugin "%s" successfully loaded.' % PLUGIN_NAME)

def config_func(config):
  for node in config.children:
    key = node.key.lower()
    val = node.values[0]

    if key == 'modem_ip':
      global DRAYTEK_MODEM_IP
      DRAYTEK_MODEM_IP = val
      collectd.info('%s: Using overridden Modem IP "%s"' % (PLUGIN_NAME, DRAYTEK_MODEM_IP))
    elif key == 'community':
      global SNMP_COMMUNITY
      SNMP_COMMUNITY = val
      collectd.info('%s: Using overridden SNMP Community "%s"' % (PLUGIN_NAME, SNMP_COMMUNITY))
    else:
      collectd.info('%s: Unknown config key "%s"' % (PLUGIN_NAME, key))

def float_round(num, places = 0, direction = floor):
  return direction(num * (10**places)) / float(10**places)

def read_func():
  SNMP_OID = netsnmp.VarList('SNMPv2-SMI::transmission.94.1.1')
  SNMP_RES = netsnmp.snmpwalk(SNMP_OID, Version=2, DestHost=DRAYTEK_MODEM_IP, Community=SNMP_COMMUNITY)
  for x in SNMP_OID:
    if x.type == "INTEGER" or x.type == "GAUGE":
      stat = collectd.Values(type=x.tag)
      stat.plugin = PLUGIN_NAME
      stat.values = [float_round(int(x.val), 3, round)]
      #stat.values = [x.val]
      collectd.info('%s: \'%s\': %r' % (PLUGIN_NAME, x.tag, stat.values))
      stat.dispatch()

def init():
  signal.signal(signal.SIGCHLD, signal.SIG_DFL)

collectd.register_init(init)
collectd.register_config(config_func)
collectd.register_read(read_func)
