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
document of all code snippets, tutorials, step-by-step processes, and config files I recurringly 
find useful. It's also the way I keep my cool. 

## Overview

The project is not intended to be 'run', nor do the various files fit together or 
function as a cohesive project. Everything just contains useful pieces of code or insight 
that I find myself using again and again. 

I don't claim that anything in this repository represents my own insight and ability. Everything is 
merely a product of my having read countless blogs/forums/implementations, customized things as 
needed for myself, and decided that no one place captured the note I wanted to have next time 
I returned to repeat a particular task. This repository is first and foremost a tool-shed for myself, 
but it's one I keep clean in the hopes that you'll find ssomething useful here too.

The files in this project are not well organized, so this README should be used as index and 
access point from which to access all files. The sections below are ordered alphabetically.

## The Featured Tools

* [Tensorflow Serving](/tutorials/tf_serving.md) (& how to use it for _real_ production settings, not 
Medium-article production).
* 

## The Full Shed

### AWS

The following notes are my attempt to write practical high-signal documentation for processes 
that usually require me to click through >5 pages of AWS docs. There are 7' (short) and LP (long) 
versions of each note as well as references to various pages of official documentation for 
further reading. 

* How to [increase EC2 storage](/tutorials/increase_ec2_storage.md)
* How to [setup an EC2 instance](/tutorials/ec2_setup.md)
* How to setup the [Cloudwatch Agent for EC2](/tutorials/cloudwatch.md)

## CI / CD / IAC

* Deploy to EC2 w. Gitlab CI (incl. Gitlab Container Registry, docker-compose)

## Docker(-Compose)

* [SSL w. certbot, nginx, & docker-compose](/tutorials/certbot.md)

## Jupyter / Google Colab

*  

## Misc.

Some more engineeringy snippets that don't fit elsewhere

* [programmatic GPU config & customization](code/gpu.py) for tensorflow & pytorch.
* [programmatic ssh](https://github.com/michaelhball/ml_tidbits/blob/9f730e23efc31a649af0371429a7f963b01360a1/ml_tidbits/utils.py#L5-L21), 
i.e. creating client connection in Python code
* [programmatic scp](https://github.com/michaelhball/ml_tidbits/blob/9f730e23efc31a649af0371429a7f963b01360a1/ml_tidbits/utils.py#L24-L49), 
i.e. using the above ssh function to copy files from/to some remote machine

## MLFlow

* 

<img align="left" height="50" src="https://github.com/michaelhball/ml_toolshed/blob/main/img/tf.png">

## Tensorflow

Almost all Tensorflow snippets I have here are provided inside the [```tf```](/code/tf) directory. The files I 
have are as follows:

* Tutorials
    * [Tensorflow Serving](/tutorials/tf_serving.md)
    * [Tensorflow Model Formats](/tutorials/tf_model_formats.md) (COMING SOON)
* Code (most of which is referenced by the tutorials)
    * [```callbacks.py```](code/tf/callbacks.py) contains a collection of training callbacks for use 
    with ```.fit``` function
        * [RestoreBestModel](https://github.com/michaelhball/ml_tidbits/blob/0450bc2d9830a1846cdaddf992ca4d74c3c62604/ml_tidbits/tf/callbacks.py#L4-L26)  
    * [```models.py```](/code/tf/models.py) contains a collection of utils for model 
    loading/modifying/customizing/converting etc.
    * [```serving_models.py```](/code/tf/serving_models.py)
    * [```serving_predictions.py```](/code/tf/serving_predictions.py) contains code for getting predictions 
    from a tensorflow serving ModelServer
        * [```format_grpc_request```](https://github.com/michaelhball/ml_toolshed/blob/8848e9f3d48f732158d243c9a065695ed83fc537/code/tf/serving_prediction.py#L9-L41)
        * [```send_prediction_request```](https://github.com/michaelhball/ml_toolshed/blob/8848e9f3d48f732158d243c9a065695ed83fc537/code/tf/serving_prediction.py#L44-L83)
