import GPUtil
import os
import tensorflow as tf


def configure_gpu_tf():
    """ This is an example for how to customise the search for a GPU for a specific job depending on
    hardware/organisational requirements. In this case, we have a machine with two GPUs on which we want to support
    three simultaneous GPU jobs (& unlimited CPU). """

    try:
        # locate available devices & set required environment variables
        available_device_ids = GPUtil.getFirstAvailable(order='first', maxLoad=0.7, maxMemory=0.7, attempts=1, interval=10)
        available_device_id = available_device_ids[0]
        os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
        os.environ['CUDA_VISIBLE_DEVICES'] = str(available_device_id)
        print(f"\n GPU Found! running on GPU:{available_device_id}\n")

        # set GPU configuration (use all GPU memory if device 0, else use <50% of memory)
        tf.debugging.set_log_device_placement(False)
        physical_gpu = tf.config.experimental.list_physical_devices('GPU')[0]

        if available_device_id == 0:
            tf.config.experimental.set_memory_growth(physical_gpu, True)
        else:
            tf.config.experimental.set_virtual_device_configuration(
                physical_gpu,
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4500)]
            )
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            assert len(logical_gpus) == 1, "error creating virtual GPU to fractionally use memory"

    # if we can't find a GPU, or they are all busy, default to using CPU
    except RuntimeError:
        print("\n No GPUs available... running on CPU\n")
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
