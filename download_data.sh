#!/bin/bash
clear
printf "You are about to download the dataset. Keep in mind that to download the full simulation data you need about 4Gb of free disk space.\n"
printf "\n"
printf "Let's start with the processed trajectories dataset.\n"
printf "Are you ok with downloading about 600Mb of data? Type 'ok' if so...\n"
printf "\n"

read download
if [ "$download" == "ok" ]; then
    cd ./data
    # TODO swp this to ZENODO links
    wget https://lipids-comparison.s3.eu-west-2.amazonaws.com/traj_processed.tar.gz
    tar -xzvf traj_processed.tar.gz && rm traj_processed.tar.gz
    cd -
else
    exit 1
fi

printf "\n"
printf "Do you also want to download the full trajectories?\n" 
printf "Bear in mind this file is about 3Gb. Type 'yeah' if so...\n"
printf "\n"

read download
if [ "$download" == "yeah" ]; then
    cd ./data
    # TODO swp this to ZENODO links
    wget [s3bucket]
    tar -xzvf traj_raw.tar.gz && rm traj_raw.tar.gz
    cd -
else
    exit 1
fi