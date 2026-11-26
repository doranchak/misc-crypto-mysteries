#!/bin/zsh
G="/Users/doranchak/Library/CloudStorage/GoogleDrive-doranchak@gmail.com/My Drive/Zodiac/Solutions/Gareth Penn/attachments"
S=/private/tmp/claude-501/-Users-doranchak-projects-github-misc-crypto-mysteries/6559da2e-315e-4764-b182-03e1130553e5/scratchpad
O=/Users/doranchak/projects/github/misc-crypto-mysteries/gareth-penn-crypto-curiosities/ocr
mkdir -p $S/raw2
for i in 1 2 3 4 5; do
  mkdir -p $S/raw2/t17p$i
  pdfimages -j "$G/Gareth Penn - Times 17 - Part $i of 5/times-17-part-$i.pdf" $S/raw2/t17p$i/p &
done
mkdir -p $S/raw2/sp
pdfimages -j "$G/Gareth Penn The Second Power/gareth_penn_second_power.pdf" $S/raw2/sp/p &
wait
ls $S/raw2/*/p-*.jpg | xargs -P 16 -I{} sh -c '/opt/homebrew/bin/python3.11 -I /Users/doranchak/projects/github/misc-crypto-mysteries/gareth-penn-crypto-curiosities/work/py/ocr_prep.py "$1" "${1%.jpg}.png" && tesseract "${1%.jpg}.png" "${1%.jpg}" --psm 6 >/dev/null 2>&1' _ {}
for d in $S/raw2/*; do n=$(basename $d); for f in $(ls $d/p-*.txt | sort -V); do echo "=== PDFPAGE $(( $(basename $f .txt | sed 's/p-0*//;s/^$/0/') + 1 ))"; cat $f; done > $O/$n.v2.txt; done
echo done
