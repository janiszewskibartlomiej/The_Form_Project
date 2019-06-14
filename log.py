import logging


def add_log():
    formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')

    log_to_file = logging.getLogger('log_to_file')

    file_handler = logging.FileHandler('from_app.log')
    file_handler.setFormatter(formatter)

    log_to_file.addHandler(file_handler)
    log_to_file.setLevel(logging.INFO)

    return log_to_file
