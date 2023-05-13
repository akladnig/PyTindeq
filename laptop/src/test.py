import asyncio
from src.timers import CountdownTimer, TimerState


class TestStatus:
    def __init__(self, name):
        self._active = False
        self._complete = False
        self._name = name

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, state):
        self._active = state

    @property
    def complete(self):
        return self._complete

    @complete.setter
    def complete(self, state):
        self._complete = state

    @property
    def name(self):
        return self._name


class Test:
    TestingStarted = False
    MaxLeft = TestStatus("Max Left")
    MaxRight = TestStatus("Max Right")
    Cft = TestStatus("CFT")
    RfdLeft = TestStatus("RFD Left")
    RfdRight = TestStatus("RFD Right")

    def testing_complete(self):
        # testing_complete = (
        #     Test.Cft.complete
        #     and Test.MaxLeft.complete
        #     and Test.MaxRight.complete
        #     and Test.RfdLeft.complete
        #     and Test.RfdRight.complete
        # )
        testing_complete = Test.RfdRight.complete

        return testing_complete

    def testing_active(self):
        testing_active = (
            Test.Cft.active
            or Test.MaxLeft.active
            or Test.MaxRight.active
            or Test.RfdLeft.active
            or Test.RfdRight.active
        )
        return testing_active

    def print_test_status(self):
        print(
            "Testing Complete: ",
            Test.testing_complete(self),
            "Testing Active: ",
            Test.testing_active(self),
        )


class TestResults:
    body_weight = 0
    max_left = 0
    max_right = 0
    rfd_left = 0
    rfd_right = 0
    peak_load = 0
    critical_load = 0
    critical_load_percent = 0


async def start_test(parent, test, test_status):
    try:
        total_duration = test.reps * (test.go_duration + test.rest_duration)

        test.end(test, test_status)

        test_status.active = True
        await asyncio.sleep(test.countdown_duration-1)
        await parent.tindeq.start_logging_weight()
        await asyncio.sleep(1)

        print(test_status.name, " Test starts!")
        test.end(test, test_status)

        print(test_status.name, " duration ", total_duration)
        await asyncio.sleep(total_duration)
        await parent.tindeq.stop_logging_weight()

        test_status.complete = True

        await asyncio.sleep(0.5)
        test.state = TimerState.IdleState
    except Exception as err:
        print(str(err))
