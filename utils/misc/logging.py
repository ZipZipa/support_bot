import logging
from datetime import date


log_format = (u'[%(levelname)-4s] [%(asctime)s] [LINE:%(lineno)-3s] '
              u'[%(filename)-15s] %(message)s')

curr_date = date.today().strftime(r"%d-%m-%Y")

logfile = (r'C:\Users\19893422\Documents\support_bot\data\logs\dops-'
           f'{curr_date}.log')

logging.basicConfig(format=log_format,
                    level=logging.INFO,
                    filename=logfile,
                    filemode='a',
                    # level=logging.DEBUG,
                    # Можно заменить на другой уровень логгирования.
                    )
