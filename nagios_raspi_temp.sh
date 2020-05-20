#!/bin/bash

temp_warn=60
temp_crit=68

error_usage () {
  echo "Usage: $0 [-w <warning_threshold>] [-c <critical_threshold>]"
  exit 3
}

# Check commandline options
while getopts 'w:c:' OPT; do
  case $OPT in
    w) temp_warn=$OPTARG ;;
    c) temp_crit=$OPTARG ;;
    *) error_usage ;;
  esac
done

# Check if thresholds are numbers
if ! [[ "$temp_warn" =~ ^[[:digit:]]+$ ]] || ! [[ "$temp_crit" =~ ^[[:digit:]]+$ ]] ; then error_usage ; fi

# Check for vcgencmd
if [ ! -x /opt/vc/bin/vcgencmd ]
then
  echo "'/opt/vc/bin/vcgencmd' not found - is this a Raspberry Pi?"
  exit 99
fi

# Read temperature information
temp=$(/opt/vc/bin/vcgencmd measure_temp | sed -e "s/temp=//" -e "s/'C//")
printf -v temp_int %.0f "$temp"

# Check for errors
if [ "$temp_int" -gt $((temp_crit*1000)) ]
then
  # Temperature above critical threshold
  return_code=2
  return_status="CRITICAL"
# Check for warnings
elif [ "$temp_int" -gt $((temp_warn*1000)) ]
then
  # Temperature above warning threshold
  return_code=3
  return_status="WARNING"
else
  # Temperature ok
  return_code=0
  return_status="OK"
fi

# Produce Nagios output
echo "TEMPERATURE ${return_status}: ${temp_int}°C | temp=${temp};${temp_warn};${temp_crit};0"
exit $return_code