from pyngrok import ngrok

sshConnection = ngrok.connect(21210,'tcp')
print(sshConnection)
