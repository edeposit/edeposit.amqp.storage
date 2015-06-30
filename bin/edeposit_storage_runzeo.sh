#! /usr/bin/env bash

cd `python -c "import edeposit.amqp.storage.settings as s; print s.ZCONF_PATH"`
runzeo -C zeo.conf
