import asyncio
from src.timers import CountdownTimer, TimerState
from src.analysis import Test, TestStatus

async def start_test_cft(self, cft, reps):
    try:
        cft.end(cft)
        await asyncio.sleep(cft.countdown_duration)
        TestStatus.active = True
        await self.tindeq.start_logging_weight()

        print("CFT Test starts! ", cft.go_duration, cft.rest_duration)
        total_duration = reps*(cft.go_duration + cft.rest_duration)
        print(total_duration)
        cft.end(cft)
        await asyncio.sleep(total_duration)
        await self.tindeq.stop_logging_weight()
        print("CFT test complete")
        TestStatus.complete = True
        await asyncio.sleep(0.5)
        TimerState.IdleStatex
    except Exception as err:
        print(str(err))
    finally:
        await self.tindeq.disconnect()
        self.tindeq = None