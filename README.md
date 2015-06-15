[![Stories in Ready](https://badge.waffle.io/dpnova/devdaemon.png?label=ready&title=Ready)](http://waffle.io/dpnova/devdaemon)

# devdaemon
Cross a pomodoro timer with your favourite task + todo + issue management software and make it all hacker friendly.
# A dev daemon to help with things

## Implementation ideas

https://github.com/twisted/twisted/blob/trunk/twisted/conch/manhole.py#L160

* powerline segment for tmux
* pomodoro timer that posts comments to pivotal tracker - done
* start PT tickets - done
* idle time tracker for pomodoros
* ideally we'd let it change the task in hubstaff too
* stream flowdock and queue highlights until after pomodoro
* telnet command line
* alert when idle
* log activity, interruptions for each pomo
* support multiple "projects" with environment variables in the client
* create new issue if no issue id passed
