import logging
from logging.handlers import RotatingFileHandler
import os
import json


class JSONFormatter(logging.Formatter):
    def __init__(self, datefmt=None):
        super().__init__(datefmt=datefmt)

    def format(self, record):
        record_dict = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "lineno": record.lineno,
        }
        if record.exc_info:
            record_dict["exc_info"] = self.formatException(record.exc_info)
        # include any structured extras
        for k, v in getattr(record, "__dict__", {}).items():
            if k not in ("msg", "args", "levelname", "levelno", "pathname", "filename", "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName", "created", "msecs", "relativeCreated", "thread", "threadName", "processName", "process"):
                try:
                    json.dumps({k: v})
                    record_dict[k] = v
                except Exception:
                    record_dict[k] = str(v)
        return json.dumps(record_dict, default=str)


def configure_logging(app_name: str = "SED"):
    """Configure root logging with console and rotating file handlers.
    If the environment variable `LOG_FORMAT` is set to `json`, logs will
    be emitted in structured JSON. Safe to call multiple times; if handlers
    already exist it will noop.
    """
    root = logging.getLogger()
    if root.handlers:
        return

    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        level = getattr(logging, log_level)
    except Exception:
        level = logging.INFO

    log_format = os.environ.get("LOG_FORMAT", "text").lower()

    if log_format == "json":
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    # File handler (rotating)
    logs_dir = os.path.join(os.getcwd(), "logs")
    try:
        os.makedirs(logs_dir, exist_ok=True)
        fh_path = os.path.join(logs_dir, f"{app_name}.log")
        fh = RotatingFileHandler(fh_path, maxBytes=5 * 1024 * 1024, backupCount=3)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        root.addHandler(fh)
    except Exception:
        # If file handler setup fails, at least the console handler exists.
        root.warning("Failed to set up file logging; continuing with console only")

    root.setLevel(level)
    root.info("Logging configured (level=%s, format=%s)", logging.getLevelName(level), log_format)
