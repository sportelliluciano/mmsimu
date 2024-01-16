import logging
import sys

from mmsimu.log import logger
from mmsimu.memory_manager import MemoryManager
from mmsimu.instance import set_instance


def mmsimu_init(main_function, heap_size=1024):
    """
    Starts the simulated memory manager and runs the main_function.

    heap_size: Maximum heap size in bytes. If the result of an
               allocation would make the total allocated bytes
               exceed this value, the allocation will fail.
    """
    for arg in sys.argv[1:]:
        if arg == "--log-alloc":
            logger.getChild("alloc").setLevel(logging.INFO)
        if arg == "--log-uninit":
            logger.getChild("uninit").setLevel(logging.INFO)

    with MemoryManager(heap_size) as mm:
        set_instance(mm)
        main_function()
