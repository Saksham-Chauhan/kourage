#!/usr/bin/bash

################################################################################
# Run this shell in detach mode. It'll start the docker in case of the stdin
# (dce_stdin) file is found.
#
# NOTE: Currently it requires sudo permissions due to docker.
################################################################################

FLOC=stream/dce_stdin

docker pull tyrrrz/discordchatexporter
function file_get(){
	local out=$(cat "$FLOC" | grep "$1" | sed "s/$1: //g")
	echo "$out"
}
while true
do
	if [ -f "$FLOC" ]
	then
		token=$(file_get "token")

		p=$(cat "$FLOC" | grep "guild")
		if [[ -z "$p" ]]
		then
			channel=$(file_get "channel")
			docker run -t -v $(pwd)/stream/files:/app/out tyrrrz/discordchatexporter export --channel "$channel" --token "$token"
		else
			guild=$(file_get "guild")
			docker run -t -v $(pwd)/stream/files:/app/out tyrrrz/discordchatexporter exportguild --guild "$guild" --token "$token"
		fi

		echo "Done" > stream/o_stdin
		rm "$FLOC"
		while true
		do
			if [ -f "$FLOC" ]
			then
				rm stream/files/*
				sudo rm "$FLOC"
				break
			fi
			sleep 1
		done
	fi
	sleep 1
done
