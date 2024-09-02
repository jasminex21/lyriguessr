## AWS Deployment Guide

1. Go to [AWS Console](https://us-east-1.console.aws.amazon.com/console/home?region=us-east-1) and then to EC2
2. Click "Launch Instance"

    i. Name the app

    ii. Select Amazon Linux

    iii. Select a free tier eligible AMI
    
    iv. Use tayLyrics key pair

    v. Select "Select existing security group" and choose "streamlit"

    vi. Launch instance

3. Connect to the instance via SSH

    i. Open terminal and navigate to directory with .pem file

    ii. Run `chmod 400 "tayLyrics.pem"`

    iii. Connect to your instance using its Public DNS (e.g. `ssh -i "tayLyrics.pem" ec2-user@ec2-100-28-99-46.compute-1.amazonaws.com` - change the public DNS)

4. Booting

    i. `sudo su`
    
    ii. `yum update` to update all packages

    iii. `yum install git`

    iv. `git clone <repo_url>`

    v. `yum install python3-pip`

    vi. Navigate to the directory (e.g. `cd tayLyrics`)

    vii. *For each requirement*, run `python3 -m pip install --ignore-installed <req_name>`

    viii. `python3 -m streamlit run <app_name.py>`, and then go to the external URL and check that the app works

    ix. `nohup python3 -m streamlit run <app_name.py>` to enable permanent running

5. Create a new target group

    i. Go to EC2 > Target Groups > Create target group

    ii. Simply add the name of the target group (keep it the same as the instance name, e.g. tayLyrics or radiohead), and keep all the defaults 

    iii. Select the corresponding instance

    iv. Change "Ports for the selected instances" to be 8501 (it is 80 by default), and Include as pending below, then Register pending targets

6. Modify load balancer settings

    i. Go to EC2 > Load Balancers > tayLyrics

    ii. For both HTTP and HTTPS, select them and then Add rule > Add condition (if Host Header is <instance_name>.lyriguessr.xyz) > Forward to correpsonding target group

7. Deploy to custom domain

    i. Go to Route 53 > Hosted zones > lyriguessr.xyz

    ii. Create record > Set Record name to the instance name > Select CNAME > Set the value to "tayLyrics-922305429.us-east-1.elb.amazonaws.com." - this is the public DNS of the load balancer > Create records

    iii. Check the link https://<instance_name>.lyriguessr.xyz - if it works we are all set! Else, it could be that DNS propagation is taking awhile, so use [WhatsMyDNS](https://www.whatsmydns.net/) to keep track of the DNS propagation