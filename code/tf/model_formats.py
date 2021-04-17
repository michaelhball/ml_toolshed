def convert_model_to_tflite(tflite_file, saved_model_dir, optimizations=None, target_spec=None):
    """ Converts SavedModel to tflite model with provided optimizations.

    :param tflite_file:
    :param saved_model_dir:
    :param optimizations:
    :param target_spec:
    :return:
    """

    try:
        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
        if optimizations is not None:
            converter.optimizations = optimizations
        if target_spec is not None:
            converter.target_spec.supported_types = target_spec
        tflite_model = converter.convert()
        tflite_file.write_bytes(tflite_model)
        return True
    except:
        log.error("Exception converting SavedModel --> tflite: \n", exc_info=True)
        return False
