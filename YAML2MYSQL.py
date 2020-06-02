# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/5/31 15:59
import yaml
import mysql.connector

# Load config
with open('cfg.yml', 'r', encoding='utf-8') as cfg_file:
    cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)

my_db = mysql.connector.connect(
    host=cfg['host'],
    user=cfg['user'],
    passwd=cfg['password']
)

# load sample file
with open('./sample.yml', 'r', encoding='utf-8') as yaml_file:
    d = yaml.load(yaml_file, Loader=yaml.FullLoader)

# add cursor
cs = my_db.cursor()
cse = cs.execute

# create database 'bot_reply_msg'
# create two tables 'reply_keyword' and 'reply_lines'
cse('create database if not exists bot_reply_msg')
cse('use bot_reply_msg')
cse('create table if not exists reply_keyword ('
    'keyword_id bigint auto_increment primary key not null,'
    'keyword varchar(255) not null'
    ')')
cse('create table if not exists reply_lines('
    'lines_id bigint auto_increment primary key,'
    'keyword_id bigint not null,'
    '`lines` varchar(255),'
    'foreign key (keyword_id) references reply_keyword(keyword_id)'
    ')')

# iterate all items in the yaml file
for key, values in d.items():
    cse('select keyword from reply_keyword')
    result = cs.fetchall()

    # add condition to help not add duplicate items
    if not result:
        sql = 'insert into reply_keyword (keyword) values (%s)'
        cse(sql, (key,))
    else:
        if (key,) not in result:
            sql = 'insert into reply_keyword (keyword) values (%s)'
            cse(sql, (key,))

    # use keyword_id as foreign key so have to get it
    cse('select keyword_id from reply_keyword where keyword = "%s"' % key)
    kid = cs.fetchall()[0][0]

    # some values is list so need to iterate all item in list
    if type(values) == list:
        for value in values:
            sql = 'insert into reply_lines (keyword_id, `lines`) values (%s, %s)'
            val = (kid, value)
            cse(sql, val)
    else:
        sql = 'insert into reply_lines (keyword_id, `lines`) values (%s, %s)'
        val = (kid, values)
        cse(sql, val)

# final
my_db.commit()
my_db.close()
