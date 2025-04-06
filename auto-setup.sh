#!/bin/bash

git init
git branch -m main

echo ".venv/" > .gitignore

echo "pip3 install -r requirements.txt --no-cache-dir" > lib-install.sh
chmod +x lib-install.sh

echo "pandas" > requirements.txt
echo "numpy" > requirements.txt
echo "flask" > requirements.txt


python3 -m venv .venv

mkdir project_root

mv lib-install.sh project_root/
mv requirements.txt project_root/ 
