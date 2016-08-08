import sys
import time


class Config:
	nginxDir = '/etc/nginx/'

	nginxConfDir = '/conf.d/'

	nginxConfFileName = 'nginx.conf'

	nginxTypesFileName = 'mime.conf'

	nginxProxyFileName = 'proxy.conf'

	nginxFcgiFileName = 'fcgi.conf'

	nginxConf = {
		'user'                : 'www-data www-data',
		'pid'                 : '/var/run/nginx.pid',
		'worker_processes'    : '2',
		'worker_rlimit_nofile': '100000',
		'events'              : {
			'worker_connections': '4096',
			'include'           : '/etc/nginx.custom.events.d/*.conf',
		},
		'http'                : {
			'default_type'                 : 'application/octet-stream',
			'access_log'                   : 'off',
			'error_log'                    : '/var/log/nginx/error.log crit',
			'sendfile'                     : 'on',
			'tcp_nopush'                   : 'on',
			'keepalive_timeout'            : '20',
			'client_header_timeout'        : '20',
			'client_body_timeout'          : '20',
			'reset_timedout_connection'    : 'on',
			'send_timeout'                 : '20',
			'types_hash_max_size'          : '2048',
			'gzip'                         : 'on',
			'gzip_disable'                 : '"msie6"',
			'gzip_proxied'                 : 'any',
			'gzip_min_length'              : '256',
			'gzip_comp_level'              : '4',
			'gzip_types'                   : 'text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript application/javascript text/x-js',
			'server_names_hash_bucket_size': '128',
			'charset'                      : 'UTF-8',
			'open_file_cache'              : 'max=100000 inactive=20s',
			'open_file_cache_valid'        : '30s',
			'open_file_cache_min_uses'     : '2',
			'open_file_cache_errors'       : 'on',
			'server_tokens'                : 'off',
			'ssl_protocols'                : 'TLSv1 TLSv1.1 TLSv1.2',
			'include'                      : [
				'proxy.conf',
				'fcgi.conf',
				'mime.conf',
				'conf.d/*.conf',
				'/etc/nginx.custom.d/*.conf'
			]
		},
		'include'             : [
			'/etc/nginx.custom.global.d/*.conf',
		]
	}

	nginxTypes = {
		'types': {
			'text/html'                           : 'html htm shtml',
			'text/css'                            : 'css',
			'text/xml'                            : 'xml rss',
			'image/gif'                           : 'gif',
			'image/jpeg'                          : 'jpeg jpg',
			'application/x-javascript'            : 'js',
			'text/plain'                          : 'txt',
			'text/x-component'                    : 'htc',
			'text/mathml'                         : 'mml',
			'image/png'                           : 'png',
			'image/svg+xml'                       : 'svg svgz',
			'image/x-icon'                        : 'ico',
			'image/x-jng'                         : 'jng',
			'image/vnd.wap.wbmp'                  : 'wbmp',
			'application/java-archive'            : 'jar war ear',
			'application/mac-binhex40'            : 'hqx',
			'application/pdf'                     : 'pdf',
			'application/x-cocoa'                 : 'cco',
			'application/x-java-archive-diff'     : 'jardiff',
			'application/x-java-jnlp-file'        : 'jnlp',
			'application/x-makeself'              : 'run',
			'application/x-perl'                  : 'pl pm',
			'application/x-pilot'                 : 'prc pdb',
			'application/x-rar-compressed'        : 'rar',
			'application/x-redhat-package-manager': 'rpm',
			'application/x-sea'                   : 'sea',
			'application/x-shockwave-flash'       : 'swf',
			'application/x-stuffit'               : 'sit',
			'application/x-tcl'                   : 'tcl tk',
			'application/x-x509-ca-cert'          : 'der pem crt',
			'application/x-xpinstall'             : 'xpi',
			'application/zip'                     : 'zip',
			'application/octet-stream'            : [
				'deb',
				'bin exe dll',
				'dmg',
				'eot',
				'iso img',
				'msi msp msm',
			],
			'audio/mpeg'                          : 'mp3',
			'audio/ogg'                           : 'oga ogg',
			'audio/wav'                           : 'wav',
			'audio/x-realaudio'                   : 'ra',
			'video/mp4'                           : 'mp4',
			'video/mpeg'                          : 'mpeg mpg',
			'video/ogg'                           : 'ogv',
			'video/quicktime'                     : 'mov',
			'video/webm'                          : 'webm',
			'video/x-flv'                         : 'flv',
			'video/x-msvideo'                     : 'avi',
			'video/x-ms-wmv'                      : 'wmv',
			'video/x-ms-asf'                      : 'asx asf',
			'video/x-mng'                         : 'mng',
		}

	}

	nginxProxy = {
		'proxy_redirect'         : 'off',
		'proxy_set_header'       : [
			'Host            $host',
			'X-Real-IP       $remote_addr',
			'X-Forwarded-For $proxy_add_x_forwarded_for'
		],
		'client_body_buffer_size': '128k',
		'proxy_connect_timeout'  : '90',
		'proxy_send_timeout'     : '90',
		'proxy_read_timeout'     : '90',
		'proxy_buffers'          : '32 4k',
	}

	nginxFcgi = {
		'fastcgi_param': {
			'QUERY_STRING'     : '$query_string',
			'REQUEST_METHOD'   : '$request_method',
			'CONTENT_TYPE'     : '$content_type',
			'CONTENT_LENGTH'   : '$content_length',
			'SCRIPT_FILENAME'  : '$document_root$fastcgi_script_name',
			'SCRIPT_NAME'      : '$fastcgi_script_name',
			'PATH_INFO'        : '$fastcgi_path_info',
			'REQUEST_URI'      : '$request_uri',
			'DOCUMENT_URI'     : '$document_uri',
			'DOCUMENT_ROOT'    : '$document_root',
			'SERVER_PROTOCOL'  : '$server_protocol',
			'GATEWAY_INTERFACE': 'CGI/1.1',
			'SERVER_SOFTWARE'  : 'nginx/$nginx_version',
			'REMOTE_ADDR'      : '$remote_addr',
			'REMOTE_PORT'      : '$remote_port',
			'SERVER_ADDR'      : '$server_addr',
			'SERVER_PORT'      : '$server_port',
			'SERVER_NAME'      : '$server_name',
			'HTTPS'            : '$https',
			'REDIRECT_STATUS'  : '200',
		}
	}
