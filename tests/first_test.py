from lib.controller.controller import Controller


class first_test(Controller):
    def __init__(self):
        super().__init__()

    def test_example(self):
        pass


if __name__ == '__main__':
    a = first_test()
    a.test_example()
    a.run_process()
