# Increase EC2 Storage

Created EC2 instances default to 8GB of storage. It's possible to configure this to a 
larger size at the time of instance creation, but I often find myself needing to adjust the storage of an 
already-running instance. It's painless, I can just never remember the sequence of commands.

## 7' Version

1. Resize EC2 storage in AWS console (EC2 &#8594; EBS &#8594; ```Modify Volume```)
2. ```$ sudo growpart /dev/xvda1 1```
3. ```$ sudo sudo resize2fs /dev/xvda1```

## LP Version

NB: the name of your drive/partition might be different to ```/dev/xvda``` depending on your instance type
(e.g. for one my accelerated computing machines the relevant drive is ```/dev/nvme0n1```). In any case, 
the following sequence of steps is identical. 

1. Resize EC2 instance's EBS Volume
    * Go to your EC2 dashboard and select the instance whose storage you want to change 
    * Click on ```Storage``` and then select the ```Volume ID``` of the Volume you want to change
    * While the appropriate row Volume row is selected, click on the ```Actions``` dropdown and select
    ```Modify Volume```
    * Change the storage size & apply the changes
2. Resize the OS partition of your instance
    * Run ```$ df -h``` to show the current size of the partition (should see that ```/dev/root``` or ```/dev/xvda``` 
    partition is still only 8GB).
    * Run ```$ lsblk``` to see the EBS volume specifics. Here we should see that ```/dev/xvda``` has the new 
    size set in the AWS console, but that it's child partition ```/dev/xvda1``` (you root drive) only has 8GB.
    * Run ```$ sudo growpart /dev/xvda 1``` to resize the partition to fill its parent
    * Rerun ```$ lsblk``` to make sure your partition is now the intended size.
3. Resize the filesystem
    * If you run ```$ df -h``` again, you'll see that despite sizing the partitions correctly, the 
    filesystem is still showing 8GB. You need to resize this to fill the newly modified partition.
    * Run ```$ sudo resize2fs /dev/xvda1```, and recheck to ```$ df -h``` to make sure you changes 
    were applied.   

Voilà! :cake: