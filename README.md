To reproduce results:

1. Clone the repo and cd into it
2. Create python virtual enviroment by running `python -m venv env` and activate it by running `source env/Scripts/activate` if Windows or `source env/bin/activate` if Mac
3. Install the python requirements by running `pip install -r requirements.txt`
4. Create a file called `.env` and write `ACCESS_TOKEN={token}` on it where `token` is the access token for the app (ask Raul to if you don't have it)
5. Execute `python test.py`
