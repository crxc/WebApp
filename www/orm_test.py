# Created by: coderShan
# Created on: 2018/10/15
import asyncio
import unittest
import logging

import orm
from bean import User


async def test(loop):
    await orm.create_pool(loop, user='root', password='', db='awesome')
    u = User(name='Test', email='jdxbwsbf@gmail.com', passwd='123', image='about:blank')
    await u.save()


class TestOrm(unittest.TestCase):
    def testSave(self):
        logging.info("start")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test(loop))
        print('Test finished.')
        loop.close()
