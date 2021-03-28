# GdriveSearcherBot
#### Google Drive Searcher Bot Written In Python Using Pyrogram. 


[![Python](http://forthebadge.com/images/badges/made-with-python.svg)](https://python.org)

<img src="https://i.imgur.com/MxrswfJ.png" width="370" align="right">


### Installation

##### Getting Google OAuth API credential file
- Visit the [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Go to the OAuth Consent tab, fill it, and save.
- Go to the Credentials tab and click Create Credentials -> OAuth Client ID
- Choose Desktop and Create.
- Use the download button to download your credentials.
- Move that file to the root of this bot, and rename it to credentials.json
- Visit [Google API page](https://console.developers.google.com/apis/library)
- Search for Drive and enable it if it is disabled
- Run these commands

```sh
$ pip3 install -U pip
$ pip3 install -U -r requirements.txt
$ python3 generate_drive_token.py
$ cp sample_config.py config.py
```
- Edit **config.py** with your own values
- Run  ```$ python3 main.py```  to start the bot.

### Docker Installation
```sh
$ git clone https://github.com/thehamkercat/GdriveSearcherBot
$ cd GdriveSearcherBot
$ sudo docker build . -t GdriveSearcherBot
$ sudo docker run GdriveSearcherBot
```
### Credits
[@SVR666](https://github.com/SVR666) For Drive module.

### Notes
- Join [PatheticProgrammers](https://t.me/patheticprogrammers) For Help.
