# FKOFVDI
通过有长度限制的共享剪切板传输图片  
Under the usual office network, the internal network is completely isolated from the external network, 
and the external network access behavior is realized through Remote Desktop Services, and only one-way file copy operations are allowed.  
In order to solve the problem that it is inconvenient to copy pictures in this scenario, 
this tool was written to copy pictures through one-way clipboard sharing that only allows the content of strings of specified length (4096).

##### Pack with Pyinstaller 
```shell
pyinstaller.exe main.spec
```
![image](https://github.com/Qinglys/FKOFVDI/assets/37425041/35a80757-a776-4d62-87f2-97deabeabb13)
