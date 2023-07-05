# workers/worker1.py
import datetime
import logging
import time

logger = logging.getLogger("skillbox.worker1")


def worker1(x: int, y: int) -> int:
   # emulate a heisenbug
   logger.debug(f"Entered worker1({x}, {y})")

   current_ts = datetime.datetime.utcnow().timestamp()

   if int(current_ts) % 2 == 0 and (x == y):
       raise OSError("Something went wrong")

   time.sleep(0.5)
   result = x ** y
   logger.debug(f"Calculation result of worker1({x}, {y}) = {result}")

   return result
