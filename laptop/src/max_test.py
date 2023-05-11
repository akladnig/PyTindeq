import asyncio
from src.timers import CountdownTimer, TimerState
from src.analysis import Test, TestStatus

async def start_test_max(cft, maxt):
    try:
        cft.timer_max.reps = 1
        cft.timer_max.end(cft.timer_max)
        print("start Countdown " +str(cft.timer_max.go_duration))

        await asyncio.sleep(cft.timer_max.countdown_duration)
        print("start logging")
        TestStatus.active = True
        print("start_test_max Active " +str(TestStatus.active))

        await cft.tindeq.start_logging_weight()

        print("Max Test starts!")
        maxt.end(maxt)

        print(maxt.go_duration)
        await asyncio.sleep(maxt.go_duration)
        await cft.tindeq.stop_logging_weight()
        print("Max Test done!")

        TestStatus.complete = True
        await asyncio.sleep(0.5)
        maxt.state = TimerState.IdleStatex
    except Exception as err:
        print(str(err))
    # finally:
    # await cft.tindeq.disconnect()
    # cft.tindeq = None
