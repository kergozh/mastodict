# Mastodict

This code manages uno or more dictionaries. It publish one random word everyday and listen mentions in order to perform several actions. It's possible to see the actions in the action.yaml file. 

### Dependencies

-   **Python 3**
-   Mastodon account

### Usage:

Within Python Virtual Environment:

1. Optionally, create a new user for running the bot: `adduser --disabled-login user_name`

2. Clone the repository `git clone https://github.com/lgbaixauli/mastodict.git` 

3. Crate a virtual environment `python3 -m venv .venv` and activate it `source .venv/bin/activate`

4. Run `pip install -r requirements.txt` to install needed libraries.  

5. Modify options in the `config.yaml` file. For exemple, the keyword the access type or directory and file names.

6. It's possible to fill in the config yaml the cliend id, cliend secret and access token of an application created in the Mastodon web (with de "development" opction). Also, it's possilbe to indicate credentials access and run `python3 dict.py` manually once to setup and get its access token to Mastodon instance.

7. Use your favourite scheduling method to set `dict.sh` to run every minute. For example,  add  `* * * * * /home/user_name/mastodict/dict.sh 2>&1 | /usr/bin/logger -t MASTODICT` in `crontab -e`. The system and error log will be in `/var/log/syslog`. 

   Don't forgot the execution privilegies `chmod +x dict.sh`. 
   Don't forgot update the user_name in `dict.sh`
