echo "Installing packages....."
echo "Installing Eventlet"
pipOut=$(pip3 install eventlet)
echo "Installed Eventlet"
echo "Installing Socket IO"
pipOut=$(pip3 install python-socketio)
pipOut=$(pip3 install "python-socketio[client]")
echo "Installed Socket IO"
echo "Installing Pillow"
pipOut=$(pip3 install wheel)
pipOut=$(pip3 install Pillow)
echo "Installed Pillow"
echo "Starting Application"
python3 SocketIOClient.py


