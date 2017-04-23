
"""A module implementing a general sharded counter."""


import random

from google.appengine.api import memcache
from google.appengine.ext import ndb

from config import config as configuration_values


class GeneralCounterShardConfig(ndb.Model):
    """Tracks the number of shards for each named counter."""
    num_shards = ndb.IntegerProperty(default=configuration_values.default_shard_count())

    @classmethod
    def all_keys(cls, name):
        """Returns all possible keys for the counter name given the config.
        Args:
            name: The name of the counter.
        Returns:
            The full list of ndb.Key values corresponding to all the possible
                counter shards that could exist.
        """

        config = cls.get_or_insert(name)
        shard_key_strings = [createShardKey(name, index)
                             for index in range(config.num_shards)]
        return [ndb.Key(GeneralCounterShard, shard_key_string)
                for shard_key_string in shard_key_strings]


class GeneralCounterShard(ndb.Model):
    """Shards for each named counter."""
    count = ndb.IntegerProperty(default=0)


def get_count(name):
    """Retrieve the value for a given sharded counter.
    Args:
        name: The name of the counter.
    Returns:
        Integer; the cumulative count of all sharded counters for the given
            counter name.
    """
    total = memcache.get(name)
    if total is None:
        total = 0
        all_keys = GeneralCounterShardConfig.all_keys(name)
        for counter in ndb.get_multi(all_keys):
            if counter is not None:
                total += counter.count
        memcache.add(name, total, 60)
    return total

def get_count_async(name):
    total = memcache.get(name)
    if total is None:
        futures = []
        all_keys = GeneralCounterShardConfig.all_keys(name)
        futures = ndb.get_multi_async(all_keys)
        return futures
    return ndb.Future().set_result(total)

def getTotal(futureList):
    if len(futureList) == 1:
        return futureList[0].get_result()
    total = 0
    for future in futureList:
        if future.get_result():
            total += future.get_result().count
    return total

def increment(name):
    """Increment the value for a given sharded counter.
    Args:
        name: The name of the counter.
    """
    config = GeneralCounterShardConfig.get_or_insert(name)
    _increment(name, config.num_shards)


def createShardKey(name,index):
    return configuration_values.shard_key_template().format(name, index)


@ndb.transactional
def _increment(name, num_shards):
    """Transactional helper to increment the value for a given sharded counter.
    Also takes a number of shards to determine which shard will be used.
    Args:
        name: The name of the counter.
        num_shards: How many shards to use.
    """
    index = random.randint(0, num_shards - 1)
    shard_key_string = createShardKey(name, index)
    counter = GeneralCounterShard.get_by_id(shard_key_string)
    if counter is None:
        counter = GeneralCounterShard(id=shard_key_string)
    counter.count += 1
    counter.put()
    # Memcache increment does nothing if the name is not a key in memcache
    memcache.incr(name)












