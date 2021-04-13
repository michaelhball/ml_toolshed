# ML Tidbits

This is just a project to compile a bunch of useful ML snippets. The project is not intended to be 
'run', and the various pieces don't necessarily go together. They are reusable pieces of code that 
I find myself needing over and over again. 

I don't claim that these snippets represent my unique insight and ability. They are a product of my 
having read countless blogs/forums/implementations and customized things as needed for my own projects 
(hence my best efforts to attribute inspiration where relevant). This repository is first and foremost 
a tool-shed for myself, but one in which I hope you'll find something useful.

This README acts as a table of contents and index, organising & linking to the various files/documents 
that are themselves not well organised.

## AWS

The AWS notes are mostly snippets or step-by-step instructions for how to repeat the setup of 
something. The topics are:
* [increase ec2 storage](/ml_eng_tutorials/increase_ec2_storage.md)
* [ec2 instance setup](/ml_eng_tutorials/ec2_setup.md)
* [cloudwatch for ec2 setup](/ml_eng_tutorials/cloudwatch.md)

## Tensorflow

Almost all Tensorflow snippets I have here are provided inside the [```tf```](/ml_tidbits/tf) directory. The files I 
have are as follows:
* [```callbacks.py```](ml_tidbits/tf/callbacks.py) contains a collection of training callbacks for use 
with ```.fit``` function
    * [RestoreBestModel](https://github.com/michaelhball/ml_tidbits/blob/0450bc2d9830a1846cdaddf992ca4d74c3c62604/ml_tidbits/tf/callbacks.py#L4-L26)
    *  
* [```models.py```](/ml_tidbits/tf/models.py) contains a collection of utils for model 
loading/modifying/customizing/converting etc.

## MLFlow

## Docker(-Compose)

* [SSL w. certbot, nginx, & docker-compose](/ml_eng_tutorials/certbot.md)

## Jupyter / Colab

## Misc.

And lastly, here's a bunch of useful snippets that don't fit anywhere else
* [programmatic GPU config & customization](ml_tidbits/gpu.py) for tensorflow, pytorch, etc.
* [programmatic ssh](https://github.com/michaelhball/ml_tidbits/blob/9f730e23efc31a649af0371429a7f963b01360a1/ml_tidbits/utils.py#L5-L21), 
i.e. creating client connection in Python code
* [programmatic scp](https://github.com/michaelhball/ml_tidbits/blob/9f730e23efc31a649af0371429a7f963b01360a1/ml_tidbits/utils.py#L24-L49), 
i.e. using the above ssh function to copy files from/to some remote machine


### wantlist

### push notification
