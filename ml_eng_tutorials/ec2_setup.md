# EC2 Setup

Terraform and similar IAC services are one of the most enjoyable recent innovations in the world of 
software engineering, but there are still times when this is overkill. I often want to quickly spin up 
an EC2 instance, clone a repo or pull a docker image, and run a service. I find myself endlessly 
repeating the same steps, and endlessly heading to project download pages to remind 
myself how to install a particular tool. So from now on, I dump it all here. 

*  first things first, to even SSH to a new EC2 instance, the ```.pem``` file permissions need to be changed: 
```$ chmod 400 <path_to_permission_file>.pem```

* install docker (& allow running without sudo)
    * ```$ curl -fsSL https://get.docker.com -o get-docker.sh```
    * ```$ sudo sh get-docker.sh```
    * ```$ sudo usermod -a -G docker <ec2_username>```

* install docker-compose (& allow running without sudo)
    * to install the latest version (provided you have [jq](https://stedolan.github.io/jq/download/) installed):
        * ```$ VERSION=$(curl --silent https://api.github.com/repos/docker/compose/releases/latest | jq .name -r)```
        * ```$ sudo curl -L "https://github.com/docker/compose/releases/download/${VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose```
    * to install a specific version, e.g. ```1.27.4```
        * ```$ sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose```
    * ```$ sudo chmod +x /usr/local/bin/docker-compose```  to apply executable permissions to the binary
    * ```$ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose``` so we don't need sudo

* Remember to set appropriate http(s) inbound & outbound rules in the AWS EC2 console! Easy to forget and frustrating to 
debug...

* If using a server that requires an SSL certificate, follow the instructions in [certbot.md](/ml_eng_tutorials/certbot.md)

* If you want to set up CloudWatch monitoring (e.g. beyond the defaults), follow the instructions in 
[cloudwatch.md](/ml_eng_tutorials/cloudwatch.md)
