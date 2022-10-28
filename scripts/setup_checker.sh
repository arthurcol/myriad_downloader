for program in curl tar git gh ; do
  if ! type "$program" &>/dev/null ; then
    echo "$program" is not installed. Please review your setup: https://github.com/lewagon/setup#in-english
    exit 1
fi
done
for var in GH_USERNAME KITT_TOKEN DEFAULT_BATCH; do
  if [ -z "${!var}" ] ; then
   echo "$var" is not set. Please run myriadloader --auth
   exit 1
  fi
done
