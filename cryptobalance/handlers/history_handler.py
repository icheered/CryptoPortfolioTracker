"""
Handles getting/adding data to the historic database
"""

from rethinkdb import RethinkDB


class History_Handler:
    def __init__(self, config, logger, db_conn):
        self.config = config
        self.logger = logger
        self.r = RethinkDB()
        self.db_conn = db_conn
        pass

    async def get_historic_total(self, amount: int, interval: int):
        """
        Return the total portfolio value for the last <amount> datapoints
        """
        ret = list(self.r.\
            table(self.config["HISTORIC_CRYPTO_TABLE"]).\
            order_by(self.r.desc('datetime_time')).\
            limit(amount * interval).\
            pluck('epoch_time', 'datetime_time', 'total').\
            run(self.db_conn))
        
        returnlist = []
        counter = 0
        for date in ret:
            counter += 1
            if counter % interval != 0:
                continue
            datapoint = {
                'epoch_time': date['epoch_time'],
                'datetime_time': date['datetime_time'],
                'total': date['total'],
            }
            returnlist.append(datapoint)
        return returnlist

    async def get_historic_individual(self, amount: int):
        """
        Return the value for each asset for the last <amount> datapoints
        """
        ret = self.r.table(self.config["HISTORIC_CRYPTO_TABLE"]).limit(amount).order_by('epoch_time').run(self.db_conn)
        return ret

    
    async def add_datapoint(self, datapoint: dict):
        """
        Adds a datapoint to the data table containing pricing data
        """
        ret = self.r.table(self.config["HISTORIC_CRYPTO_TABLE"]).insert(datapoint).run(self.db_conn)
        self.logger.trace(ret)
        if ret["inserted"] == 1:
            self.logger.info(f"Added new datapoint for epoch: {datapoint['epoch_time']}, datetime: {datapoint['datetime_time']}")
        else:
            self.logger.warning(f"Adding datapoint went wrong: {ret}")
        return