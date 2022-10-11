# pip install pipx
# pipx install poetry
# pipx ensurepath
# source ~/.bashrc

# curl -sSL https://install.python-poetry.org | python3 -
# -C- continue -S show error -o output
curl -sSL -C- -o install-poetry.py  https://install.python-poetry.org
python install-poetry.py
rm install-poetry.py
echo export PATH=~/.local/bin:$PATH > ~/.bashrc
source ~/.bashrc
# ~/.local/bin/poetry install

wget -qO- https://deb.nodesource.com/setup_14.x | bash
# bash setup_14.x
apt-get install -y nodejs
npm install -g npm@latest
npm install -g nodemon
# rm setup_14.x

# apt update  # alerady done in apt-get install -y nodejs
apt install byobu -y > /dev/null 2>&1
byobu-enable
byobu
