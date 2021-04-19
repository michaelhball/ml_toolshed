# ML Toolshed

<p align="center">
    <img alt="hammer icon" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/hammer_apple.png" width="64" hspace="20">
    <img alt="clamp icon" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/clamp_apple.png" width="64" hspace="20">
    <img alt="nut & bolt icon" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/nut_and_bolt_apple.png" width="64" hspace="20">
    <img alt="wrench icon" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/wrench_apple.png" width="64" hspace="20">
    <img alt="microscope icon" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/microscope_apple.png" width="64" hspace="20">
</p>

<h3 align="center">
<p>Track with MLFlow, serve with Tensorflow, deploy with docker-compose, & master AWS
</h3>

This is my personal wiki for machine learning & engineering related topics: a living 
document of all code snippets, tutorials, step-by-step processes, and config files I recurrently 
find useful. It's also how I keep my cool.

--- 

## :owl: Overview

The project is not intended to be 'run', nor do the various files fit together or function as a 
cohesive project. Everything in this repository is either a useful insight, piece of code, 
or config file that I find myself using again and again. The tutorials section is my effort to 
organise these snippets into more cohesive wholes.

I don't claim that anything in this repository represents my own insight and ability. Everything is 
a product of my having read countless blogs/forums/implementations, customized things as 
needed for myself, and there was no one place I would be able to go to get all the information I need 
the next I want to perform a particular task. This repository is first and foremost a toolshed for myself, 
but I try to keep it clean in the hope that you'll find something useful here too. 

This README should be used as the index and entry point into everything the Toolshed has to offer.

---

## :book: Table of Contents

* [Featured](#-featured-tutorials)
* [AWS](#-aws)
* [CI, CD, IAC](#ci,-cd,-iac)
* [Docker & Docker-Compose](#docker-&-docker-compose)
* [Jupyter & Colab](#jupyter-&-colab)
* [MLFlow](#mlflow)
* [Tensorflow](#tensorflow)
* [Utilities](#utilities)

--- 

## Featured Tutorials

* [Tensorflow Serving](/tutorials/tf_serving.md) and how to use it for _real_ production settings.

--- 

<br /><br />
<img align="left" height="50" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/aws.png">

## AWS

The following notes are my attempt to write practical high-signal documentation for processes 
that usually require me to click through >5 pages of AWS docs. There are 7' (short) and LP (long) 
versions of each note as well as references to various pages of official documentation for 
further reading. 

* How to [increase EC2 storage](/tutorials/increase_ec2_storage.md)
* How to [setup an EC2 instance](/tutorials/ec2_setup.md)
* How to setup the [Cloudwatch Agent for EC2](/tutorials/cloudwatch.md)


<br /><br />
<img align="left" height="50" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/gitlab.png">

## CI, CD, IAC

This section contains general tips on deployment and automated infrastructure setup, and some specific 
example walkthroughs of specific, real-life production pipelines.

* EC2 deployment w. Gitlab CI & Docker :building_construction: \[Coming Soon\] :building_construction: 
* Blue-Green Deployment with Terraform & AWS :building_construction: \[Coming Soon\] :building_construction:


<br /><br />
<img align="left" height="50" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/docker.png">

## Docker & Docker-Compose

This section primarily contains the Dockerfiles and docker-compose yaml files used by tutorials in other 
sections of the README, as well as a few Docker-specific tutorials

* SSL w. certbot, nginx, & docker-compose :building_construction: \[Coming Soon\] :building_construction:
* Files
    * [docker-compose.tf.yml](/code/docker/docker-compose.tf.yml) (used by the 
    [Tensorflow Serving](/tutorials/tf_serving.md) tutorial).


<br /><br />
<img align="left" height="50" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/jupyter.png">

## Jupyter & Colab

This contains a bunch of notebook specific functions or functions I use with Colab.

* [images.ipynb](/notebooks/images.ipynb) contains helper functions for displaying & manipulating images
* [stylegan.ipynb](/notebooks/stylegan.ipynb) contains StyleGAN2 helper functions; I mostly use these w. 
Google Colab StyleGAN implementations


<br /><br />
<img align="left" height="50" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/mlflow.png">

## MLFlow

* MLFlow in Production :building_construction: \[Coming Soon\] :building_construction:
* [MyMLFlowClient](/code/mlflow.py) contains the client I use for _all_ programmatic MLFlow interaction


<br /><br />
<img align="left" height="50" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/tf.png">

## Tensorflow

This section contains a number of code snippets & tutorials related to Tensorflow and the 
Tensorflow-in-production ecosystem. All code snippets are available inside the [```tf```](/code/tf) directory, 
though most of these are referenced in at least one tutorial

* Tutorials
    * [Tensorflow Serving](/tutorials/tf_serving.md) (for _real_ production workflows)
    * Tensorflow Model Formats \[Coming Soon\] :building_construction:
* Code (most of which is referenced by the tutorials)
    * [```callbacks.py```](code/tf/callbacks.py) contains a collection of training callbacks for use 
    with ```.fit``` function
        * [RestoreBestModel](https://github.com/michaelhball/ml_tidbits/blob/0450bc2d9830a1846cdaddf992ca4d74c3c62604/ml_tidbits/tf/callbacks.py#L4-L26)  
    * [```models.py```](/code/tf/models.py) contains a collection of utils for model 
    loading/modifying/customizing/converting etc.
    * [```model_formats.py```](/code/tf/model_formats.py)
    * [```serving_predictions.py```](/code/tf/serving_predictions.py) contains code for getting predictions 
    from a tensorflow serving ModelServer
        * [```format_grpc_request```](https://github.com/michaelhball/ml_toolshed/blob/8848e9f3d48f732158d243c9a065695ed83fc537/code/tf/serving_prediction.py#L9-L41)
        * [```send_prediction_request```](https://github.com/michaelhball/ml_toolshed/blob/8848e9f3d48f732158d243c9a065695ed83fc537/code/tf/serving_prediction.py#L44-L83)


<br /><br />
## :toolbox: Utilities

And here are some utility functions that don't fit anywhere else  

* [programmatic GPU config & customization](code/gpu.py) for tensorflow & pytorch.
* [programmatic ssh](https://github.com/michaelhball/ml_tidbits/blob/9f730e23efc31a649af0371429a7f963b01360a1/ml_tidbits/utils.py#L5-L21), 
i.e. creating client connection in Python code
* [programmatic scp](https://github.com/michaelhball/ml_tidbits/blob/9f730e23efc31a649af0371429a7f963b01360a1/ml_tidbits/utils.py#L24-L49), 
i.e. using the above ssh function to copy files from/to some remote machine
