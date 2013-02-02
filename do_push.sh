rm ~/.ssh/known_hosts
scp dotcloud@netsmabot.www:current/niconicomovie.db .
dotcloud push --application netsmabot
rm ~/.ssh/known_hosts
scp niconicomovie.db dotcloud@netsmabot.www:current/
rm ~/.ssh/known_hosts
scp ./netsmabot/movies/config.yaml dotcloud@netsmabot.www:current/netsmabot/movies/config.yaml
