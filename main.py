from checker.factory.checkers_factory import CheckersFactory
from checker.result.checker_result import CheckerResult
from logger.formatter import get_logger


class MainChecker:

    def run_checkers(self):
        logger = get_logger(self.__class__.__name__)
        checkers = CheckersFactory().create_checkers()
        results = [checker.run_checker() for checker in checkers]
        if results.count(CheckerResult.FAILED) > 0:
            logger.warning("Problems detected! Please fix the issues described above and run this application again!")
        else:
            logger.info("Your Docker cluster is valid!")

if __name__ == '__main__':
    main_checker = MainChecker()
    main_checker.run_checkers()

