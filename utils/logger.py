import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv


class Logger:
    @staticmethod
    async def start_logger() -> None:
        load_dotenv()
        log_file_path = os.getenv('LOG_DIR') + datetime.now().strftime("%d-%m-%Y") + ".log"
        log_format = "%(asctime)s.%(msecs)03d *** %(levelname)s : %(lineno)d *** %(message)s"
        log_date_format = "%d-%m-%Y %H:%M:%S"

        """ Function to Initiate the Logger """
        if not os.path.exists(os.getenv('LOG_DIR')):
            os.makedirs(os.getenv('LOG_DIR'), exist_ok=True)

        logging.basicConfig(filename=log_file_path, format=log_format, level=logging.INFO,
                            datefmt=log_date_format, force=True)

    @staticmethod
    async def error_log(file_name: str, func_name: str, error) -> None:
        try:
            if not isinstance(error, str):
                error = f"{error} | Line {error.__traceback__.tb_lineno}."

            logging.error(f"{file_name} | {func_name} | Exception : {error}")
            print(f"{datetime.now()} | {file_name} | {func_name} | Exception : {error}")
        except Exception as error:
            logging.error(f"{__name__} | errorLog | Exception : {error}")
            print(f"{datetime.now()} | {__name__} | errorLog | Exception : {error}")

    @staticmethod
    async def info_log(msg: str) -> None:
        logging.info(msg=msg)
        print(f"{datetime.now()} | {msg}")


if __name__ == '__main__':
    asyncio.run(Logger.start_logger())
