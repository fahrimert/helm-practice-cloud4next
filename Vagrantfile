Vagrant.configure("2") do |config|
  
  config.vm.box = "ubuntu/jammy64"
  config.vm.network "private_network", ip: "192.168.56.30"
  
  config.vm.hostname = "mert-k3slab-server"


config.vm.provision "shell", inline: <<-SHELL
    echo "Sistem yapılandırılıyor..."
    
    chattr -i /etc/resolv.conf || true
    
    rm -f /etc/resolv.conf
    echo "nameserver 8.8.8.8" > /etc/resolv.conf
    echo "nameserver 1.1.1.1" >> /etc/resolv.conf
    
    chattr +i /etc/resolv.conf
    
    IFACE=$(ip -o link show | awk -F': ' '{print $2}' | grep -v "lo" | head -n 1)
    
    echo "Tespit edilen Ag Karti: $IFACE"
    
    ip route del default || true
    
    ip route add default via 10.0.2.2 dev $IFACE
  SHELL
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "8192"   
    vb.cpus = 4         
    vb.name = "mert-k3slab-helm-practice-server"
    
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

end
