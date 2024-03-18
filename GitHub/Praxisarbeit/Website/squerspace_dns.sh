#!/bin/bash

# Squarespace DNS-Einstellungen

# Ändere den CNAME-Eintrag für die Hauptdomain
echo "Ändere den CNAME-Eintrag für die Hauptdomain"
squarespace_dns_command movielegends.ch CNAME <squarespace_url>

# Ändere den CNAME-Eintrag für die Subdomain www
echo "Ändere den CNAME-Eintrag für die Subdomain www"
squarespace_dns_command www.your_domain.com CNAME <squarespace_url>

echo "DNS-Einstellungen für movielegends.com wurden aktualisiert."
