# Setting up the Environment on Google Cloud (Cloud VM + SSH access)

1. Generate SSH keys

   - https://cloud.google.com/compute/docs/connect/create-ssh-keys

     ```bash
     mkdir .ssh
     cd .ssh/
     
     ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME
     ```

2. Upload public key to GCP

   - Metadata > SSH keys

     ```bash
     cat gpc.pub
     ```

3. Create VM

   - VM instances > Create Instance

     1. Name

     2. region

     3. zone

     4. Series

     5. Machine type

     6. Change Book disk (optional)

        OS -> Ubuntu -> 20.04 LTS 

        Size -> 30 GB
     
     7. Create (enable API when prompted)

4. SSH into VM

   ```bash
   cd ~
   ssh -u ~/.ssh/PRIVATE_KEY USERNAME@EXTERNAL_IP
   YES
   htop # machine check 
   gcloud --version
   ```

5. Install Anaconda

   1. copy linux download link from anaconda website

   2. ```bash
      wget URL
      bash Ana....sh
      enter
      ```

6. Config VM and setup local

   ```bash
   cd .ssh/
   touch config
   code config .
   ```

   ```config
   Host host_name
   	HostName EXTERNAL_IP
   	User USERNAME
   	IdentityFile  ~/.ssh/PRIVATE_KEY
   ```

   ```bash
   ssh host_name # login
   logout # to logout
   
   cd ~
   source .bashrc # base
   
   git clone de-zoomcamp
   
   # install docker
   sudo apt-get update
   sudo apt-get install docker.io
   Y
   ```

   ```bash
   # docker wihout sudo
   sudo groupadd docker
   sudo gpasswd -a $USER docker
   # logout and log back
   sudo service docker restart
   docker run hello-world
   docker run -it ubuntu bash
   ```

   ```
   exit
   mkdir bin
   cd bin
   
   # install docker compose
   # https://github.com/docker/compose -> release -> docker-compose-linux-x86_64 URL
   
   wget URL -O docker-compose
   chmod +x docker-compose
   
   cd ~
   nano .bashrc
   ```

   ```tex
   # add in the end of file
   export PATH="${HOME}/bin:${PATH}"
   ```

   ```bash
   source .bashrc # login
   which docker-compose
   docker-compose version
   
   # download docker compose from yaml file
   cd directory to yaml file 
   docker-compose up -d
   docker ps
   ```

   ```bash
   pip install pgcli
   pgcli -h localhost -U root -d ny_taxi
   
   pip uninstall pgcli
   conda install -c conda-forge pgcli
   y
   pgcli -h localhost -U root -d ny_taxi
   ```

   

7. SSH with VS code

   1. Install Remote - SSH extension
   2. Open remote window -> Connect to host -> Host (Config file)
   3. Open de-zoomcamp directory

8. Forwarding Ports

   1. VS code -> Ports -> Forward a Port -> input 5432

   2. VS code -> Ports -> Forward a Port -> input 8080

   3. go to localhost:8080 -> login pgadmin

9. Run Jupyter Notebook

   ```bash
   cd de-zoomcamp/week1/2_docker_sql
   jupter notebook
   ```

   1. VS code -> Ports -> Forward a Port -> input 8888

   2. copy URL-> go to localhost:8888 URL

   3. Run upload-data.ipynb

   4. ```bash
      pgcli -h localhost -U root -d ny_taxi
      ```

   5. test query

10. Install Terraform

    1. Go to terraform download website -> Linux Binary Download -> copy Amd64 link

    2. ```bash
       cd ~
       cd bin/
       wget tf_download_URL
       sudo apt-get install unzip
       unzip tf_file.zip
       rm zip file
       cd ~
       terraform -version
       ```

11. sftp google credentials to VM

    ```bash
    # source machine of json file
    sftp de-zoomcamp
    mkdir .gc
    cd .gc
    put ny-rides.json
    ```

    ```bash
    # vm
    cd de-zoomcamp/week1/tf_gcp/terraform
    export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/ny-rides.json
    gcloud auth activate-service-account --key-file $GOOGLE_APPICATION_CREDENTIALS
    terraform init
    terraform plan
    	ny-rides-alexey
    terraform apply
    ```

12. Shutdown VM

    ```bash
    sudo shutdown down
    ```

    or

    1. GCP -> VM instances -> select instance -> 3 dots -> Stop

13. Resume

    1. GCP -> VM instances -> select instance -> 3 dots -> Start/Resume

    2. Copy new EXTERNAL IP

    3. ```
       nano .ssh/config
       # replace hostname
       
       ssh HOST # login
       ```

       