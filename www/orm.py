# Author:YK  gu
import asyncio
import logging

import aiomysql


async def create_pool(loop, **kwargs):
    logging.info('create database connection pool...')

    global __pool

    __pool = await aiomysql.create_pool(
        host=kwargs.get('host', 'localhost'),
        port=kwargs.get('port', 3306),
        user=kwargs['user'],
        password=kwargs['password'],
        db=kwargs['db'],
        charset=kwargs.get('charset', 'utf-8'),
        autocommit=kwargs.get('autocommit', True),
        maxsize=kwargs.get('maxsize', 10),
        minsize=kwargs.get('minsize', 1),
        loop=loop

    )


async def select (sql,args,size=None):
    log(sql , args)
    global __pool
    async with __pool.get() as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'),args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()

        await cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs


async def execute(sql, args, autocommit=True):
    log(sql)
    global __pool
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor ) as cur:
                await cur.execute(sql.replace('?', '%s'),args or ())
                affected = cur.rowcount
                if not autocommit:
                    await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
                raise
            return affected


