_global_heap_instance = None


def set_instance(instance):
    global _global_heap_instance

    _global_heap_instance = instance


def get_instance():
    return _global_heap_instance
