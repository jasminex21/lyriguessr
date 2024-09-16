## Setting up SSH in each AWS EC2 instance

1. `ssh-keygen -t ed25519 -C "jasminexu7003@icloud.com"`

2. 
    * `eval "$(ssh-agent -s)"`
    * `ssh-add ~/.ssh/id_ed25519`
3. Copy key to clipboard via `cat ~/.ssh/id_ed25519.pub`
4. Add the SSH key to GitHub
5. Change the remote URL to use SSH via `git remote set-url origin git@github.com:jasminex21/lyriguessr.git`
