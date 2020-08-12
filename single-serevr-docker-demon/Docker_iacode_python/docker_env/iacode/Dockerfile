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
RUN yum install   -y  https://rhel7.iuscommunity.org/ius-release.rpm
RUN yum install   -y python36u-pip
RUN pip3 install  --upgrade pip
#RUN pip3 install --upgrade setuptools
RUN pip3 install  --user paramiko
RUN pip3 install  --user python-jenkins
RUN pip3 install  PyQt5

RUN yum install   -y  fontconfig-devel.x86_64 \
                      libXrender.x86_64 \
                      libxkbcommon-x11-devel.x86_64 \
                      xorg-x11-xauth \
                      mesa-libGL-devel







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
