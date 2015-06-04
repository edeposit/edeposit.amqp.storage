#! /usr/bin/env bash

SCRIPT_DIR=`dirname $0`
cd "$SCRIPT_DIR/../src/edeposit/amqp/storage"
cd `python -c "import settings; print settings.ZCONF_PATH"`

runzeo -C zeo.conf
