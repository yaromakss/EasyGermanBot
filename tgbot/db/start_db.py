import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
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
    cur.execute('''CREATE TABLE IF NOT EXISTS "users"(
                id               varchar not null
                constraint users_pk
                    primary key,
                name             text    not null,
                username         text,
                correct_answers  integer default 0,
                last_achievement integer default 0);
                
                create table if not exists "nouns"
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
                
                create table if not exists "verbs"
                (
                    id           serial
                        constraint verbs_pk
                            primary key,
                    verb_inf     text not null,
                    verb_past    text not null,
                    verb_perfect text not null
                );
                
                create table if not exists "adjectives"
                (
                    id  serial
                        constraint adjectives_pk
                            primary key,
                    adj text not null
                );
                
                create table if not exists "achievements"
                (
                    id                         serial
                        constraint achievements_pk
                            primary key,
                    achievement_name           text    not null,
                    achievement_answers_amount integer not null
                );
                
                
                
                
                
                
                
                
                ''')

    base.commit()
    cur.close()
    base.close()
