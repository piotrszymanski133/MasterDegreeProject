from checker.log.parser.base_logs_parser import BaseLogsParser


class LogsParserFactory:

    def get_parser_for_image(self, image_name: str) -> BaseLogsParser:
        return None
