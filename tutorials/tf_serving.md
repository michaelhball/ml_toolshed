# Tensorflow Serving

// EMPHASIZE HERE THAT MOST TUTORIALS ARE SHIT, AND DON'T GET GET THE DEEPEST PARTS OF WHAT THE 
REQUIREMENTS ARE FOR DEPLOYING SOMETHING IN PRODUCTION

Despite the growing popularity of Pytorch (and for good reason), Tensorflow Serving is still 
my go to solution for quickly achieving production-grade model serving.  The Tensorflow website claims that that tf-serving
'makes it easy to deploy new algorithms and experiments, while keeping the same server architecture and APIs,' 
and while Tensorflow documentation shouldn't always be taken at face value, in this case it's spot on. 

This tutorial is targeted at achieving a standard (but still realistic) small-scale production environment: a 
model server running on a single machine, serving any number of models. That being said, as the server is run using 
Docker, it lends itself easily to scaling. I also include a brief snipper [here]( demonstrating how easy it is to 
incorporate TF serving into a more complex docker-compose setup. The [7'](#7') version demonstrates how to run a non-optimized model server on the CPU, while the steps required for 1) 
building a system optimized server, and 2) using GPUs are outlined in the [LP](#lp) version.

## :books: Table of Contents

* [7'](#:musical_note:-7')
* [LP](#LP)
    * [Building your Docker image]($1-building-your-docker-image)
    * [SavedModels]($2-creating-a-savedmodel-servable)
    * [Config]($3-config)
    * [Running the server]($4-running-the-server)
    * [Using the server]($5-using-the-server)
    * [Docker-Compose](6-docker-compose)
  
--- 

## :musical_note: 7'

1. Run ```$ docker pull tensorflow/serving``` to pull the base docker image 
2. Upload models (in TF [SavedModel](https://www.tensorflow.org/guide/saved_model) format) to S3 using 
the following structure. 
    ```
    models
    │
    │
    └───model_1
    │   │   
    │   └───0
    │   │   │   saved_model.pb
    │   │   └── variables
    |   │ 
    │   └───1
    │       │   saved_model.pb
    │       └── variables
    │
    └───model_2
        │
       ... 
    ```
   For instructions on saving models in this format, refer to [this tutorial](/tutorials/tf_model_formats.md) 
   and the functions in [```model_formats.py```](/code/tf/model_formats.py). 
3. Create a config ```file models.config``` and upload to S3, e.g. at 
```s3://bucket_name/configs/models.config```
    ```
    model_config_list: {
        config: {
            name: "model_1",
            base_path: "s3://model_bucket_name/models",
            model_platform: "tensorflow",
            model_version_policy: {
                all: {}
            }
        }
    }
    ``` 
4. Run the server!
    ```
    $ docker run 
             -d --rm 
             --name tf_serving_7_inch        
             -p 8500:8500 -p 8501:8501
             -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
             -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
             -e AWS_REGION="eu-central-1"
             -e AWS_ENDPOINT="s3.eu-central-1.amazonaws.com"
             -e AWS_LOG_LEVEL=3
             -e TF_CPP_MIN_LOG_LEVEL=3
             -t tensorflow/serving
             --model_config_file=s3://bucket_name/configs/models.config
    ``` 
   - explanation for all arguments here & more are given [below]().
5. Requests can be made using either the gRPC (8500) or REST (8900) endpoints. Example code for sending 
data to a model server is provided in [```serving_predictions.py```](/code/tf/serving_prediction.py)

## :musical_score: LP

### 1. Building your docker image

Let's start by creating an optimized CPU version of the server first. You probably noticed in the 
startup logs when running the default ```tensorflow/serving``` docker image a warning message 
that looks something like this
```
I external/org_tensorflow/tensorflow/core/platform/cpu_feature_guard.cc:141]
Your CPU supports instructions that this TensorFlow binary was not compiled to
use: AVX2 FMA
```
where ```AVX2``` and ```FMA``` could be any one of a number of different support instructions.

This suggests the server isn't optimized for the CPU it's of the machine it's running on. Luckily, 
it's easy to create a Docker image that's optimized for your specific CPU:

1. Clone the TF Serving github project
    ```bash
    $ git clone https://github.com/tensorflow/serving
    $ cd serving 
    ```
2. Build a helper image with a CPU-optimized ModelServer: 
    ```
    $ docker build --pull 
                   -t tensorflow-serving-intermediate 
                   -f tensorflow_serving/tools/docker/Dockerfile.devel .
   ```
3. Build a proper _serving_ image with the optimized intermediate image as base
   ```
   $ docker build -t tensorflow-serving-optimized 
                  --build-arg TF_SERVING_BUILD_IMAGE=tensorflow-serving-intermediate 
                  -f tensorflow_serving/tools/docker/Dockerfile 
   ```

And that's _almost_ all there is to it. There are two caveats:
 
1. The first build command consumes a lot of RAM, so you may want to cap the amount available 
to the process by specifying ```--local_ram_resources=2048``` (or a smaller number). This 
argument needs to be passed as a build option to the docker process, for example
    ```
    $ docker build --pull
                   --build-arg TF_SERVING_BUILD_OPTIONS="--local_ram_resources=2048"
                   -t tensorflow-serving-intermediate 
                   -f tensorflow_serving/tools/docker/Dockerfile.devel . 
    ``` 
    
2. If you are not building the ModelServer image on the machine where it will be running (i.e. almost all 
cases in real life), you'll have to specify the optimizations manually. The full set of possible 
optimizations is listed [here](https://www.tensorflow.org/tfx/serving/setup#optimized_build), though a 
discussion of when to use which is out of the scope of this tutorial (check [this]() out for a better 
explanation than I could ever hope to give). These arguments can be passed to the docker build process in 
the same way as the RAM limiter above. For example, to run the build process with the ```AVX2``` and ```FMA``` 
instruction sets (to resolve the error message listed above) you would run
    ```
    $ docker build --pull
                   --build-arg TF_SERVING_BUILD_OPTIONS="--copt=-mavx2 --copt=-mfma"
                   -t tensorflow-serving-intermediate 
                   -f tensorflow_serving/tools/docker/Dockerfile.devel . 
    ```

### 2. Creating a SavedModel [servable](https://www.tensorflow.org/tfx/serving/architecture#servables) 

Please skip  this section if you know how to save a Tensorflow model as a SavedModel and upload it to S3 
(or wherever your models will be stored).

To use the Tensorflow ModelServer, you first need to save your models in [SavedModel](https://www.tensorflow.org/guide/saved_model), 
format (basically a low-level representation of a complete Tensorflow program that _does not_ require the original model 
building code in order to run). As with all things Tensorflow, there are many confusing and conflicting APIs for 
saving models in said format.

In this section I will just give a brief outline demonstrating how to save a model in SavedModel format and 
upload it to S3. For an in-depth discussion of the SavedModel format, the breadth of available APIs, 
converting between model formats, and optimizing models for production, please refer to my other 
tutorial on [Tensorflow model formats](/tutorials/tf_model_formats.md) and the supporting code in 
[serving_models.py](/code/tf/model_formats.py)

Imagine you have a simple tensorflow model as outlined in the snippet below (though this works equally 
for complex custom models), then saving in SavedModel format is as easy as the one line command.

```python
import numpy as np
import tensorflow as tf

from tensorflow import keras as K
from tensorflow.keras.models import Sequential



# imagine you have the following simple model (the saving is identical for real-life use cases)
inputs = K.Input(shape=(32,))
outputs = K.layers.Dense(1)(inputs)
model = K.Model(inputs, outputs)
model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(np.random.random((128, 32)), np.random.random((128, 1)))

# method 1
model.save('my_model')

# method 2 
save_dir = '~/models'
tf.saved_model.save(model, save_dir)
```

The [first method](https://www.tensorflow.org/guide/keras/save_and_serialize) is the default high-level saving 
mechanism for Keras models. I recommend to always use the [second function](https://www.tensorflow.org/api_docs/python/tf/saved_model/save), 
as this provides far greater flexibility and control. For example, the ```saved_model.save()``` function takes an 
optional ```signatures``` argument that controls which methods in your model object will be exposed to 
programs using your model (i.e. the Tensorflow ModelServer).

The result of saving your model in this format is a directory containing ```saved_model.pb``` (storing model 
architecture, training configuration, optimizer losses, etc.), ```variables``` (storing the weights), and 
```assets``` (optionally storing extra files needed by more complex Tensorflow graphs).     



Once again, please refer [here](/tutorials/tf_model_formats.md) for my in-depth discussion of the SavedModel format.

Lastly, SavedModel file paths should follow a convention of ```<model_name>/<model_version>/...```, where model 
versions start at 0 and increment.

#### Uploading SavedModels to S3

It is by no means a requirement to store your models in S3, but it's a pretty great system, allowing you 
to easily disentangle the deployment of new models from the deployment of new application code, with no 
downtime. Of course, other cloud providers work too. AWS is just what I use, so that's what I'lll outline 
here. 

### 3. Config

This section refers to the various ways that the ModelServer can be customized, in many cases to take it 
to the level required for a production system. A complete guide to all possible configuration options can be 
found [here](https://www.tensorflow.org/tfx/serving/serving_config), but in this section I will point out and 
explain a few that I think are most useful.

My view is that the first type of config file (specifying the details of your models to serve) should be considered
essential, but the other two are optional and depend on your use case.  

#### Model Config

The quickest way to specify which models your server should use is via the ```--model_name``` and ```--model_base_path```
flags, but I _always_ opt to spend the few seconds extra it takes to create a Model Server config file. Using a 
config file allows you to
1. serve multiple types of models at a time with low overhead on your part
2. version your models and deploy a new version with _no_ downtime (while still being able to use the old version) 

Using a model config file gives you the extensibility needed to change any config settings as your needs develop, all while 
keeping the server live. 

The config file itself is a [ModelServerConfig protocol buffer](https://github.com/tensorflow/serving/blob/master/tensorflow_serving/config/model_server_config.proto#L76),
but you don't really have to worry about that. This is how I structure my ```models.config``` file _every_ time

```
model_config_list: {
    config: {
        name: <model_1_name>
        base_path: "s3://<bucket_name>/models/<model_1_name>"
        model_platform: "tensorflow"
        model_version_policy: {
            specific: {
                versions: 0
                versions: 1
                versions: 2
            }
        }
        version_labels: {
            key: 'retiring'
            value: 0
        }
        version_labels: {
            key: 'live'
            value: 1
        }
        version_labels: {
            key: 'test'
            value: 2
        }
    }
    config: {
        name: <model_2_name>
        base_path: "s3://<bucket_name>/models/<model_2_name>"
        model_platform: "tensorflow"
        model_version_policy: {
            specific {
                versions: 0
            }
        }
    }
}
``` 

It is possible to specify ```all: {}``` for the ```model_version_policy``` rather than writing out versions 
manually, but I recommend against it. The method above is better for two reasons:
1. it's easy to use the config file as a reference to understand exactly which models the server is serving 
at any given time,
2. it prevents any issues with the server loading new models as they added (when using a config file 
specifying all versions, I have frequently run into issues where the server does not automatically pull 
new models, inevitably requiring either a reboot or a 
[manual request](https://github.com/tensorflow/serving/blob/master/tensorflow_serving/apis/model_service.proto#L22) 
for reloading models).

In addition, the config file above is just a text file that in my case sits in S3. So it's easy to build 
into the application code the logic that automatically turns the ```test``` into the ```live``` model and 
the ```live``` into the ```retiring``` (when some criteria is met).

The commands needed to tell the server to use this config file are outlined in the [next section](#4-running-the-server).  

#### Batching Config

In order to improve the performance of the ModelServer, you'll probably want to configure batching (batching in this 
case refers to the server grouping together 'multiple inference requests it receives from clients and process(ing) 
them in a batch'<sup>[1](https://github.com/tensorflow/serving/issues/882)</sup>). So if your application 
won't be sending any parallel client requests, you can safely skip this section. You should still perform 
client side batching as normal, meaning that each request to the server contains a batch of input data. 

If your application _will_ involve the model server handling requests in parallel, you will already see a 
benefit from enabling the default batching settings (the flag for which is outlined in 
section [4.](#4-running-the-server) below). That being said, it is possible to optimize the performance 
beyond the default, though the optimization process is more of an art than a science, and very system 
dependent. As this article is focused on a CPU-optimized TF-serving setup, here is the  standard 
```batching.config``` file I use for a [CPU setup](https://github.com/tensorflow/serving/blob/master/tensorflow_serving/batching/README.md#cpu-only-one-approach).

```
batch_timeout_micros: { value: 0 },
max_batch_size: { value: 128 },
max_enqueued_batches: { value: 1000000 },
num_batch_threads: { value: 8},
```
 
If you're so inclined, you can refer [here](https://github.com/tensorflow/serving/blob/master/tensorflow_serving/batching/README.md) 
for a more in-depth look at how batching works under the hood.

#### Monitoring Config

The last type of config file you can specify is a monitoring config file allowing you to better understand of the 
health of your model server. The ```monitoring.config``` file I use is
 
```
prometheus_config: {
    enable: true,
    path: "/monitoring/prometheus/metrics"
}
```

which exposes metrics at ```http://<host_name>:8501/monitoring/prometheus/metrics``` (though you have to 
expose the REST endpoint to access these logs, even if you only want to use the gRPC endpoint for 
requesting predictions. More on this [below](#.-docker-compose)).

### 4. Running the server

It's time for the big moment! Finally we can run the server. The command here is almost identical to that 
used in the [7'](#7') version, but here we'll discuss in detail each argument (and add a few more). Assuming you 
have set up config files outlined in the [previous](#3-config) section, the command we'll use to run 
the server is:
```
$ docker run 
         -d --rm 
         --name tf_serving_LP        
         -p 8500:8500 -p 8501:8501
         -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
         -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
         -e AWS_REGION="eu-central-1"
         -e AWS_ENDPOINT="s3.eu-central-1.amazonaws.com"
         -e AWS_LOG_LEVEL=3
         -e TF_CPP_MIN_LOG_LEVEL=3
         -t tensorflow-serving-optimized
         --model_config_file="s3://bucket_name/configs/models.config"
         --monitoring_config_file="s3://bucket_name/configs/monitoring.config"
         --enable_batching
         --batching_parameters_file="s3://bucket_name/configs/batching.config"
         --model_config_file_poll_wait_seconds=216000
``` 
Phew! Alrighty, let's go through that line by line and outline what each and every argument is doing.
* ```-d``` and ```--rm``` are standard Docker run [arguments](https://docs.docker.com/engine/reference/commandline/run/), 
meaning that we will detach from the container on running and that the container will be removed upon exiting. 
* ```--name tf_serving_LP``` here we are just giving our container a name with which to address it when 
using any further Docker commands.
* ```-p 8500:8500 -p 8501:8501``` here we are publishing Docker's ports 8500 and 8501 
(where the gRPC and REST endpoints of the ModelServer are running respectively) to our machines ports 
8500 and 8501. The machine's ports are on the left of the colon, the container's on the right.
*  ```-e AWS_*``` these arguments are standard AWS credentials, always necessary if we want to serve 
models from S3. You can refer [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html) 
for more details on these environment variables.
* ```-e AWS_LOG_LEVEL=3``` and ```-e TF_CPP_MIN_LOG_LEVEL=3``` are both needed to prevent a small 
[logging bug](https://github.com/tensorflow/serving/issues/789) from occurring that makes the 
server logs unreadable.
* ```-t tensorflow-serving-optimized``` specifies which Docker image to run, in this case the 
CPU-optimized image we creating in section [1](#1.building-your-docker-image).
* ```--model_config_file="s3://bucket_name/configs/models.config"``` points the server to your model 
config file
* ```--monitoring_config_file="s3://bucket_name/configs/monitoring.config"``` points the server to your 
monitoring config file
* ```--enable_batching``` allows the server to batch requests (outlined in detail [above](#3-config))
* ```--batching_parameters_file="s3://bucket_name/configs/batching.config"``` is needed in addition to 
the above command to allow the server to batch requests according to your config
* ```--model_config_file_poll_wait_seconds=216000``` specifies how often TF should check whether your 
config file has changed (and => whether new models are ready to be downloaded). In this case I've set 
it only to every hour, but it could be much more often (though the flag should be set to prevent 
[this bug](https://github.com/tensorflow/serving/issues/1291).

You can read about a few additional arguments [here](https://www.tensorflow.org/tfx/serving/serving_config), 
s  

### 5. Using the server

To verify that the model server is running, you can send a GET request to the default server endpoint
```
$ curl http://<host_name>:8501/v1/models/<model_name>
```
, where a successful response might look something the following:
```
{
    "model_version_status": [
        {
            "version": "1",
            "state": "AVAILABLE",
            "status": {
            "error_code": "OK",
            "error_message": ""
        },
        {
            "version": "0",
            "state": "AVAILABLE",
            "status": {
            "error_code": "OK",
            "error_message": ""
        },
    ]
}
``` 

In addition, if you've have included a ```monitoring.config``` file as outlined above you can also 
send a request to the monitoring endpoint to get more detailed status information
```
$ curl http://<host_name>:8501/monitoring/prometheus/metrics
```

Once you've confirmed that the server is running, you have a choice of two endpoints to use: [gRPC](https://grpc.io/) or 
[REST](https://restfulapi.net/). There is an extensive literature explaining and comparing the two API 
specs, but I won't get into that here. I will say that I use the gRPC endpoint almost exclusively, primarily 
due to the performance improvements: the network packets are much smaller, and server side processing is much faster. 
You can refer [here](https://cloud.google.com/blog/products/api-management/understanding-grpc-openapi-and-rest-and-when-to-use-them) 
and [here](https://medium.com/@avidaneran/tensorflow-serving-rest-vs-grpc-e8cef9d4ff62) for two 
investigations of the performance differences.

I have included two complete and general functions in [```serving_predictions.py```](/code/tf/serving_prediction.py) that 
can be used to send requests to any model with any input structure & data type requirements. I use this 
function verbatim in the vast majority of my projects. The request structure is slightly more complex 
than that required of the REST endpoint, though worth it 1000x over for the performance increase.

One thing that is very importaat to my deployment flow is model signatures. The whats and hows of these
were outlined in the section on SavedModels [above](#2-creating-a-savedmodel-servable), but it's 
important to note that the function I use to send prediction requests requires 1) these model 
signatures at prediction time, and 2) the data to be formatted in such a way that it corresponds 
to the model signature. Each time a model is uploaded to the server, I save its signatures to a 
database, before using these to determine the input/output structure every time I want to interact 
with that model in the future. 

Here's an example demonstrating how we might send a sequence of images to version 3 of an 'efficient_net' 
model
```python
import grpc
import numpy as np

from tensorflow import make_tensor_proto
from tensorflow_serving.apis.predict_pb2 import PredictRequest
from tensorflow_serving.apis.prediction_service_pb2_grpc import PredictionServiceStub

# inputs & variables
images_to_predict = []  # images / data to get predictions for
model_signatures = None  # load from file
model_name, model_version, signature_name = 'efficient_net', 3, 'serving_default'
model_spec_inputs = model_signatures[signature_name]["input"]

# convert list of input dictionaries => dictionary of batched inputs
grpc_inputs = {k: [] for k in model_spec_inputs.keys()}
for model_input in images_to_predict:
    for k in model_spec_inputs.keys():
        grpc_inputs[k].append(model_input[k])

# create grpc request
grpc_request = PredictRequest()
grpc_request.model_spec.name = model_name
grpc_request.model_spec.version.value = int(model_version)
grpc_request.model_spec.signature_name = 'serving_default'
for k, v in model_spec_inputs.items():
    tf_input = np.array(grpc_inputs[k])
    tensor_proto = make_tensor_proto(tf_input, shape=tf_input.shape)
    grpc_request.inputs[k].CopyFrom(tensor_proto)
 
# send request
channel = grpc.insecure_channel('localhost:8500')
stub = PredictionServiceStub(channel)
output_dict = stub.Predict(grpc_request).outputs
``` 

### 6. Docker-Compose

The snippet below demonstrates how to format the ```docker-compose.yml``` file to run 
the same server as in section [4](#4-running-the-server) using [docker-compose](https://docs.docker.com/compose/)
```yaml
version: '3'

services:
  tf:
    command:
      - "--model_config_file=s3://bucket_name/configs/models.config"
      - "--monitoring_config_file=s3://bucket_name/configs/monitoring.config"
      - "--enable_batching"
      - "--batching_parameters_file=s3://bucket_name/configs/monitoring.config"
      - "--model_config_file_poll_wait_seconds=216000"
    env_file:
      - env.list
    image: tensorflow-serving-optimized
    logging:
      options:
        max-size: 10m
    ports:
      - 8500:8500
      - 8501:8501
    restart: unless-stopped
```

Assuming the tensorflow-serving-optimized image is present on the machine we are running the model server 
from (more on deployment can be found in [deployment.md](/tutorials/deployment.md)), we can then run the 
server with the following command:
```
$ docker-compose --env-file .env -f docker-compose.yml up -d
```

Some points on the ```docker-compose.yml file```:
*  ```env_file``` tells docker-compose where it can find the _names_ of the environment variables it needs 
to read (those variable values themselves still have to be passed to docker-compose, but that happens 
when we run the command to spin up our services). ```env.list``` in this case looks like this
    ```
    AWS_REGION
    AWS_ENDPOINT
    AWS_SECRET_ACCESS_KEY
    AWS_ACCESS_KEY_ID
    AWS_LOG_LEVEL
    TF_CPP_MIN_LOG_LEVEL
    ```
   , a simple text file listing the names of the required variables
* ```logging``` allows us to specify config options for how docker-compose stores its container's logs; in 
this case I am specifying that the rolling log file should hold no more than 10MB of logs. I tend to 
include a variation of this in every ```docker-compose.yml``` I write to avoid issues like [this](https://serverfault.com/questions/637996/clearing-deleting-docker-logs),
excessive logging causing out of storage errors on the host machine. For more information on logging 
customization you can check out the docs [here](https://docs.docker.com/config/containers/logging/configure/).

And finally, the command used to run our service is standard, except _here_ is where we need to pass ```docker-compose```
the actual values of our environment variables (which I choose to do using an env file, though it can be done 
in [many ways](https://docs.docker.com/compose/environment-variables/)).

---



https://blog.tensorflow.org/2021/03/a-tour-of-savedmodel-signatures.html


## Links
- https://www.tensorflow.org/tfx/guide/serving
- https://www.tensorflow.org/tfx/serving/docker
- https://www.tensorflow.org/tfx/serving/setup
- https://www.tensorflow.org/tfx/serving/serving_config
- https://www.tensorflow.org/guide/saved_model
- https://github.com/tensorflow/tensorflow/issues/7530
- https://github.com/tensorflow/examples/blob/master/community/en/docs/deploy/s3.md
- https://mux.com/blog/tuning-performance-of-tensorflow-serving-pipeline/
- https://docs.docker.com/compose/
