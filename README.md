# optc-python
 Unofficial Python client for One Piece Treasure Cruise


## Requirements

* Python 3
* pip

## Installation

```
git clone https://github.com/daye10/optc-python
cd optc-python
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage

### Login

This is the main entry, it creates an account, login into the account and download the latest game database locally.

Run `python login.py`, after completing this step, the script should have generated `sakura.db`.

(!) Eventually check and edit game version in `config.py` with `python game_version.py`.

### Bisque

Contains methods to encrypt and decrypt game's requests, see `bisqueDoc.py` for more details.