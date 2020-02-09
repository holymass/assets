#!/usr/bin/env bash

main() {
  local svg
  cd psalms
  for f in $(ls */*.txt); do
    svg="../images/${f/txt/svg}"
    if ! [ -f $svg ]; then
      ../scripts/jianpu.py -i $f -o $svg
    fi
  done
  cd ..
}

main
