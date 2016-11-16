# 配置 Harbor

## 证书生成
* 若 harbor 域名为 harbor.ail.unisound.com，在 Ubuntu 上执行:
  ```bash
bash generate_cert.sh ail.unisound.com
```
或者若无域名，根据 IP 生成证书，若 IP 为 10.10.14.253，执行:

  ```bash
bash generate_cert.sh 10.10.14.253
```

* harbor 配置需要三个文件:

| 文件         | 用途                         |
| ------------ | ---------------------------- |
| dns/IP.crt   | 供 nginx 配置 ssl            |
| dns/IP.key   | 供 nginx 配置 ssl            |
| ca.crt       | 供 客户端设置访问            |

## 配置文件修改



## 参考
* https://github.com/vmware/harbor/blob/master/docs/configure_https.md
