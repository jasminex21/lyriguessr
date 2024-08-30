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

5. Deploy to custom domain

    i. I already have a hosted zone in Route 53 (lyriguessr.xyz)

    ii. Click "Create record"

    iii. Enter the name of the app, e.g. "tayLyrics"

    iv. Select record type A

    v. Add the instance's public DNS (without the port, e.g. 100.28.99.46) as the value

6. Set up load balancer to direct HTTPS traffic

    i. From the console, go to Target Groups > Create Target Group

    ii. Change the port to 8501 (default is 80)

    iii. Click Next, then select the correct instance as a target, and Create Target Group

    iv. Go to EC2 > Load Balancers > tayLyrics

    v. Add a rule to both HTTPS:443 and HTTP:80 - choose condition "Host Header" and set the host header to "<app_name>.lyriguessr.xyz"

    vi. Log in to Namecheap and go to Advanced DNS - create a new CNAME record with "<app_name>" as the host, and "tayLyrics-922305429.us-east-1.elb.amazonaws.com." as the value

    vii. Use [WhatsMyDNS](https://www.whatsmydns.net/) to keep track of the DNS propagation