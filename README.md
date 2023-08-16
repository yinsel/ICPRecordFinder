# 使用方法

- 安装依赖

```cmd
pip install -r requirements.txt
```

- 运行redis

```cmd
cd redis
```

- 运行代理池

```cmd
cd proxy_pool
# 安装代理池依赖
pip install -r requirements.txt
# 启动调度程序
python proxyPool.py schedule
# 启动webApi服务
python proxyPool.py server
```

- 运行脚本

```cmd
python icp_record_finder.py -l domain.txt
```
