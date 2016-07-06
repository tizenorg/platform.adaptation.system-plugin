#!/bin/sh

PATH=/bin:/usr/bin:/sbin:/usr/sbin

if [ "$#" -ne 1 ];then
	echo "Argument was missed."
	exit 1
fi

CHARGE_NOW_FILE=`/usr/bin/find /sys/devices -path */power_supply/battery/charge_now`
if [ "x$CHARGE_NOW_FILE" == "x" ]; then
	echo "Can not find 'charge_now'."
	CHARGE_NOW_VALUE=0
else
	CHARGE_NOW_VALUE=`/bin/cat $CHARGE_NOW_FILE`
fi

BATTERY_STATUS_FILE=`/usr/bin/find /sys/devices -path */power_supply/battery/status`
if [ "x$BATTERY_STATUS_FILE" == "x" ]; then
	echo "Can not find 'status'."
	exit 1
else
    STATUS_VALUE=`/bin/cat $BATTERY_STATUS_FILE`
fi

BATTERY_CAPACITY_FILE=`/usr/bin/find /sys/devices -path */power_supply/battery/capacity`
if [ "x$BATTERY_CAPACITY_FILE" == "x" ]; then
	echo "Can not find 'capacity'."
	exit 1
else
    CAPACITY_VALUE=`/bin/cat $BATTERY_CAPACITY_FILE`
fi

echo $STATUS_VALUE
echo $CAPACITY_VALUE

if [ "$CHARGE_NOW_VALUE" -gt 0 ];then
	echo "Do fstrim(C1)."
	/sbin/fstrim -v $*
else
    if [ \( $STATUS_VALUE == "Charging" -o $STATUS_VALUE == "Full" \) -a \( $CAPACITY_VALUE -gt 30 \) ]; then
	echo "Do fstrim(C2)."
	/sbin/fstrim -v $*
    else
	echo "Not on charging."
    fi
fi
