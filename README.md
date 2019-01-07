## About:
**pam_notifier**
is a python script, supposed to inform administrator about suspicious (client not in whitelist) ssh logins via a telegram bot and email notifications.

### Prerequisites:
````
    apt-get install libpam-python python-pip python-yaml
    pip install wheel
    pip install python-telegram-bot
````
This line should be added to */etc/pam.d/sshd* file to enable notification mechanism.
````
    session optional pam_python.so /etc/ssh/pam/pam_notify.py
````
Files supposed to be placed in */etc/ssh/pam/* directory (create a new one).
