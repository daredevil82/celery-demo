# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 4369, host: 4369
  config.vm.network "forwarded_port", guest: 15672, host: 15672
  config.vm.network "private_network", ip: "192.168.33.10"

  config.vm.synced_folder ".", "/home/vagrant/project"

  config.vm.provider "virtualbox" do |vb|
    vb.name = 'celery-demo'
    vb.memory = "1536"
    vb.cpus = 2
  end

  config.vm.provision "shell", path: "provision/provision.sh"

end
