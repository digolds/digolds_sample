internet_title = """互联网是如何运作的？"""
internet_description = """在编写Web Service之前，你需要对互联网有一个清晰的认识，原因在于你编写的服务一般会接入互联网。为了让你快速地进入状态，本文将通过以下几方面来介绍互联网："""
internet_content = """# 互联网是如何运作的？

在编写Web Service之前，你需要对互联网有一个清晰的认识，原因在于你编写的服务一般会接入互联网。为了让你快速地进入状态，本文将通过以下几方面来介绍互联网：

* 什么是互联网（Internet）
* 什么是HTTP协议
* HTTP协议的消息格式
* 访问[https://www.digolds.cn](https://www.digolds.cn)
* Web Service

![](https://2cloudlab.com/images/blog/isp-internet.png)

## 什么是互联网（Internet）

**互联网（Internet）**是一张巨大的网络，它覆盖全球，把所有局域网连接在一起，打通了世界各地信息流转的路径。你只需要将手机或者电脑接入互联网，就可以访问世界另外一端的服务器，并从上面获取或提交信息。同理，其他使用互联网的人也能够看到你提交的信息。以下示意图刻画了这种关系：

![](https://2cloudlab.com/images/blog/TheWeb.png)

为了能让互联网上的设备交换信息（即通信），则需要一套双方达成共识的**协议（protocols）**。常用的协议有：**TCP**，**IP**，**HTTP**，**DNS**等等，它们共同协作，最终使得互联网中的任何2台设备都能相互通信。这些协议还在不断演化，它们的制定者基本上都来自美国互联网协会，协会成员来自各大知名互联网公司，比如Google，微软，甲骨文等等。

以上提到的协议几乎每天都在使用，其中**HTTP**协议可能是研发人员经常使用的。比如，你用浏览器访问[digolds.cn](www.digolds.cn)的过程就使用了该协议；或者，你使用微博或知乎手机客户端阅读微博和问答，也使用了该协议。由于**HTTP**协议太流行了，所以接下来，让我们花一些时间来了解它。

## 什么是HTTP协议

![](https://2cloudlab.com/images/blog/Fetching_a_page.png)

HTTP是一种基于客户-服务器模式来运作的协议，客户端遵守它来向服务器发出**请求（request）**，以便获取资源（比如HTML，CSS，JS文档，图片，视频或其它）。服务器接收到这些请求，并根据HTTP协议来解析它们，然后再根据请求里的内容选择对应的处理逻辑，最后把**结果（response）**返回给客户端，犹如上图所示。上图表明，一个接入互联网的设备（上图最左边）为了获取一个Web document中的所有信息（HTML，Image，Video，Ads），它需要通过Internet和HTTP协议来分别与3个服务器进行交互。

首先，它通过以下顺序来获取Web document：

1. 发送`GET page.html`请求，该请求到达Web server，此时Web server会返回Web document
2. 此时的Web document包含了4个**超链接**，它们指向另外一些资源，这些资源遍布在不同的服务器上（Ads server，Web server和Video server）

接着，它依然通过Internet和HTTP协议来异步获取剩下的4个资源，它们分别是：`GET layout.css`，`GET image.png`，`GET video.mp4`和`GET ads.jpg`。发起这一系列请求的客户端软件有**浏览器**，然而也可以是一些支持HTTP协议的客户端软件，比如手机端的微博APP。

HTTP协议具有扩展能力，因此它从1990s开始就在不停地演化，期间经历了以下几个版本：

* HTTP/1.0
* HTTP/1.1
* HTTP/2

版本越高，它的效率越好，比如HTTP/2可以重复使用同一个连接来连续发送多个请求和接收多个响应，而HTTP/1.0只能支持一对请求和响应/每个新连接。除此之外，为了支持高版本的HTTP协议，就意味着要升级其它已经存在的系统，对一个庞大的系统进行升级是非常困难的，因此，你会看到依然有大量的系统使用HTTP/1.1协议。

HTTP协议不是单独存在的，它在应用层使用，并依赖于其它底层协议，如下图所示：

![](https://2cloudlab.com/images/blog/HTTP & layers.png)

HTTP需建立在一个稳定的连接上，因此需要依赖于TCP协议。如果，想在稳定的连接上面传输加密信息，那么需要借助TLS协议，它也是基于TCP协议的。

当你在浏览器里看见正在访问的网址是以`http`开头，那么说明该连接是基于TCP的。如果是以`https`开头的，则说明该连接是基于TLS的。

客户端向服务端发送的请求会经过互联网上的多个服务节点（每个服务节点可能由一台或多台计算机组成），并以**代理（Proxy）**的角色将请求转发出去，指导请求到达服务端。同理，服务端会沿着之前的路径将结果返回。整个过程如下图所示：

![](https://2cloudlab.com/images/blog/Client-server-chain.png)

常见的Proxies有网络上的Routers（路由器）和Cache（缓存）节点等等，前者会修改请求并转发，而后者仅仅将请求缓存并转发。

由于互联网是属于公开的，因此为了安全起见，最好使用基于TLS的HTTP协议-即`https`来加密和传输数据。

## HTTP协议的消息格式

基于HTTP/1.1及之前版本的消息是可阅读的，而基于HTTP/2的消息是难以阅读、需要借助一些工具，但是它们的语义格式是一样的。因此，通常需要基于之前版本来理解HTTP协议的消息格式。

HTTP协议定义了2类消息：**Request**和**Response**，它们的格式如下所示：

### 1）Request

![](https://2cloudlab.com/images/blog/HTTP_Request.png)

它由以下部分组成：

* Method，此次请求的操作，有POST、GET、PUT、DELETE等等
* Path，资源的路径
* Version of the protocal，HTTP协议的版本
* Headers，请求的头，里面是一系列KEY-VALUE键值对
* Body，请求的数据体

### 2）Response

![](https://2cloudlab.com/images/blog/HTTP_Response.png)

它由以下部分组成：

* Status code，返回的状态码
* Status message，返回的信息
* Version of the protocal，HTTP协议版本
* Headers，返回结果的头，里面是一系列KEY-VALUE键值对
* Body，返回的数据体

## 访问[https://www.digolds.cn](https://www.digolds.cn)

接下来让我们分析，在浏览器中访问[https://www.digolds.cn](https://www.digolds.cn)，其背后都发生了什么。

### 1）域名解析

![](https://2cloudlab.com/images/blog/dns-workflow.png)

1. 把网址分解成域名（[www.digolds.cn](https://www.digolds.cn)）和**https**协议。前者主要由3部分组成，分别是顶级域名**cn**、域名**digolds**、子域名**www**（其中**digolds.cn**组合在一起被称为根域名），后者使浏览器使用TLS协议来传输数据。
2. 浏览器根据**DNS**协议，向DNS服务器发送域名解析请求，DNS服务器返回对应的IP地址。整个DNS协议是基于UDP协议来完成的。
3. UDP协议会依赖于IP协议，UDP的Package加上IP信息，形成一个完整的IP Package，然后通过路由器（Routers）转发到DNS Server。

### 2）TCP连接

![](https://2cloudlab.com/images/blog/https-tcp-ip-workflow.png)

1. 浏览器根据域名解析阶段获得的IP地址，向服务器建立TCP连接。
2. 三次握手，建立稳定连接。每次握手，其TCP的数据包（Packages）均需要转换成IP数据包，然后由路由器接收和转发。

### 3）https认证

![](https://2cloudlab.com/images/blog/https-workflow.png)

1. digolds服务器向浏览器发送Certificate和Public Key。
2. 浏览器向第三方可信的CAs机构验证获得的Certificate，如果验证失败，则提示用户，否则进行下一步
3. 浏览器生成一个Session Key，并用Public Key对Session Key和Request信息进行非对称加密，然后发送给服务端。
4. 服务端接收到浏览器发送过来的加密请求，并用Private Key对请求进行解密，同时获得Session Key和其它请求的数据。
5. 当服务端准备给浏览器返回信息时，它会使用Session Key对这些信息进行加密。
6. 当浏览器接收到加密的信息之后，它会使用Session Key对这些信息进行解密。
7. 同理，当浏览器需要继续向服务端发送请求时，它会使用Session Key对信息进行加密。
8. 直到浏览器把整个页面显示出来整个过程才会停止。

接入设备（比如PC，Mobile Phone，服务器，路由器，DNS服务器等）与互联网以及协议之间的协作关系如下图所示：

![](https://2cloudlab.com/images/blog/what-happen-when-visit-a-site.png)

除了以上提到的协议之外，还有其它常用的协议，比如文件传输协议（FTP）、邮件传输协议（SMTP）、SSH等等。这些协议、服务器、路由器、DNS服务器、物理链路等等一起支撑着互联网的运行（全天候7*24小时），由此可见，互联网已经成为现代社会不可或缺的基础设施，如果有一天它瘫痪了，全球不计其数的设备将受到影响。

## Web Service

互联网上有一些节点位于互联网的另外一头-**服务端**，它们的作用是提供服务，我们称之为**Web Service**，经常由各大公司提供。常见的Web Service有：淘宝、微博、知乎、百度等等，为了提供这些服务，各自公司均需要在自己的数据中心或云计算平台上运行上万台**服务器或虚拟机（Application Servers）**，然后根据业务逻辑，并在每台服务器或者虚拟机上安装不同的软件。最终，一个庞大的服务会分解成多个子服务，以淘宝为例，它的子服务有：存储服务、用户认证和授权服务、商品陈列服务、购物车服务、支付服务等等，每个子服务均由多台服务器或虚拟机支撑，子服务之间通过gRPC、Restful或GraphQL方式来交互，以下是一个简化版的示意图：

![](https://2cloudlab.com/images/blog/web-service-break-down.png)

其中Service Bus和API Gateway也是由多台服务器或虚拟机支撑着，前者的作用是支持gRPC、Restful或GraphQL，并接收或传递不同子服务的消息，而后者的作用是接收来自客户端的请求，并把这些请求均匀地分发到不同的子服务。

因此，大多数研发人员的工作会集中在这些子服务中，也就是我们常说的后端研发。相对于后端研发，还有一类研发人员的主要工作是针对不同设备：手机、PC、平板电脑等来研发客户端程序，这些程序很可能会通过HTTP协议来使用后端的服务，这也就是我们常说的前端研发。由于这个系列的文章是关于[digwebs](https://github.com/digolds/digwebs)的，它是一个Web框架，用于后端服务，因此我们的关注点只集中在后端研发。

由上图可知，子服务之间非常独立，你可以选择Python来研发商品陈列服务，也可以选择C++来研发支付服务。除此之外，每个子服务均由不同的团队来负责，这样，工作得以同时进行。子服务内部运行着大量的服务器或虚拟机，因此你需要设计子服务的结构并安装相对应的程序，这些程序有自己研发的，也有使用开源的，这完全由研发该子服务的团队来决定。比如，你决定使用Python来研发商品陈列服务，其架构图如下所示：

![](https://2cloudlab.com/images/blog/web-service-python-nginx.png)

商品陈列服务由以下部分组成：

1. 由开源Web服务器软件-Nginx，构成的负载均衡服务，所有的HTTP请求均会先到达Nginx服务，然后解析HTTP请求，获取Method，Path，Protocol Version，Headers，Body等信息。
2. 一族虚拟机（VM），每台虚拟机上运行着Python+digwebs编写的程序，Nginx服务通过WSGI协议与这些程序交互。
3. 使用AWS的DynamoDB服务来存储商品数据，VM与这一层之间的交互是由HTTP协议完成的。

以上只是一个比较简单的架构，现实世界里可能存在更加复杂的架构。通过上图可知，后端研发依然有大量的事情要做，比如，你需要安装和部署Nginx集群服务、研发和部署digwebs应用、应用第三方服务（比如使用了AWS的DynamoDB服务）等等，其中涉及到企业内部的局域网（Intranet）和外部的互联网（Internet）。互联网的兴起是由多方来决定的，没有服务提供者（Server）或消费者（Client），它的存在是没有价值的。随着各种丰富的服务接入互联网，比如视频服务、缴费服务、市政服务等，以及手机的普及，它的价值进一步放大，人们已经无法摆脱对它的依赖。

## 结束语

网民通过浏览器来访问[digolds.cn](https://www.digolds.cn)的过程，表面上似乎很简单，输入网址，回车，得到返回页面，然而在这背后却触发了一系列行为以及牵涉到了大量系统。为了支持背后的逻辑，互联网因应而生，美国互联网标准委员会为它定义了各种协议，比如HTTP、TCP/IP、UDP等等，网络提供商为它提供了路由器，域名运营商为它提供了域名解析服务器，企业为它提供了各种Web Service，从搜索到电商，无所不有，最终网民使用手机或电脑来享受它带来的便捷。**它是一个连接信息的工具，使得人类获取和输送信息的能力从手指间延伸到全世界**。

本文通过一个HTTP请求来揭开互联网内部的运行逻辑，旨在让读者从全局来理解：一个Web服务的组成、运行在哪里（之前的**ORG**处）、如何与互联网配合、如何为用户提供服务。如果你想成为一个后端研发工作者，那么理解HTTP和TCP/IP协议是必不可少的，本文仅仅涉及了一些关于HTTP协议的皮毛知识，比如Request和Response格式，然而其中有大量的细节需要在工作中学习和总结，[Mozilla](https://developer.mozilla.org/en-US/docs/Web)在这方面做了大量的工作，当你遇到问题时，不妨到那里看看，收获一定会不少。

[digwebs](https://github.com/digolds/digwebs)仅仅是一个基于Python编写的Web框架，它可以用来编写网站（比如[digolds](https://www.digolds.cn)），也可以用来编写Web服务（提供Restful API）。然而，想要将它提供给网民使用，则还需要依赖其它基础设施，比如Nginx集群服务，虚拟机（VM）和Python运行时环境等等，以及通过HTTP和WSGI协议把它们连接起来，示意图如下所示：

![](https://2cloudlab.com/images/blog/sub-web-service.png)

上图VM部分就是我们需要关注的，因为那里运行着由[digwebs](https://github.com/digolds/digwebs)驱动的Python程序。如果你阅读到这里，很可能想知道如何使用digwebs来编写一个类似于digolds的Web应用，那么[文章-《如何使用digwebs框架来编写Web应用》](https://www.digolds.cn/article/001553757423266a02c9e9f7bc44159829e2db86d0d076d000)就是为你准备的!

## 参考

1. [An overview of HTTP.](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
2. [How HTTP requests work.](https://flaviocopes.com/http-request/)
3. [How HTTPS works Part 1 — Building Blocks.](https://medium.com/@animeshgaitonde/how-https-works-part-1-building-blocks-64f9915b1f39)
4. [Behind the scenes when u type www.google.com in browser.](https://stackoverflow.com/questions/6241991/how-exactly-https-ssl-works)
5. [Web Server vs. Application Server.](https://www.ibm.com/cloud/learn/web-server-vs-application-server)"""