
#DataBus


```pip install pika```

##Mac:
```pip3 install pika```
```brew update```
```brew install rabbitmq```

The RabbitMQ server scripts and CLI tools are installed into the sbin directory 
under /usr/local/Cellar/rabbitmq/<version>/, 
which is accessible from /usr/local/opt/rabbitmq/sbin. 
Links to binaries have been created under /usr/local/sbin. 
In case that directory is not in PATH it's recommended to append it:
```export PATH=$PATH:/usr/local/sbin```

launch on foreground (seem to be best to used queue):
```rabbitmq-server```

launch on background rabbitmq with :
```brew services start rabbitmq```
stop it:
```brew services stop rabbitmq```
restart it:
```brew services restart rabbitmq```