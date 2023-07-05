import datetime
import logging
import time

logger = logging.getLogger("skillbox.worker2")


def worker2(x: int, y: int) -> int:
   logger.debug(f"Entered worker2({x}, {y})")
   # emulate a heisenbug
   current_ts = datetime.datetime.utcnow().timestamp()

   if int(current_ts) % 2 == 0 and y == 1:
       raise ValueError("Something went wrong")

   time.sleep(0.1)

   result = y ** x

   logger.debug(f"Calculation result of worker2({x}, {y}) = {result}")

   return result