# Linux下常见网络故障的处理思路

1. 网络硬件问题，可以通过检测网线、网卡、集线器、路由器、交换机等是否正常来确认是否由硬件问题造成网络故障。

2. 检查网卡是否正常工作，可以从网卡驱动是否正常加载、网卡IP设置是否正确、系统路由设置是否正确等三个方面确认。

3. 检查局域网主机之间的练级是否正常，可以通过ping自身IP、ping局域网其他主机IP、ping网关地址等方式来确认。

4. 检查DNS是否设定正确，可以从Linux的DNS客户端配置文件**/etc/resolv.conf**、本地主机文件**/etc/hosts**进行确认。

5. 服务是否正常打开，可以通过Telnet或netstat命令检测服务是否开启。

6. 检查访问权限是否打开，可以从本机iptables防火墙、Linux内核强制访问控制策略SELinux两方面入手。

   # 检查网卡是否正常

   1. 检查网卡是否正常加载：通过lsmod、ifconfig命令判断网卡是否正常加载，如果通过ifconfig可以显示网络接口（eth0、eth1）的配置信息，表示系统已经找到网卡驱动程序，检测到网络设备，网卡加载正常。
   2. 检查网卡IP设置是否正确：检查网卡的软件设置是否正确，如IP是否配置、配置是否正确、确保IP的配置和局域网其他服务器的配置没有冲突。
   3. 检查系统路由表信息是否正确：

   # 检查DNS解析文件是否设置正确

   在Linux系统中，有两个文件用来指定系统到哪里寻找相关域名解析的库：分别是文件**/etc/host.conf**和**/etc/nsswitch.conf**。**/etc/host.conf**用来指定系统如何解析主机名，Linux系统通过域名解析库来获得主机名对应的IP地址。下面是CentOS系统安装后默认的**/etc/host.conf**内容：

   order hosts,bind

   其中，order指定主机名查询顺序，这里表示首先查找**/etc/hosts**文件对应的解析，如果没有找到对应的解析，接下来就根据**/etc/resolve.conf**指定的域名服务器进行解析。

   **/etc/nsswitch.conf**文件是由SUN公司开发，用于管理系统中多个配置文件查询的顺序。由于**nsswitch.conf**提供了更多的资源控制方式，因此它现在已经基本取代了**hosts.conf**文件。虽然Linux系统中两个文件默认都在，但实际上起作用的是**nsswitch.conf**文件。

   **nsswitch**文件每行都以一个关键字开头，后面跟冒号，紧接着是空白，然后是一系列方法的列表。

   如：

   > hosts:    files dns

   表示系统首先查询**/etc/hosts**文件，如果没有找到对应的解析，就会去DNS配置文件制定的DNS服务器上进行解析。

   # 检查服务是否正常打开

   在一个应用出现故障时，必须要检查的是服务本身，比如服务是否开启，配置是否正确等。检查服务是否正确打开分两步，第一步是查看服务的端口是否打开。

   例如：我们不能用root用户SSH登录10.10.80.89这台Linux服务器，首先检查sshd服务的22端口是否打开：

   > telnet 10.10.80.89 22

   如果没有任何输出，表示服务没有启动或者服务端口被屏蔽。

   也可以在服务器上通过netstat命令检查22端口是否打开：

   ```netstat -ntl```

   第二步，既然服务已经启动，就可能是sshd服务配置问题，检查sshd服务端配置文件**/etc/ssh/sshd_config**，发现有下面一行信息：

   > PermitRootLogin no

   由此可知是SSH服务端配置文件限制了root用户不能登录系统，如果需要root用户登录系统，只需要更改为如下即可：

   > PermitRootLogin yes

   # 检查访问权限是否打开

   1. 检查系统防火墙iptalbes的状态

   ```#iptables -L -n
   #iptables -L -n
   #iptables -A INPUT -i eth0 -p tcp --dport 80 -j ACCEPT
   #iptables -A OUTPUT -p tcp --sport 80 -m state --state ESTABLISED -j ACCEPT
   ```

   1. 检查SELinux是否打开

   定位问题，最简单的办法是先关闭SELinux，然后测试软件运行是否正常。

   # 检查局域网主机之间联机是否正常

   可以先通过ping命令测试局域网主机之间的连通性，然后ping网关，检测主机到网关的通信是否正常。




