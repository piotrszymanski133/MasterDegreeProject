from checker.factory.checkers_factory import CheckersFactory


def run_checkers():
    checkers = CheckersFactory().create_checkers()
    [checker.run_checker() for checker in checkers]


if __name__ == '__main__':
    run_checkers()

