# -*- mode: ruby -*-
# vi: set ft=ruby :

$provision_script = <<SCRIPT
echo Provisioning...
date > /etc/vagrant_provisioned_at
SCRIPT

$upgrade_script = <<SCRIPT
apt-get update
apt-get -y upgrade
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: $provision_script
end

Vagrant::Config.run do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.host_name = "ubuntu" 
  config.vm.provision "shell", inline: $upgrade_script

  config.vm.share_folder "karma", "/mnt/karma", ".", :create => true

  # Neo4j set-up & port forwarding
  config.vm.provision :shell, :path => ".vagrant_config/neo4j_setup.sh"
  # config.vm.network :forwarded_port, guest: 7474, host: 7474
  config.vm.forward_port 7474, 17474

  # PostgreSQL set-up & port forwarding
  # config.vm.provision :shell, :path => ".vagrant_config/pg_setup.sh"
  # config.vm.forward_port 5432, 15432

  # Python 2/3 development set-up
  config.vm.provision :shell, :path => ".vagrant_config/py_setup.sh"
  # Flask port forwarding
  config.vm.forward_port 8000, 18000

end
