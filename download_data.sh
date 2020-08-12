clear
printf "You are about to download the dataset. Keep in mind that to download the full simulation data you need about 4Gb of free disk space.\n"
printf "\n"
#!/bin/bash
printf "Let's start with the processed trajectories dataset.\n"
printf "Are you ok with downloading about 600Mb of data? Type 'ok' if so...\n"
printf "\n"

read download
if [ "$download" == "ok" ]; then
    cd ./simulations/traj_processed
    wget [s3bucket]
    tar -xzvf traj_processed.tar.gz
    rm traj_processed.tar.gz
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
    wget [s3bucket]
else
    exit 1
fi