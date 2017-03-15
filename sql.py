import sqlite3
import  sys
mlist=(('John','john@lrd',233,'Developer','Submitter','Developer','abc123'),
       ('John','john@lrd',233,'Developer','Submitter','SEO','abc123'),
       ('Marry','marry@lrd',556,'Content Writer','Subscriber','Content Writer','abc123'),
       ('Cherry','cherry@lrd',356,'SEO','Curator','SEO','abc123'),
       ('Nisha','nisha@lrd',556,'DMM','Submitter','DMM','abc123'),
       ('Neha','neha@lrd',226,'UI/UX','Submitter','UI/UX','abc123'),
       ('Harry','harry@lrd',116,'Graphic Designers','Subscriber','Graphic Designer','abc123'),
       ('Om', 'om@lrd', 566, 'Database','Submitter','Database','abc123'))
#con=sqlite3.connect('sales.db')
#mlist=(('johnid',233),('marryid',556))

with sqlite3.connect("mailinglist.db") as connection:
    c=connection.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute("CREATE TABLE users(user_name TEXT,email TEXT,phoneno INTEGER,company_designation TEXT,list_role TEXT,subscribed_list TEXT,password TEXT,PRIMARY KEY(email,subscribed_list))")
   # c.execute("CREATE TABLE users(user_id TEXT,user_name INTEGER)")

    c.executemany('insert into users values (?,?,?,?,?,?,?)',mlist)