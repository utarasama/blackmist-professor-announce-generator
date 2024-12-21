pip install -r requirements.txt
apt-get update && apt-get install -y locales \
    && locale-gen fr_FR.UTF-8 \
    && update-locale LANG=fr_FR.UTF-8
