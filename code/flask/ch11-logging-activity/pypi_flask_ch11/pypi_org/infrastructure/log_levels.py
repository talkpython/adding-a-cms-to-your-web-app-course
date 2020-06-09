class LogLevel:
    debug = "DEBUG"
    info = "INFO"
    notice = "NOTICE"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"

    @staticmethod
    def parse(level_text: str) -> str:
        if not level_text:
            raise Exception("Level text must be specified")

        level_text = level_text.upper().strip()

        if level_text == LogLevel.debug:
            return LogLevel.debug
        elif level_text == LogLevel.info:
            return LogLevel.info
        elif level_text == LogLevel.notice:
            return LogLevel.notice
        elif level_text == LogLevel.warning:
            return LogLevel.warning
        elif level_text == LogLevel.error:
            return LogLevel.error
        elif level_text == LogLevel.critical:
            return LogLevel.critical
        else:
            raise Exception(f"The level text {level_text} is not a supported log level.")
