import os

def handler_path(context: str) -> str:
    return context.split(os.getcwd())[1][1:].replace('\\', '/')