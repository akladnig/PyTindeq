import asyncio
from src.timers import CountdownTimer, TimerState
from src.analysis import Test, TestStatus

async def start_test_cft(self, cft, reps, test):
    try:
        cft.end(cft, test)

        await asyncio.sleep(cft.countdown_duration)
        test.active = True
        await self.tindeq.start_logging_weight()

        print("CFT Test starts! ", cft.go_duration, cft.rest_duration)
        cft.end(cft, test)

        total_duration = reps*(cft.go_duration + cft.rest_duration)+10
        print("Cft duration", total_duration)
        # cft.end(cft, test)
        await asyncio.sleep(total_duration)
        await self.tindeq.stop_logging_weight()

        test.complete = True
        print("CFT test complete")

        await asyncio.sleep(0.5)
        cft.statex = TimerState.IdleStatex
    except Exception as err:
        print(str(err))
    finally:
        await self.tindeq.disconnect()
        self.tindeq = None


