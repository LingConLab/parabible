ABS_PATH=`dirname readlink -f "${BASH_SOURCE:-$0}"`
CURPUS_DIR="$ABS_PATH/bible_parser/paralleltext-master/"
ARCH_FILE="paralleltext-master.exe"

set -e

if [ ! -d "$CURPUS_DIR" ] ; then
    echo "Corpus is missing. Trying to extract is from the archive"
    mkdir "$CURPUS_DIR"

    echo "./$ARCH_FILE" -d "$CURPUS_DIR" -s
    "./$ARCH_FILE" -d "$CURPUS_DIR" -p "$PWD"

    echo "Done!"
else
    echo "Corpus folder is present"
fi

echo "Launching docker..."
docker compose up --detach

echo "Starting python init parsing script..."
echo "Trying 'python'..."
if python bible_parser\\main.py ; then
    echo "Success!"
else
    echo "Failed. Trying 'python3'..."
    python3 bible_parser/main.py
fi