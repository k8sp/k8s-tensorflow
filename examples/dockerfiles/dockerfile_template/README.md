# tips

base images 一进去是运行 jupyter 的，
而且 imports tensorflow 报错了，
后来知道是 base 需要 gpu 才可以运行。
所以不需要重新安装 tensorflow 了，
而且新安装的 tensorflow 是不支持 gpu 的，
也没有 SSE 支持等。

所以，这个目录下的文件用不着了。

需要时参看：examples/dockerfiles
