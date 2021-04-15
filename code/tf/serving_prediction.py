import grpc
import numpy as np

from tensorflow import make_tensor_proto
from tensorflow_serving.apis.predict_pb2 import PredictRequest
from tensorflow_serving.apis.prediction_service_pb2_grpc import PredictionServiceStub


def format_grpc_request(model_name, model_version, model_signatures, signature_name, inputs_to_predict):
    """ Formats a given GRPC request (for sending to TF-serving model server)

    :param model_name: (str) name of model in TF-serving model server that you want to predict with
    :param model_version: (int) version of model in TF-serving model server that you want to predict with
    :param model_signatures: (dict)
    :param signature_name: (dict)
    :param inputs_to_predict: (list(dict(object))) list of inputs (where each input is a dict mapping from input name
                                                    to input object, named according to the model_spec)
    :return: GRPC request object
    """

    try:
        tf_request = PredictRequest()
        tf_request.model_spec.name = model_name
        tf_request.model_spec.version.value = int(model_version)
        tf_request.model_spec.signature_name = signature_name
        model_spec_inputs = model_signatures[signature_name]["input"]

        grpc_inputs = {k: [] for k in model_spec_inputs.keys()}
        for model_input in inputs_to_predict:
            for k in model_spec_inputs.keys():
                grpc_inputs[k].append(model_input[k])

        for k, v in model_spec_inputs.items():
            tf_input = np.array(grpc_inputs[k])
            assert tf_input.shape[1:] == tuple(v['shape'][1:])                  # make sure inputs dim == model_spec
            tensor_proto = make_tensor_proto(tf_input, shape=tf_input.shape)
            tf_request.inputs[k].CopyFrom(tensor_proto)
        return tf_request
    except Exception as e:
        print(e)
        return False


def send_prediction_request(host, port, model_name, model_version, model_signatures, signature_name, inputs_to_predict,
                            batch_size):
    """ Sends sequence of inputs to a TF-serving model server for prediction

    :param host: (str) TF-serving model server host
    :param port: (int) TF-serving model server port
    :param model_name: (str) name of model in TF-serving model server that you want to predict with
    :param model_version: (int) version of model in TF-serving model server that you want to predict with
    :param model_signatures: (dict)
    :param signature_name: (dict)
    :param inputs_to_predict: (list(dict(object))) list of inputs (where each input is a dict mapping from input name
                                                    to input object, named according to the model_spec)
    :param batch_size: (int) desired batch size with which to batch predictions
    :return list of model predictions
    """

    # TODO: add support for REST API
    # TODO: handle multiple outputs, not assuming only one

    try:
        # create connection stub to TF serving server
        channel = grpc.insecure_channel(f'{host}:{port}')
        stub = PredictionServiceStub(channel)

        # format request for each batch & get result from server
        model_spec_output_name = list(model_signatures[signature_name]['output'].keys())[0]
        input_batches = [inputs_to_predict[i:i + batch_size] for i in range(0, len(inputs_to_predict), batch_size)]

        # format request for each batch & get result from server
        predictions = []
        for input_batch in input_batches:
            grpc_request = format_grpc_request(model_name, model_version, model_signatures, signature_name, input_batch)
            result = stub.Predict(grpc_request)
            batch_predictions = list(result.outputs[model_spec_output_name].float_val)
            predictions += list(batch_predictions)

        return predictions
    except Exception as e:
        print(e)
        return False
