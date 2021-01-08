import asyncio
import motor


async def insert_kvpair(db, kvpair):
    doc = await db.kvpairs.insert_one(dict(kvpair.__dict__))
    return doc


async def find_kvpair(db, key):
    doc = await db.kvpairs.find_one({"key": key})
    return doc if doc else None


async def drop_kvpairs(db):
    result = await db.kvpairs.drop()
    return result

