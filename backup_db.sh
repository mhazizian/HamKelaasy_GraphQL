#!/bin/bash

time=$(date +%Y_%m_%d_%A_%H_%M_%S)
backup_file="./db_backup/"$time".json"
./manage.py dumpdata > $backup_file