# pam_lastsqlite.py

While trying to implement `pam_lastlog` for a vsftpd server I ran into issues... `pam_lastlog` is trying to lookup the virtual users that are authenticated with pam_pwdfile as being system users.
The good thing is that `pam_lastlog` is being deprecated for `pam_lastlog2`... the bad thing is that Debian/Ubuntu LTS do not include those changes.
You can import users as epoch 0, so you can easily list old accounts.

This a stop gap solution, it does not support date > 2038.

## pam

If you follow the guide above you should edit, and add a line `/etc/pam.d/vsftpd`:

```pam
session optional pam_exec.so /usr/local/bin/pam_lastsqlite.py --file /path/to/lastlog.db
auth    required pam_pwdfile.so pwdfile /etc/vsftpd/vsftp-users
account required pam_permit.so
```

(be sure to edit the files locations)

## setup

Arch has a very good guide on how to [setup vsftpd](https://wiki.archlinux.org/title/Very_Secure_FTP_Daemon)

Please adapt the path according to your setup:

```bash
# Initialize the db
/usr/local/bin/pam_lastsqlite.py --file /path/to/lastlog.db --create

# Load existing user from the password file
/usr/local/bin/pam_lastsqlite.py --file /path/to/lastlog.db --load /etc/vsftpd/vsftp-users
```

## useful commands

List all:

```bash
sqlite3 /path/to/lastlog.db 'select * from lastlog'
```

List old users:

```bash
export date=$(date -d "1 year ago" +%s)
sqlite3 /path/to/lastlog.db "select user from lastlog where date < $date"
```
