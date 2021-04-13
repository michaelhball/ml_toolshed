# ML Toolshed

<h3 align="center">
<p>Serve with Tensorflow, track with MLFlow, master AWS, & deploy with docker-compose.
</h3>

<h2 align="center">
🔨🪛🗜️⛏️🔩🔧🔬
</h2>

This is my personal wiki for machine learning & engineering related topics: a living 
document of all code snippets, tutorials, step-by-step processes, and config files I recurringly 
find useful. It also helps me keep it cool.

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

## AWS

The following notes are my attempt to write practical high-signal documentation for processes 
that usually require me to click through >5 pages of AWS docs. There are 7' (short) and LP (long) 
versions of each note as well as references to various pages of official documentation for 
further reading. 

* How to [increase EC2 storage](/ml_eng_tutorials/increase_ec2_storage.md)
* How to [setup an EC2 instance](/ml_eng_tutorials/ec2_setup.md)
* How to setup the [Cloudwatch Agent for EC2](/ml_eng_tutorials/cloudwatch.md)

## CI / CD / IAC

* Deploy to EC2 w. Gitlab CI (incl. Gitlab Container Registry, docker-compose)

## Docker(-Compose)

* [SSL w. certbot, nginx, & docker-compose](/ml_eng_tutorials/certbot.md)

## Jupyter / Google Colab

*  

## Misc.

And lastly, here's a bunch of useful snippets that don't fit anywhere else
* [programmatic GPU config & customization](ml_tidbits/gpu.py) for tensorflow, pytorch, etc.
* [programmatic ssh](https://github.com/michaelhball/ml_tidbits/blob/9f730e23efc31a649af0371429a7f963b01360a1/ml_tidbits/utils.py#L5-L21), 
i.e. creating client connection in Python code
* [programmatic scp](https://github.com/michaelhball/ml_tidbits/blob/9f730e23efc31a649af0371429a7f963b01360a1/ml_tidbits/utils.py#L24-L49), 
i.e. using the above ssh function to copy files from/to some remote machine

## MLFlow

* 

## Tensorflow

Almost all Tensorflow snippets I have here are provided inside the [```tf```](/ml_tidbits/tf) directory. The files I 
have are as follows:
* [```callbacks.py```](ml_tidbits/tf/callbacks.py) contains a collection of training callbacks for use 
with ```.fit``` function
    * [RestoreBestModel](https://github.com/michaelhball/ml_tidbits/blob/0450bc2d9830a1846cdaddf992ca4d74c3c62604/ml_tidbits/tf/callbacks.py#L4-L26)
    *  
* [```models.py```](/ml_tidbits/tf/models.py) contains a collection of utils for model 
loading/modifying/customizing/converting etc.
