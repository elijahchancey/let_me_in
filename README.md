## Let_me_in 
Let_me_in is a python utility that will add an ingress rule to a vpc security group using your IP address. Here's how to use it:

```
$ ./let_me_in.py bastion 22
This Inbound Security Rule is about to be added:
Security Group Name: bastion
Security Group Id:   sg-1234567
My IP Address:       42.42.42.42/32
Port:                TCP/22
Rule Description:    2018-02-22.elijahchancey.MacBook-ProE
Type 'yes' to continue: yes
Rule Added.
```
Please let me know if you think this tool should be improved.
