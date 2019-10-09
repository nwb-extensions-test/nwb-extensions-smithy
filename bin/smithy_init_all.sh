#!/usr/bin/bash

for d in */ ; do
  if [ $d != "example/" ]; then
    echo "$d"
    if nwb-extensions-smithy init --register-github "$d"; then
      git rm -r "$d"
      git commit -m "Removing registered extension record $d"
      git push origin master
  	fi
  fi
done