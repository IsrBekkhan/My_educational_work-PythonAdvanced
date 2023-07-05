import logging

logger = logging.getLogger("skillbox.worker3")


def worker3(x: int, y: int) -> int:
   logger.debug(f"Entered worker3({x}, {y})")

   result = x ** x
   logger.debug(f"Calculation result of worker3({x}, {y}) = {result}")

   return result
