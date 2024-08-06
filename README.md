# flask-ipinfo

## Installation
```shell
 git clone https://github.com/git1e/flask-ipinfo.git --recurse-submodules
 cd scripts && bash init_ip_db.sh
```

## nginx 配置
```shell
server {
    listen 80;
    server_name ipinfo.com;

    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $http_host;
    proxy_set_header X-NginX-Proxy true;

    location / {

        proxy_pass http://127.0.0.1:5000;

        access_log /data/logs/nginx/ipinfo-access.log json_format;
        error_log /data/logs/nginx/ipinfo-error.log;
    }
}

```