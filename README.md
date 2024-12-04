# pam_lastsqlite.py
While trying to implement pam_lastlog for a vsftpd server I ran into issues with the module trying to lookup the users in the OS, but those users are not present as system users and are being authenticated with pam_pwdfile.
The good thing is that pam_lastlog is being deprecated for pam_lastlog2, but that version has not been pulled yet into Debian/Ubuntu LTS repos yet (as of december 2024).

# setup
Arch has a very good guide on how to [setup vsftpd](https://wiki.archlinux.org/title/Very_Secure_FTP_Daemon)

# pam
If you follow the guide above you should edit, and add a line `/etc/pam.d/vsftpd`:
```
session optional pam_exec.so /usr/local/bin/pam_lastsqlite.py --file /path/to/lastlog.db
auth    required pam_pwdfile.so pwdfile /etc/vsftpd/vsftp-users
account required pam_permit.so
```

# useful commands
