FROM centos:7

#install 



RUN mkdir -p /usr/src/iacode 
WORKDIR /usr/src/iacode 







RUN yum install -y wget unzip

ENV TER_VER="0.12.17"
RUN wget --directory-prefix=/usr/src/terraform  https://releases.hashicorp.com/terraform/${TER_VER}/terraform_${TER_VER}_linux_amd64.zip
RUN unzip /usr/src/terraform/terraform_${TER_VER}_linux_amd64.zip -d /usr/local/bin/
RUN terraform -v












#install requrements
#RUN yum install   -y  https://rhel7.iuscommunity.org/ius-release.rpm
#RUN yum install   -y  https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum update 
<<<<<<< HEAD
RUN yum install epel-release openssl -y
=======
RUN yum install epel-release -y
>>>>>>> 83264dcac7cd7a05f010bbcfc5dce7ee01240c84

RUN yum install   -y python3-pip
RUN pip3 install  --upgrade pip
#RUN pip3 install --upgrade setuptools
RUN pip3 install  --user paramiko
RUN pip3 install  --user python-jenkins
RUN pip3 install  pyqt5==5.14.0

RUN yum install   -y  fontconfig-devel.x86_64 \
                      libXrender.x86_64 \
                      libxkbcommon-x11-devel.x86_64 \
                      xorg-x11-xauth \
                      mesa-libGL-devel

#install aws_cli
RUN pip3 install awscli
RUN pip3 install --user --upgrade awscli
RUN aws --version
COPY aws_config/. /root/.aws/



#install kubectl

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl
RUN kubectl version --client



#install helm

RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
RUN chmod 700 get_helm.sh
RUN ./get_helm.sh


#install ssh 

RUN yum -y install  git openssh-server  openssh-clients
RUN mkdir -p /root/.ssh/
RUN rm /etc/ssh/sshd_config
COPY sshd_config /etc/ssh/
RUN chown root:root /etc/ssh/sshd_config
RUN chmod -R 600 /etc/ssh/sshd_config


#helpers to check libreries dependensis 
#ldd /usr/local/lib64/python3.6/site-packages/PyQt5/Qt/plugins/platforms/libqxcb.so
#ldd /usr/local/lib64/python3.6/site-packages/PyQt5/Qt/plugins/xcbglintegrations/libqxcb-glx-integration.so
#export QT_DEBUG_PLUGINS=1


RUN echo 'root:strongpass' | chpasswd




ENTRYPOINT ["/usr/sbin/init"]
VOLUME [ "/sys/fs/cgroup" ]
