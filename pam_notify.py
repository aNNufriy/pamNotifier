#!/usr/bin/env python
import os
import sys 
import smtplib
import time
import syslog
import telegram
import yaml

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Author:: Alexander Schedrov (schedrow@gmail.com)
# Copyright:: Copyright (c) 2019 Alexander Schedrov
# License:: MIT
def pam_sm_open_session(pamh, flags, args):
    cwd = '/etc/ssh/pam/'

    whitelist=[line.rstrip('\n') for line in open(cwd+'whitelist','r')]
    if not any(pamh.rhost==s for s in whitelist):
        if pamh.get_user()!="git":
            message = '%s: [%s] logged in from [%s]' % (os.uname()[1],pamh.get_user(),pamh.rhost)
            syslog.syslog(message)

            with open(cwd+'parameters.yml', 'r') as stream:
                try:
                    params = yaml.safe_load(stream)
                    
                    send_tg_message(params['tg'], message)
                    send_em_message(params['em'], message)

                    return pamh.PAM_SUCCESS
                except Exception, e:
                    syslog.syslog(syslog.LOG_ERR, str(e))
                    return pamh.PAM_SERVICE_ERR

def pam_sm_close_session(pamh, flags, args):
    return pamh.PAM_SUCCESS

def send_tg_message(tgparams, message):
    bot = telegram.Bot(token=tgparams['bot_token'])
    bot.sendMessage(chat_id=tgparams['chat_id'], text=message)

def send_em_message(emparams, message, host=os.uname()[1]):
    timestring = time.strftime("[%Y-%m-%d %H:%M:%S]") 

    mpartmsg = MIMEMultipart()
    mpartmsg['From'] = emparams['adr_from']
    mpartmsg['To'] = emparams['adr_to']
    mpartmsg['Subject'] = host+' ssh login'
    mpartmsg.attach(MIMEText(message))

    emclient = smtplib.SMTP_SSL(emparams['smtp_server'],465)
    emclient.ehlo()
    emclient.login(emparams['adr_from'], emparams['password'])
    emclient.sendmail(emparams['adr_from'], emparams['adr_to'], mpartmsg.as_string())
    emclient.quit()
