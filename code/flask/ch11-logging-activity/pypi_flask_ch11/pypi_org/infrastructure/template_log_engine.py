import logbook
from markdown_subtemplate import logging
from markdown_subtemplate.logging import LogLevel

log = logbook.Logger('Subtemplates')


class TemplateLogger(logging.SubtemplateLogger):
    def verbose(self, text: str):
        if self.should_log(LogLevel.verbose, text):
            log.trace(text)

    def trace(self, text: str):
        if self.should_log(LogLevel.trace, text):
            log.trace(text)

    def info(self, text: str):
        if self.should_log(LogLevel.info, text):
            log.info(text)

    def error(self, text: str):
        if self.should_log(LogLevel.error, text):
            log.error(text)
