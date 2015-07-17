[![Stories in Ready](https://badge.waffle.io/dpnova/devdaemon.png?label=ready&title=Ready)](http://waffle.io/dpnova/devdaemon)

# devdaemon

[![Join the chat at https://gitter.im/dpnova/devdaemon](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/dpnova/devdaemon?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
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


# Notes

project is broken up into main components:

* issues - issue tracker code
* activity - anything time tracker related
* notes - storing quick notes
* timer - anything to do with timer stuff, like pomodoro
* todo - task lists, generally smaller and less formal than issues
* ui - anything for user interactions
