import asyncio
from src.timers import CountdownTimer, TimerState
from src.analysis import Test, TestStatus

async def start_test_max(cft, maxt, test):
    try:
        cft.timer_max.reps = 1
        cft.timer_max.end(cft.timer_max, test)

        await asyncio.sleep(cft.timer_max.countdown_duration)
        test.active = True
        await cft.tindeq.start_logging_weight()

        print("Max Test starts!")
        maxt.end(maxt, test)

        print("go_duration ", maxt.go_duration)
        await asyncio.sleep(maxt.go_duration)
        await cft.tindeq.stop_logging_weight()

        test.complete = True
        print("Max Test done! ", Test.testing_complete(cft), Test.testing_active(cft))

        await asyncio.sleep(0.5)
        cft.timer_max.statex = TimerState.IdleStatex
    except Exception as err:
        print(str(err))
    # finally:
    # await cft.tindeq.disconnect()
    # cft.tindeq = None
