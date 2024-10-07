NGINX_CONF = """
worker_processes auto;
events {
    worker_connections 1024;
}
http {
    limit_conn_zone $binary_remote_addr zone=addr:10m;
    limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=1r/s;


    underscores_in_headers on;
    ignore_invalid_headers off;
    client_max_body_size 0;
    proxy_intercept_errors on;

    server {
        listen {{external_axon_port}};
        location / {

            if ($http_bt_header_dendrite_hotkey = "") {
                return 401;
            }
            if ($http_sec_ch_ua ~* "Not\(A:Brand") {
                return 403;
            }
            if ($http_sec_ch_ua ~* "Not A\(Brand") {
                return 403;
            }
            limit_conn addr 10;
            limit_req zone=req_limit_per_ip burst=5 nodelay;
            proxy_pass http://127.0.0.1:{{internal_axon_port}};

        }
    }
}
"""
