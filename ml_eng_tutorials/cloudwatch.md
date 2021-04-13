# Cloudwatch Agent Setup

As a default monitoring solution for any project, I tend to just organise a very simple Cloudwatch Dashboard. But for 
ML projects in particular, the default metrics don't quite cut it. Setting up a Cloudwatch Agent is easy though, and 
provides both more fine-grained system metrics, and the ability to completely customize application metrics.

The purpose of this document is not to suggest when one should(n't) use the Cloudwatch Agent, but here a few key cases 
where it is useful: 
* You want to monitor any of [these](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/metrics-collected-by-CloudWatch-agent.html) metrics
* You want to collect Cloudwatch metrics from in-house (non-EC2) servers
* You want to log custom application metrics (& view these alongside system Cloudwatch metrics).  

## 7' Version (for Ubuntu EC2 instance)

1. create IAM role for CloudWatchAgent ([help](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-iam-roles-for-cloudwatch-agent-commandline.html))
2. attach IAM role to EC2 instance ([help](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/iam-roles-for-amazon-ec2.html#attach-iam-role))
3. ```$ wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb```
4. ```$ sudo dpkg -i -E ./amazon-cloudwatch-agent.deb```
5. ```$ sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard``` to interactively created the 
agent's config file
6. ```$ sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json```
7. ```$ sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status``` to check agent status 

## LP Version (ein Spaziergang)

1. First things first we need to create an [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html). 
This is required to grant the cloudwatch agent (a background service running on your EC2 instance) to read information 
from said instance and save it to Cloudwatch.
    * The instructions [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-iam-roles-for-cloudwatch-agent-commandline.html) 
    are pretty comprehensive. The only thing missing is that you'll have to make one extra click, to select that you 
    don't want to assign any tags to your Role, though this will be obvious when you get there.
    * Once you've created this Role once, you can use it for _every_ EC2 instance for which you want to use the 
    Cloudwatch Agent in the future
2. Next we need to attach the recently created role to the EC2 instance on which we want to run the agent
    * The instructions [here](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/iam-roles-for-amazon-ec2.html#attach-iam-role) 
    outline how to attach an IAM role to an existing EC2 instance
    * if you need >1 role on your instance, things get a little more complicated. You'll need to create two 
    [access policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) and 
    [attach](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) them to a single 
    IAM role (e.g. in this circumstance, the Cloudwatch access control would be handled by an access policy, not the role 
    itself)
3. Download the Cloudwatch Agent using the command-line
    * To download the installation file run ```$ wget <download_link>```, where the <download_link> depends on which 
    platform & system architecture you are using. The complete list of download links can be found 
    [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/download-cloudwatch-agent-commandline.html).
    * If you want, you can verify the signature of the downloaded file by following the instructions 
    [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/verify-CloudWatch-Agent-Package-Signature.html).
4. Package installation
    *  the command needed to install the package depends on whether you downloaded a ```.rpm``` or ```.deb``` file; the 
    two commands are ```$ sudo rpm -U ./amazon-cloudwatch-agent.rpm``` and ```$ sudo dpkg -i -E ./amazon-cloudwatch-agent.deb``` 
    respectively.
5. Config creation & configuration (yes that's right, _you_ have to configure the config)
    * You can either create the config using an interactive wizard or manually, though if you're (like me) depending on this guide, 
    I'd suggest using the [wizard](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-cloudwatch-agent-configuration-file-wizard.html).
    * Some of the prompts were not immediately self-explanatory to me, so I'll enumerate them with some tips here:
        * ```On which OS are you planning to use the agent?``` - :cake:
        * ```Are you using EC2 or On-Premises hosts``` - :cake:
        * ```Which user are you planning to run the agent?``` - default is root, though if you want to select another user 
        to run the agent with you can follow the instructions [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-common-scenarios.html#CloudWatch-Agent-run-as-user) 
        to do so.
        * ```Do you want to turn on StatsD daemon?``` - required if you want to use [StatsD](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-custom-metrics-statsd.html) 
        to collect custom application metrics (i.e. metrics from within your application itself, not the system/OS outside it).
        * ```Do you want to monitor metrics from CollectD``` - the same as the previous point, but required if you want 
        to use [CollectD](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-custom-metrics-collectd.html) 
        for the same purpose.
            * NB: if you want to use CollectD, you'll need to install it before the agent can start correctly
        * ```Do you want to monitor any host metrics? e.g. CPU, memory, etc.``` - almost certainly yes, unless you only 
        want application metrics
        * ```Do you want to monitor CPU metrics per core?``` - do you want fine-grained metrics for each core on the 
        machine, than only aggregated metrics for the entire machine (if so, there are [additional costs](https://aws.amazon.com/cloudwatch/pricing/)). 
        The complete list of CPU metrics (that you can get either overally or per-core) is available [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/metrics-collected-by-CloudWatch-agent.html)
        * ```Do you want to add ec2 dimensions (ImageId, InstanceId...) into all of your metrics... ?``` - to make it 
        easier to tie Cloudwatch metrics to your instances
        * ```Would you like to collect your metrics at high-resolution (sub-minute resolution)?``` - you can set the 
        resolution to be 1s, 10s, 30s, or 60s, though using the wizard this will apply equally to all metrics. If you 
        want a more fine-grained setting of metric collection resolution, you can modify the config file manually (discussed below)
        * ```Which default metrics config do you want?``` - choose from one of the default configs, available 
        [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-cloudwatch-agent-configuration-file-wizard.html)
            * If you don't want one of these, you can select ```None```, and you will then be prompted in turn whether 
            or not you want to monitor each of the possible metrics
    * And you made it! You'll then be prompted to review the config, and finally whether you have any existing log files 
    that you'd like to be monitored by the Cloudwatch Agent, and then you're done.
    * Your config file is saved by default here ```/opt/aws/amazon-cloudwatch-agent/bin/config.json```. Once you've run 
    the wizard once, you can copy this file to any other machine to expedite the setup process.
    * If you want to customize the config file in more detail, you can edit it like any other JSON file. Explanations 
    of all possible modifications are documented [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html).
6. Run it! 
    * On Linux, you can run the agent using ```$ sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:<configuration-file-path>```, 
    where ```<configuration-file-path>``` is the path to the config file you just created.
7. To check the agent's status
    * ```$ sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status```
    * as long as the dictionary printed in response has ```"status": "running"```, you are good to go!
    
:partying_face:	:partying_face:	
