import asyncio
from src.timers import CountdownTimer, TimerState
from src.analysis import Test, TestStatus

async def start_test_rfd(cft, rfd, test):
    try:
        cft.timer_rfd.reps = 1
        cft.timer_rfd.end(cft.timer_rfd, test)

        await asyncio.sleep(cft.timer_rfd.countdown_duration)
        test.active = True
        await cft.tindeq.start_logging_weight()

        print("Rfd Test starts!")
        rfd.end(rfd, test)

        print("go_duration ", rfd.go_duration)
        await asyncio.sleep(rfd.go_duration)
        await cft.tindeq.stop_logging_weight()

        test.complete = True
        print("Rfd Test done! ", Test.testing_complete(cft), Test.testing_active(cft))

        await asyncio.sleep(0.5)
        cft.timer_rfd.statex = TimerState.IdleStatex
    except Exception as err:
        print(str(err))
    # finally:
    # await cft.tindeq.disconnect()
    # cft.tindeq = None
