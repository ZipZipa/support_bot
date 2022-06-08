import logging
from datetime import date


log_format = (u'[%(levelname)-4s] [%(asctime)s] [LINE:%(lineno)-3s] '
              u'[%(filename)-15s] %(message)s')

curr_date = date.today().strftime(r"%d-%m-%Y")

logfile = (r'data\logs\dops-'
           f'{curr_date}.log')

logging.basicConfig(format=log_format,
                    level=logging.INFO,
                    filename=logfile,
                    filemode='a',
                    encoding='utf-8'
                    # level=logging.DEBUG,
                    # Можно заменить на другой уровень логгирования.
                    )
