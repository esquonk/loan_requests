# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/srv/loan_requests/project", create: true

  config.vm.network "forwarded_port", guest: 80, host: 8080

  config.vm.provision :shell, path: "deploy/scripts/bootstrap_ubuntu.sh"

end
