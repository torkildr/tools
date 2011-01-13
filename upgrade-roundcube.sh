#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: source destination"
    exit 0
fi

base=$(basename ${1})
dest=$(basename ${2})

echo "Upgrading installation in ${dest} with files from ${base}"

for dir in "bin" "SQL" "program" "installer" "skins/default" "plugins"; do
    echo "${base}/${dir} -> ${dest}/${dir}/"
    cp -R ${base}/${dir}/* ${dest}/${dir}/
done

echo "${base}/ -> ${dest}/"
find ${base} -maxdepth 1 -type f -exec cp {} ${dest}/ \;

cd ${dest}

echo
echo "Running update script"

${dest}/bin/update.sh

cd - > /dev/null

