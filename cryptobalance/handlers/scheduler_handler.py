"""
The scheduler updates the data at regular intervals.
"""
import asyncio
import datetime
import pytz


class Scheduler:
    def __init__(self, config, logger, updater, history_handler):
        self.config = config
        self.logger = logger
        self.updater = updater
        self.history_handler = history_handler

        self.timer_task = asyncio.Task(self.timer(), name="SCH")

    async def timer(self):
        """
        Call a function at regular intervals
        """
        while True:
            try:
                await self.add_new_datapoint()
            except Exception as e:
                self.logger.error(f"Error while adding new datapoint: {e}")
            await asyncio.sleep(self.config['GET_INTERVAL'])

        self.logger.warning("Timer has stopped")
        return

    async def add_new_datapoint(self):
        """
        Retrieves and combines account data and price data
        """
        epoch_time = await self.updater.get_epoch_time()
        account_data = await self.updater.get_account_data()
        price_data = await self.updater.get_price_data()

        if(epoch_time == 0 or account_data == [] or price_data == []):
            if(not epoch_time):
                self.logger.error(f"Tried adding new datapoint but retrieved invalid time: {epoch_time}")
            if(not account_data):
                self.logger.error(f"Tried adding new datapoint but retrieved invalid account data: {account_data}")
            if(not price_data):
                self.logger.error(f"Tried adding new datapoint but retrieved invalid price data: {price_data}")
            return

        unaware_datetime_time = datetime.datetime.fromtimestamp(epoch_time / 1000) # fromtimestamp takes in seconds
        amsterdam = pytz.timezone('Europe/Amsterdam')
        datetime_time = amsterdam.localize(unaware_datetime_time)


        total = 0
        individual = []

        for asset in account_data:
            symbol = asset['symbol']
            amount = float(asset['available'])
            price = 0
            for market in price_data:
                if(market['market'] == symbol + "-EUR"):
                    price = float(market['price'])
                    break
            if not price:
                continue
            value = price * amount
            total += value

            crypto_data = {
                'symbol': symbol,
                'amount': amount,
                'price': price,
                'value': value,
            }
            individual.append(crypto_data)


        datapoint = {
            'epoch_time': epoch_time,
            'datetime_time': datetime_time,
            'total': total,
            'individual': individual
        }

        await self.history_handler.add_datapoint(datapoint)
        return