import psycopg2
from tgbot.config import load_config

import logging

config = load_config(".env")


async def postgre_start():
    base = psycopg2.connect(dbname=config.db.database,
                            user=config.db.user,
                            password=config.db.password,
                            host=config.db.host, )
    cur = base.cursor()
    if base:
        logging.info(f"data base connect success!")
    cur.execute('''create table if not exists public.users
                (
                    id                        integer not null
                        constraint users_pk
                            primary key,
                    name                      text    not null,
                    username                  text,
                    lang                      varchar(2),
                    correct_answ_plural       integer default 0,
                    last_achievement_plural   integer default 0,
                    correct_answ_articles     integer default 0,
                    last_achievement_articles integer default 0,
                    correct_answ_perfect      integer default 0,
                    last_achievement_perfect  integer default 0
                );
                
                create table if not exists public.nouns
                (
                    id              serial
                        constraint nouns_pk
                            primary key,
                    article         text not null,
                    noun_single_ger text not null,
                    noun_plural_ger text not null,
                    noun_single_eng text not null,
                    noun_plural_eng text not null,
                    noun_single_ukr text not null,
                    noun_plural_ukr text not null,
                    noun_single_rus text not null,
                    noun_plural_rus text not null
                );
                                
                create table if not exists public.verbs
                (
                    id               serial
                        constraint verbs_pk
                            primary key,
                    verb_ger_inf     text not null,
                    verb_ger_past    text not null,
                    verb_ger_perfect text not null,
                    verb_eng         text not null,
                    verb_ukr         text not null,
                    verb_rus         text not null
                );
                                
                create table if not exists public.adjectives
                (
                    id      serial
                        constraint adjectives_pk
                            primary key,
                    adj_ger text not null,
                    adj_eng text not null,
                    adj_ukr text not null,
                    adj_rus text not null
                );''')

    base.commit()
    cur.close()
    base.close()
