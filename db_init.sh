set -e

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