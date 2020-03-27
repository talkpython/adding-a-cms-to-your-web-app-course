import logbook
from markdown_subtemplate import logging
from markdown_subtemplate.logging import LogLevel

log = logbook.Logger('Markdown')


class SubTemplateLogger(logging.SubtemplateLogger):

    def verbose(self, text: str):
        if not self.should_log(LogLevel.verbose, text):
            return

        log.trace(text)

    def trace(self, text: str):
        if not self.should_log(LogLevel.trace, text):
            return

        log.trace(text)

    def info(self, text: str):
        if not self.should_log(LogLevel.info, text):
            return

        log.info(text)

    def error(self, text: str):
        if not self.should_log(LogLevel.error, text):
            return

        log.error(text)
