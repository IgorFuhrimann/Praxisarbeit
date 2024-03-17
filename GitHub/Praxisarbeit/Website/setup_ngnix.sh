#!/bin/bash

# Nginx Konfiguration erstellen
sudo tee /etc/nginx/sites-available/movielegends.com.conf > /dev/null <<EOF
server {
    listen 80;
    server_name movielegends.com www.movielegends.com;

    location / {
        proxy_pass http://localhost:5000; # Hier den Port deiner Flask-Anwendung angeben
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Symbolischen Link erstellen, um die Konfiguration zu aktivieren
sudo ln -s /etc/nginx/sites-available/movielegends.com.conf /etc/nginx/sites-enabled/

# Konfiguration überprüfen und Nginx neu starten
sudo nginx -t && sudo systemctl restart nginx

# Firewall konfigurieren, um HTTP-Verkehr zuzulassen
sudo ufw allow 'Nginx HTTP'

echo "Nginx-Konfiguration für movielegends.com wurde aktualisiert."
