import asyncio

from python_bitvavo_api.bitvavo import Bitvavo

from cryptobalance.api.server import Server

from cryptobalance.handlers.update_handler import Updater
from cryptobalance.handlers.scheduler_handler import Scheduler
from cryptobalance.handlers.history_handler import History_Handler
from cryptobalance.handlers.db_handler import DB_Handler

from cryptobalance.utils.log_handling import Logging
from cryptobalance.utils.parameters import Parameters

async def main(loop):
    # Config and logging
    parameters = Parameters()
    config = parameters.get_dict()

    logging = Logging(config)
    logger = logging.get_logger()
    logging.log_dict("Configuration", items_dict=config)

    # Handlers
    logger.info("Creating handlers...")
    bitvavo = Bitvavo({
        'APIKEY': config['APIKEY'],
        'APISECRET': config['APISECRET'],
        'ACCESSWINDOW': 60000,
    })

    db_handler = DB_Handler(config=config, logger=logger)
    db_conn = db_handler.get_db_connection()
    updater = Updater(config=config, logger=logger, db_handler=db_handler, bitvavo=bitvavo)
    history_handler = History_Handler(config=config, logger=logger, db_conn=db_conn)
    scheduler = Scheduler(config=config, logger=logger, updater=updater, history_handler=history_handler)
    
    # API
    server = Server(
        config=config,
        logger=logger,
        loop=loop,
        history_handler=history_handler,
    )

    logger.info("Starting server...")
    server.start()

if __name__ == "__main__":
    try: 
        loop = asyncio.get_event_loop()

        #loop.set_debug(enabled=True)    
        if loop.get_debug():
            print("\nIf you're seeing this, the application is running in debug mode. \n")

        task = asyncio.Task(main(loop=loop))
        loop.run_forever()
    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt")
    finally:
        loop.close()