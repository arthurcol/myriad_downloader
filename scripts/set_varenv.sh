
echo "Enter your KITT token"
read token
echo '# LeWagon Kitt token to download Myriad challenges' >> ~/.zshrc
echo "export KITT_TOKEN=$token" >> ~/.zshrc


echo '# GitHub Username' >> ~/.zshrc
echo "export GH_USERNAME=$(gh api 'https://api.github.com/user'|jq .login)" >> ~/.zshrc


echo "Enter the batch number to use by default"
read batch
echo '# LeWagon batch number to use to download Myriad challenges' >> ~/.zshrc
echo "export DEFAULT_BATCH=$batch" >> ~/.zshrc
