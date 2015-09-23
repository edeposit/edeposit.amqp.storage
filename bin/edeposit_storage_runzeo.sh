#! /usr/bin/env bash

cd `python -c "import edeposit.amqp.storage.settings as s; print s.ZCONF_PATH"`

# supervisord can't will stop the script, but let the runzeo running, this
# should fix it
trap "{ pkill runzeo -SIGINT; exit 0; }" EXIT

runzeo -C zeo.conf
