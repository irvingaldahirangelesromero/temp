# shared_kernel/config/shared_settings.py

import os
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from shared_kernel.enums.database_enum import DatabaseEnum

class DatabaseSettingsDTO(BaseModel):
    host: str
    username: str
    password: str
    name: str
    port: int
    driver: Optional[str]
    driver_file: Optional[str]

class AWSSettingsDTO(BaseModel):
    region: str
    access_key_id: str
    secret_access_key: str

class SharedSettings:
    def __init__(self):
        load_dotenv()

    def get(self, key: str, default: str = None) -> str:
            return os.getenv(key, default)

    def get_aws_settings(self) -> AWSSettingsDTO:
        aws_settings = AWSSettingsDTO(
            region=os.getenv("AWS_REGION"),
            access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        return aws_settings

    def get_mariadb_settings(self, database: DatabaseEnum) -> DatabaseSettingsDTO:
        driver = os.getenv("MARIADB_DRIVER")
        driver_file = os.getenv("MARIADB_DRIVER_PATH")

        if database.BENGINE == database:
            return DatabaseSettingsDTO(
                host=os.getenv("MARIADB_HOST_BENGINE"),
                username=os.getenv("MARIADB_USER_BENGINE"),
                password=os.getenv("MARIADB_PASSWORD_BENGINE"),
                name=os.getenv("MARIADB_NAME_BENGINE"),
                port=os.getenv("MARIADB_PORT_BENGINE"),
                driver=driver,
                driver_file=driver_file
            )

        return DatabaseSettingsDTO(
            host=os.getenv("MARIADB_HOST_CLEVER"),
            username=os.getenv("MARIADB_USER_CLEVER"),
            password=os.getenv("MARIADB_PASSWORD_CLEVER"),
            name=os.getenv("MARIADB_NAME_CLEVER"),
            port=os.getenv("MARIADB_PORT_CLEVER"),
            driver=driver,
            driver_file=driver_file
        )

shared_settings = SharedSettings()
