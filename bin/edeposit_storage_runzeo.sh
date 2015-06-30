#! /usr/bin/env bash

SCRIPT_PATH=$(dirname `which $0`)
cd "$SCRIPT_PATH/../src/edeposit/amqp/storage"
cd `python -c "import settings; print settings.ZCONF_PATH"`

runzeo -C zeo.conf
