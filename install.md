docker compose up -d

docker build -t oh-ctionbudget-my-app-watcher .\app-watcher\

docker run -it --rm -v $(pwd)/app-watcher:/app -v $(pwd)/channel/telegram.txt:/channel/telegram.txt:ro -v $(pwd)/breachfiles:/breachfiles --env-file .env oh-ctionbudget-my-app-watcher python sessiongenerate.py

docker run -it --rm -v C:/Coding/docker/oh-ctionbudget/app-watcher:/app -v C:/Coding/docker/ohcti-threatexposure/channel/telegram.txt:/channel/telegram.txt:ro -v C:/Coding/docker/ohcti-threatexposure/breachfiles:/breachfiles --env-file .env ohcti-threatexposure-my-app-watcher python sessiongenerate.py

