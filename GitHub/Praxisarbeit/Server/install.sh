#!/bin/bash

# Funktion zum Installieren von Tools auf einer Azure-VM

install_tools() {
    echo "Aktualisiere das Paketverzeichnis..."
    sudo apt update

    echo "Installiere Git..."
    sudo apt install git -y

    echo "Installiere Python und pip..."
    sudo apt install python3 python3-pip -y

    echo "Installiere Flask..."
    sudo pip3 install flask

    echo "Installiere MariaDB..."
    sudo apt install mariadb-server -y

    echo "Installiere Nginx..."
    sudo apt install nginx -y

    echo "Tools wurden erfolgreich installiert."
}

# Hauptprogramm
install_tools
