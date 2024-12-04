#!/usr/bin/python3

import sqlite3
import argparse
import time
import os
import socket

parser = argparse.ArgumentParser()
parser.add_argument('--create', action='store_true',
                    help='Create database file and initialize')
parser.add_argument('--file', dest='file', type=str,
                    help='Location of the database file')
parser.add_argument('--load', dest='load', type=str,
                    help='Load accounts from file')
args = parser.parse_args()


def create_db(db):
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE lastlog(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user TEXT, date INTEGER)")
        cursor.close()
        con.close()
        print("Database initialized")
    except sqlite3.Error as e:
        print(f"create_db: {e}")


def update_db(db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        current_time = int(time.time())
        user = os.environ.get('PAM_USER')

        cursor.execute(
            "SELECT * FROM lastlog WHERE user=?", (user,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.execute(
                "UPDATE lastlog SET date=? WHERE user=?", (current_time,user,))
        else:
            cursor.execute(
                "INSERT INTO lastlog (user, date) VALUES (?, ?)", (user,current_time,))
        conn.commit()
        # print(f"User '{params[0]}' {'updated' if existing_user else 'inserted'} successfully.")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"update_db: {e}")


def load_db(db, users_file):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        import csv
        with open(users_file) as csvfile:
            list = csv.reader(csvfile, delimiter=':')
            for row in list:
                print(row[0])
                # data = (
                #     row[0],
                #     '0',
                # )
                # cursor.execute( "INSERT INTO lastlog (user, date) VALUES (?, ?)", data )
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"load_db: {e}")


# MAIN
if args.create:
    create_db(args.file)
    exit(0)
elif args.load:
    load_db(args.file, args.load)
    exit(0)
else:
    update_db(args.file)
    exit(0)
