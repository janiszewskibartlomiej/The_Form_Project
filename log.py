import logging


def logi():
    formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')

    logger_plikow = logging.getLogger('log_do_pliku')

    file_handler = logging.FileHandler('form_app.log')
    file_handler.setFormatter(formatter)

    logger_plikow.addHandler(file_handler)
    logger_plikow.setLevel(logging.INFO)
    return logger_plikow
