# DrayTek SNMP CollectD Plugin

This is a python plugin for CollectD, which will poll via SNMP, the connection statistics for a given DrayTek Router/Modem.

## Requirements
This plugin will require the netsnmp package to be installed prior to use.  For example:
### Centos
`yum install net-snmp-python`
### Debian/Ubuntu
`apt-get install python-netsnmp`

You will also need to ensure that you have enabled the Python module within the CollectD configuration:
```
    <LoadPlugin python>
      Globals true
    </LoadPlugin>
```

## Installation
1. Copy `draytek_collectd_python.py` to your CollectD plugins directory
2. Copy the contents of the `mibs` folder to `/usr/share/snmp/mibs/`
3. Configure the Plugin and set the required options for it to work (see below).
4. Update your `custom-types.db` to include new value types.
4. Restart CollectD

## Supplied MIBS
SNMP uses MIBS to determine the tags for each value returned when polling a client.  The included MIBS are taken directly from public sources of information (DrayTek site for ADSL-Specific Stats) and also `PerfHist-TC-MIB` which is required by the Draytek ADSL MIBS definitions.
**It is important that you have these definitions IN PLACE prior to using this plugin**

## Updating `custom-types.db`
It is recommended that you add the following to your custom types definitions:
```
adslAtucChanCrcBlockLength      value:GAUGE:U:U
adslAtucChanCurrTxRate  value:GAUGE:U:U
adslAtucChanInterleaveDelay     value:GAUGE:U:U
adslAtucChanPrevTxRate  value:GAUGE:U:U
adslAturChanCrcBlockLength      value:GAUGE:U:U
adslAturChanCurrTxRate  value:GAUGE:U:U
adslAturChanInterleaveDelay     value:GAUGE:U:U
adslAturChanPrevTxRate  value:GAUGE:U:U
adslAturCurrAtn value:GAUGE:U:U
adslAturCurrAttainableRate      value:GAUGE:U:U
adslAturCurrOutputPwr   value:GAUGE:U:U
adslAturCurrSnrMgn      value:GAUGE:U:U
adslLineCoding  value:GAUGE:U:U
adslLineType    value:GAUGE:U:U
```

## Configuration
By default, this plugin will connect to `127.0.0.1` and use the SNMP community `public`.  To enable this plugin, add the following to your CollectD configuration:
```
  Import "draytek-collectd"
```
You can then configure (if required) a different IP for the Modem, or different SNMP Community value:
```
  <Module "draytek-collectd">
    modem_ip "192.168.1.254"
    community "public"
  </Module>
```

## Metrics
The plugin will perform an SNMP Walk against the OID `SNMPv2-SMI::transmission.94.1.1`, which contains the majority of all connection-based statistics which are defined as either an Integer or Gauge value:
```
adslLineCoding
adslLineType
adslAturCurrSnrMgn
adslAturCurrAtn
adslAturCurrOutputPwr
adslAturCurrAttainableRate
adslAtucChanInterleaveDelay
adslAtucChanCurrTxRate
adslAtucChanPrevTxRate
adslAtucChanCrcBlockLength
adslAturChanInterleaveDelay
adslAturChanCurrTxRate
adslAturChanPrevTxRate
adslAturChanCrcBlockLength
```
