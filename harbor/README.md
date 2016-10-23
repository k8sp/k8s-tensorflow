# Harbor 使用与配置

## Harbor 使用
没有开启 SSL 认证的 Harbor，跳过配置证书步骤，同时，需要添加 `--insecure-registry harbor.ail.unisound.com`，参考 https://docs.docker.com/registry/insecure/

### 配置证书
开启 SSL 认证的 Harbor，需要在每台进行 docker login/push/pull 操作的机器上配置证书。其中 `harbor.ail.unisound.com` 为 Harbor 地址，`ca.crt` 是在配置 Harbor 是生成的证书。

* CoreOS

  ```
   sudo bash ./update_certs_coreos.sh harbor.ail.unisound.com ca.crt
  ```

* CentOS (Redhat)

  ```
  sudo bash ./update_certs_centos.sh harbor.ail.unisound.com ca.crt
  ```

* Ubuntu

  ```
  sudo bash ./update_certs_ubuntu.sh harbor.ail.unisound.com ca.crt
  ```

## 使用 Harbor
* 登陆 Harbor
  ```
  docker login https://harbor.ail.unisound.com
  ```
  网页版的 Harbor 在浏览器中输入 `https://harbor.ail.unisound.com`

* 上传/下载 images

  成功登陆之后，通过 `docker push harbor.ail.unisound.com/project/imagename:tag` 上传 docker images。
  通过 `docker pull harbor.ail.unisound.com/project/imagename:tag` 拉去 docker images，对于公开的 docker images， 拉取不需要登陆验证。




## Harbor 配置
[Harbor 配置](how-to-config-harbor.md)


## 参考
* https://docs.docker.com/registry/insecure/
