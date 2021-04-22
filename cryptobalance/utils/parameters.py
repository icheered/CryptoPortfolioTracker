import configargparse


class Parameters:
    def __init__(self):
        self.parser = configargparse.ArgParser(default_config_files=["config.ini"])

        self.init_general_parameters()
        self.init_database_parameters()
        self.init_bitvavo_parameters()
        self.init_scheduler_parameters()

        parameters, unknown = self.parser.parse_known_args()
        self.dictionary = self.create_dict(parameters)

    @staticmethod
    def create_dict(parameters):
        ret = {}
        for option in vars(parameters):
            ret[option] = getattr(parameters, option)
        return ret

    def get_dict(self):
        return self.dictionary

    @staticmethod
    def str2bool(string: str) -> bool:
        """
        Converts a string to a boolean.
        :param string: string to convert to boolean
        :return: True or False
        """
        if string.lower() in ["false", "n", "no", "f"]:
            return False
        elif string.lower() in ["true", "y", "yes", "t"]:
            return True
        else:
            raise TypeError(f"{string} cannot be converted to boolean")

    def init_general_parameters(self):
        general_group = self.parser.add_argument_group("General")

        general_group.add_argument(
            "--LOG_LEVEL",
            type=str,
            help="Set level of logging to DEBUG, INFO, WARNING, ERROR",
            default="INFO",
        )
        general_group.add_argument(
            "--API_ADDRESS",
            type=str,
            help="Address where the API will be accesible",
            default="0.0.0.0",  # nosec
        )
        general_group.add_argument(
            "--API_PORT",
            type=int,
            help="Port on which the API is served",
            default=4500,  # nosec
        )

    def init_database_parameters(self):
        db_group = self.parser.add_argument_group("Database")

        db_group.add_argument(
            "--DB_ADDRESS",
            type=str,
            help="Address of the RethinkDB",
            default="", 
        )
        db_group.add_argument(
            "--DB_PORT",
            type=str,
            help="Port of the RethinkDB",
            default="", 
        )
        db_group.add_argument(
            "--DB_NAME",
            type=str,
            help="Name of the database",
            default="",
        )
        db_group.add_argument(
            "--HISTORIC_CRYPTO_TABLE",
            type=str,
            help="Name of the crypto table with historic data",
            default="",
        )

    def init_bitvavo_parameters(self):
        bv_group = self.parser.add_argument_group("BitVavo")

        bv_group.add_argument(
            "--APIKEY",
            type=str,
            help="APIKEY from BitVavo",
            default="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 
        )
        bv_group.add_argument(
            "--APISECRET",
            type=str,
            help="APISECRET from BitVavo",
            default="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 
        )
    
    def init_scheduler_parameters(self):
        scheduler_group = self.parser.add_argument_group("Scheduler")

        scheduler_group.add_argument(
            "--GET_INTERVAL",
            type=int,
            help="Time between GET requests for new price data",
            default=60, 
        )
       