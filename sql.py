import sqlite3

ulist=(('John','john@lrd',233,'Developer','Submitter','abc123'),
       ('Marry','marry@lrd',556,'Content Writer','Subscriber','abc123'),
       ('Cherry','cherry@lrd',356,'SEO','Curator','abc123'),
       ('Nisha','nisha@lrd',556,'DMM','Submitter','abc123'),
       ('Neha','neha@lrd',226,'UI/UX','Submitter','abc123'),
       ('Harry','harry@lrd',116,'GraphicDesigner','Subscriber','abc123'),
       ('Om', 'om@lrd', 566, 'Database','Submitter','abc123'))


llist=(('Developer',),('Content writer',),('SEO',),('DMM',),('UIUX',),('GraphicDesigner',),('Database',))

with sqlite3.connect("mailinglist.db") as connection:
    c=connection.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,user_name TEXT,email TEXT UNIQUE,phoneno INTEGER,"
              "company_designation TEXT,list_role TEXT,password TEXT)")
    c.executemany('INSERT into users(user_name,email,phoneno,company_designation,list_role,password) values (?,?,?,?,?,?)',ulist)

    """primary key should be as small as possible ,because it makes searching faster
    as primary key is by default indexed small keys take less space
    every curator and submitter will be subscriber
    """

    c.execute('DROP TABLE IF EXISTS lists')
    c.execute("CREATE TABLE lists(list_id INTEGER PRIMARY KEY AUTOINCREMENT,list_name TEXT UNIQUE)")
    c.executemany('INSERT into lists(list_name) values (?)',llist)

    c.execute('DROP TABLE IF EXISTS subscriber_lists')
    c.execute("CREATE TABLE subscriber_lists(sl_id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER ,list_id INTEGER,"
              "FOREIGN KEY(list_id) REFERENCES lists(list_id),FOREIGN KEY (user_id) REFERENCES users(user_id),"
              "UNIQUE(user_id,list_id))")
    c.execute("insert into subscriber_lists(user_id,list_id) values (?,?)", (1,1,))
    c.execute("insert into subscriber_lists(user_id,list_id) values (?,?)", (1,2,))
    c.execute("insert into subscriber_lists(user_id,list_id) values (?,?)", (2,1,))

    c.execute('DROP TABLE IF EXISTS submitter_suggestions')
    c.execute("CREATE TABLE submitter_suggestions(ss_id INTEGER PRIMARY KEY  AUTOINCREMENT,user_id INTEGER,list_id INTEGER,url TEXT,"
              "title TEXT,description TEXT,"
              "FOREIGN KEY(user_id) REFERENCES users(user_id),FOREIGN KEY(list_id) REFERENCES lists(list_id),"
              "UNIQUE(user_id,list_id,url))")#one user can suggest one url for only one list
    c.execute('INSERT into submitter_suggestions(user_id,list_id,url,title,description) values(?,?,?,?,?)',
              (1,1,'https://us15.admin.mailchimp.com/account/api/','mailchimp','abc'))
    c.execute('INSERT into submitter_suggestions(user_id,list_id,url,title,description) values(?,?,?,?,?)',
              (4,1,'https://us15.admin.mailchimp.com/account/api/','mailchimp','abc'))
    c.execute('INSERT into submitter_suggestions(user_id,list_id,url,title,description) values(?,?,?,?,?)',
              (4, 2, 'https://us15.admin.mailchimp.com/account/api/', 'mailchimp', 'abc'))

"""mlist=(('John','john@lrd',233,'Developer','Submitter','abc123',1,0,0,0,0,0,0),
       ('Marry','marry@lrd',556,'Content Writer','abc123','Subscriber',0,1,0,0,0,0,0),
       ('Cherry','cherry@lrd',356,'SEO','Curator','abc123',0,0,1,0,0,0,0),
       ('Nisha','nisha@lrd',556,'DMM','Submitter','abc123',0,0,0,1,0,0,0),
       ('Neha','neha@lrd',226,'UI/UX','Submitter','abc123',0,0,0,0,1,0,0),
       ('Harry','harry@lrd',116,'Graphic Designer','abc123','Subscriber',0,0,0,0,0,1,0),
       ('Om', 'om@lrd', 566, 'Database','Submitter','abc123',0,0,0,0,0,0,1))


with sqlite3.connect("mailinglist.db") as connection:
    c=connection.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute("CREATE TABLE users(user_name TEXT,email TEXT,phoneno INTEGER,"
              "company_designation TEXT,list_role TEXT,password TEXT,"
              "Developer INTEGER,Content Writer INTEGER,SEO INTEGER,DMM INTEGER,UIUX INTEGER,Graphic Designer INTEGER,Database INTEGER,"
              "PRIMARY KEY(email))")
    c.executemany('insert into users values (?,?,?,?,?,?,?,?,?,?,?,?,?)',mlist)
"""

