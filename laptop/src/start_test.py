import asyncio
from src.timers import CountdownTimer, TimerState
from src.analysis import Test, TestStatus

async def start_test(parent, test, test_status):
    try:
        total_duration = test.reps*(test.go_duration + test.rest_duration)

        test.end(test, test_status)

        await asyncio.sleep(test.countdown_duration)
        test_status.active = True
        await parent.tindeq.start_logging_weight()

        print(test_status.name, " Test starts!")
        test.end(test, test_status)

        print(test_status.name, " duration ", total_duration)
        await asyncio.sleep(total_duration)
        await parent.tindeq.stop_logging_weight()

        test_status.complete = True
        print(test_status.name, " done! ", Test.testing_complete(parent), Test.testing_active(parent))

        await asyncio.sleep(0.5)
        test.state = TimerState.IdleState
    except Exception as err:
        print(str(err))

