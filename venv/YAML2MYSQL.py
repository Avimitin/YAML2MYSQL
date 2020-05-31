# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/5/31 15:59
import yaml
import mysql.connector

with open('cfg.yml', 'r', encoding='utf-8') as cfg_file:
    cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)

my_db = mysql.connector.connect(
    host=cfg['host'],
    user=cfg['user'],
    passwd=cfg['password']
)

with open('./Reply.yml', 'r', encoding='utf-8') as yaml_file:
    d = yaml.load(yaml_file, Loader=yaml.FullLoader)

cs = my_db.cursor()
cse = cs.execute

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

for key, values in d.items():
    cse('select keyword from reply_keyword')
    result = cs.fetchall()

    if not result:
        sql = 'insert into reply_keyword (keyword) values (%s)'
        cse(sql, (key,))
    else:
        if (key,) not in result:
            sql = 'insert into reply_keyword (keyword) values (%s)'
            cse(sql, (key,))

    cse('select keyword_id from reply_keyword where keyword = "%s"' % key)
    kid = cs.fetchall()[0][0]
    
    if type(values) == list:
        for value in values:
            sql = 'insert into reply_lines (keyword_id, `lines`) values (%s, %s)'
            val = (kid, value)
            cse(sql, val)
    else:
        sql = 'insert into reply_lines (keyword_id, `lines`) values (%s, %s)'
        val = (kid, values)
        cse(sql, val)


my_db.commit()
my_db.close()
