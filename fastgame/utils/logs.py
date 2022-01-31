"""
fastgame.utils.logs

Fastgame日志工具。
底层模块。
"""

import arrow


def log(level: str, message: str):
    """
    输出一条日志信息。
    
    :param level: 日志级别。
    :param message: 日志信息。
    """
    now = arrow.now().format('YYYY-MM-DD HH:mm:ss')
    text = f'{now} {level} "{message}"'
    print(text)


def info(message: str):
    """
    输出一条INFO级别日志信息。

    :param message: 日志信息。
    """
    log('INFO', message)
    

def debug(message: str):
    """
    输出一条DEBUG级别日志信息。

    :param message: 日志信息。
    """
    log('DEBUG', message)
    

def warning(message: str):
    """
    输出一条WARNING级别日志信息。

    :param message: 日志信息。
    """
    log('WARNING', message)
