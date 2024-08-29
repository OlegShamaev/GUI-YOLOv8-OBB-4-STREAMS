from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar, Optional, Dict, Any, Literal, Union
import json

from src.utils.general import ROOT
import os
from src.utils.logging_config import logger


FILE_PATH = os.path.join(ROOT, "config.json")
FILE_PATH_OUT = os.path.join(ROOT, "config_out.json")


###################################################################################


class TabConfig(BaseModel):
    tab_out: int
    yolo_name: str
    source_in: str
    source_value: Optional[Union[str, int]] = Field(
        ..., description="Source value must be a string or an integer"
    )
    confidence_threshold: float = Field(
        ..., gt=0, le=1, description="Confidence threshold must be between 0 and 1"
    )
    iou_threshold: float = Field(
        ..., gt=0, le=1, description="IoU threshold must be between 0 and 1"
    )
    frame_interval: int = Field(
        ..., ge=0, le=10, description="Frame interval must be between 0 and 10"
    )
    in_out_area: Optional[Literal["IN", "OUT"]]
    display_area: Any


class LastState(BaseModel):
    preference: bool
    db_confidence: float = Field(
        ..., gt=0, le=1, description="Confidence DB must be between 0 and 1"
    )
    db_use_conf_model: bool
    db_save: Literal["DataBase", "File", "Disabled"]
    last_opened_tab: int = Field(
        ..., ge=0, le=4, description="Last opened tab must be non-negative"
    )
    state_close_connection_pool: bool


class Config(BaseModel):
    last_state: LastState
    tabs: Dict[str, TabConfig]

    @classmethod
    def from_json(cls):
        try:
            with open(FILE_PATH, "r") as file:
                data = json.load(file)
                return cls(**data)
        except FileNotFoundError:
            logger.error("Config file not found. Creating a new one.")

    def to_json(self):
        try:
            with open(FILE_PATH, "w") as file:
                json.dump(self.dict(), file, indent=4)
        except Exception as e:
            logger.error(f"Error writing to JSON file: {e}")


###################################################################################


class DataBaseSettings(BaseSettings):
    db_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(..., env="DB_PORT")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASS: str = Field(..., env="DB_PASS")
    DB_NAME: str = Field(..., env="DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True  # Учитывать регистр переменных окружения
        extra = "ignore"  # Игнорировать переменные, которые не определены в модели


###################################################################################

config = Config.from_json()
db_settings = DataBaseSettings()
