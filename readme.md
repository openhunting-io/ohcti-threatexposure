![OpenAI Logo](https://www.openai.com/images/openai-logo.png)
# OHCTI! Threat Exposure | Data Breach Monitoring (Telegram)
As someone tasked with threat analysis, it is important for a threat hunter to understand how threat exposure occurs due to external factors such as user account breaches. There are many ways to analyze compromised accounts caused by malware stealers that infiltrate user devices. However, the average service provider offering user account exposure analysis tends to have a relatively high cost, making it challenging for threat analysts to provide their analysis.

OHCTI! Threat Exposure is a tool built to facilitate this function, where threat analysts and intelligence professionals can examine exposure of user accounts within the organization under analysis, or perhaps for those conducting related research. OHCTI! Threat Exposure will detect user account breaches distributed through Telegram accounts. Every new file containing user information that emerges will be automatically integrated into the OHCTI! Threat Exposure system. You can easily search for account exposure using Telegram by contacting your BOT, and the BOT will automatically provide the results of your search command.

## Pre-Installation
- Git
- Docker
- Telegram BOT token (Create Bot using [Bot Father](https://t.me/BotFather))
- Telegram Account (API_ID, API_HASH, USER_PHONE) [Telegram Account](https://my.telegram.org/auth)



## Download Script

Use This Command To Download Script

```bash
git clone https://github.com/openhunting-io/ohcti-threatexposure
cd ohcti-threatexposure
mv .env.example .env
```

## Edit .env File
Insert your Telegram BOT Token And Telegram Account

```
BOT_TOKEN=

## EXAMPLE
# BOT_TOKEN=6342412021:AAFr_cIgZFZYKzkdIn6NJ3UQzJ-WxrK2ayd

TELEGRAM_API_ID=
TELEGRAM_API_HASH=
TELEGRAM_PHONE_NUMBER=

## EXAMPLE
# TELEGRAM_API_ID=2172637
# TELEGRAM_API_HASH=1813a353948a0baaff99a5b59c6e5380
# TELEGRAM_PHONE_NUMBER=+628123456789

```

## Running Tools

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

```
docker build -t ohcti-threatexposure-my-app-watcher .\app-watcher\
```
Then, Create Telegram Session
```
docker run -it --rm -v $(pwd)/app-watcher:/app -v $(pwd)/channel/telegram.txt:/channel/telegram.txt:ro -v $(pwd)/breachfiles:/breachfiles --env-file .env ohcti-threatexposure-my-app-watcher python sessiongenerate.py
```

here is example, if you run in Windows

```
docker run -it --rm -v C:/Coding/docker/oh-ctionbudget/app-watcher:/app -v C:/Coding/docker/ohcti-threatexposure/channel/telegram.txt:/channel/telegram.txt:ro -v C:/Coding/docker/ohcti-threatexposure/breachfiles:/breachfiles --env-file .env ohcti-threatexposure-my-app-watcher python sessiongenerate.py
```

You Have to Insert Phone Number, then get token from Telegram.

Then, Running Docker Compose
```
docker compose up -d
```

## How to Use

chat your telegram bot, for example

```
/search example.co.id
```


## Openhunting.io

Let's Opensource Threat Hunting Intelligence Information & Tools
Openhunting.io is Project To Make Threat Hunting Information & Tools Available for Every One

![OpenAI Logo](https://www.openai.com/images/openai-logo.png)


## License

[MIT](https://choosealicense.com/licenses/mit/)