import sqlite3
import os
from database.struc import *


if os.path.isfile(filename):

    ans = input("This will delete the existing data base!\n"
                "Would you like to continue? \n")
    if ans == "yes":
        print("REMOVING OLD DB...")
        os.remove(filename)
    else:
        print("Aborting process.. bye")
        exit()


create_users_script = f"CREATE TABLE {USERS} ({ str(user_keys)[1:-1] })"
print(create_users_script, user_keys)
create_deals_script = f"CREATE TABLE {DEALS} ({ str(deal_keys)[1:-1] })"
create_commits_script = f"CREATE TABLE {COMMITS} ({ str(commit_keys)[1:-1] })"


conn = sqlite3.connect(filename)
c = conn.cursor()

c.execute(create_users_script)

c.execute(create_deals_script)

c.execute(create_commits_script)

conn.commit()
conn.close()
print("DB Created successfully.")
