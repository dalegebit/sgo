#!/bin/bash
mkdir -p ~/.local/bin
cp sgo.py ~/.local/bin/sgo
chmod +x ~/.local/bin/sgo
RC_FILE=~/.${SHELL##*[/-]}rc
if [[ ! $PATH == *$HOME"/.local/bin"* ]]; then
    echo "export PATH=~/.local/bin:\$PATH" >> $RC_FILE
fi
source $RC_FILE

