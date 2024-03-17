#!/bin/bash

# Ersetze "your_dns_provider" durch den Namen deines DNS-Anbieters
# Ersetze "your_domain.com" durch deine tatsächliche Domain

# Ändere den DNS-Eintrag für die Hauptdomain
echo "Ändere den DNS-Eintrag für die Hauptdomain"
your_dns_provider_command maindomain your_domain.com A <server_ip_address>

# Ändere den DNS-Eintrag für die Subdomain www
echo "Ändere den DNS-Eintrag für die Subdomain www"
your_dns_provider_command subdomain www.your_domain.com CNAME your_domain.com

echo "DNS-Einstellungen für movielegends.com wurden aktualisiert."
