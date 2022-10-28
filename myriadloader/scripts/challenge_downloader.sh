mkdir -p ~/code/lewagon/$CHA_PATH && cd $_
if [ "$(ls -A .)" ] ; then
  echo "$(pwd)" folder is not empty. Overwrite existing challenge ? [Y/n]
  read input
  if [[ $input == "Y" || $input == "y" ]]; then
    curl -s -H "Authorization: Token $KITT_TOKEN" "https://kitt.lewagon.com/camps/$DEFAULT_BATCH/challenges/setup_script?gh=$GH_USERNAME&path=${CHA_PATH//\//%2F}" | tail -n +11 | bash
    echo "✅ $CHA_PATH downloaded"
  else
    echo "❌ Challenge not downloaded"
    exit 0
  fi
else
  curl -s -H "Authorization: Token $KITT_TOKEN" "https://kitt.lewagon.com/camps/$DEFAULT_BATCH/challenges/setup_script?gh=$GH_USERNAME&path=${CHA_PATH//\//%2F}" | tail -n +11 | bash
  echo "✅ $CHA_PATH downloaded"
fi
