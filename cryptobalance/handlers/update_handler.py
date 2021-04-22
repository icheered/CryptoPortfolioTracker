"""
Handles the updating of the database
"""

import asyncio

class Updater:
    def __init__(self, config, logger, db_handler, bitvavo):
        self.config = config
        self.logger = logger
        self.db_handler = db_handler
        self.bitvavo = bitvavo
    
    async def get_epoch_time(self):
        """
        Get the number of milliseconds since 1/1/1970 (Epoch time) from BitVavo
        """
        if(not await self.get_remaining_limit()):
            self.logger.warning("Rate limit exceeded")
            return 0
        
        ret = self.bitvavo.time()
        if 'time' in ret:
            return ret['time']
        else:
            self.logger.warning("Tried retrieving time but did not receive dict with 'time'")
            return 0

    async def get_remaining_limit(self):
        """
        Retrieve the amount of api calls that I can make. If an API call is made while there is no limit left then bad things happen
        
        Returns:
            int: Remaning API call limit
        """
        ret = self.bitvavo.getRemainingLimit()
        if type(ret) == int:
            return ret
        else:
            self.logger.warning("Retrieved rate limit but did not receive integer")
            return 0

    async def get_account_data(self):
        """
        Retrieve the account data from BitVavo
        """
        if(not await self.get_remaining_limit()):
            self.logger.warning("Rate limit exceeded")
            return
        
        ret = self.bitvavo.balance({})
        if(type(ret) == list):
            return ret
        else:
            self.logger.warning("Tried getting ticker price but did not receive list")
            return []

    async def get_price_data(self):
        """
        Retrieve the prices for all markets on BitVavo
        """
        if(not await self.get_remaining_limit()):
            self.logger.warning("Rate limit exceeded")
            return

        ret = self.bitvavo.tickerPrice({})
        if(type(ret) == list):
            return ret
        else:
            self.logger.warning("Tried getting ticker price but did not receive list")
            return []