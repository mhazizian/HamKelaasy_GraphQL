#!/bin/bash

RUNAT="02"

while [ 1 ]
do
    DATE=`/bin/date +%H`
    if [ $DATE. = $RUNAT. ]
    then
        time=$(date +%Y_%m_%d_%A_%H_%M_%S)
		backup_file="./backup/db/"$time".json"
		backup_file_enc=$backup_file".enc"

		./manage.py dumpdata > $backup_file

		openssl aes-256-cbc -a -salt -in $backup_file -out $backup_file_enc -pass pass:borhan123
		./gdrive upload -p 0B9kxC0hDGmDLeTdCSXh2UWFBU2c $backup_file_enc
    fi

    sleep 3590
done


#openssl aes-256-cbc -d -a -in $backup_file_enc -out secrets.txt.new -pass pass:borhan123
