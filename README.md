# Status Page for Homelab
This is the source code for my simple status website built using Flask.
Upon visiting the site, the Flask app makes a few simple queries to see
which services are online.

![Screenshot](docs/statuspage.png)

## TODO
 - [x] Basic functionality
 - [x] Config file instead of hard-coded domains
 - [x] Config file instead of hard-coded queries
 - [ ] Add more informative text instead of "OK" and "UNREACHABLE"
 - [ ] IPv6 things

## Development
For local development, use
~~~
flask --app statuspage run
~~~

## Deployment
See the [Flask documentation](https://flask.palletsprojects.com/en/latest/deploying/nginx/)
for more information. I use Apache with simple CGI because there is no
(performance) reason to set up FastCGI or similar.

Provide a `config.json` with your domains:
~~~
{
    "hostname": "foo.bar"
    "domains": [
        {
            "uri": "example.com",
            "supported_queries": [
                "ping",
                "dns",
                "https"
            ]
        },
        {
            "uri": "localhost",
            "supported_queries": [
                "ping",
                "http",
                "https"
            ]
        }
    ],
    "query_types": [
        {
            "id": "ping",
            "pretty_name": "Ping",
            "cmd": [
                "ping",
                "-W",
                "3",
                "-c",
                "1",
                "{uri}"
            ],
            "text_nonzero": "UNREACHABLE",
            "text_zero": "OK",
            "color_nonzero": "f07070",
            "color_zero": "70f070"
        },
        {
            "id": "dns",
            "pretty_name": "DNS",
            "cmd": [
                "nslookup",
                "{uri}"
            ],
            "text_nonzero": "UNREACHABLE",
            "text_zero": "OK",
            "color_nonzero": "f07070",
            "color_zero": "70f070"
        },
        {
            "id": "https",
            "pretty_name": "HTTPS",
            "cmd": [
                "curl",
                "--max-time",
                "3",
                "-f",
                "https://{uri}"
            ],
            "text_nonzero": "UNREACHABLE",
            "text_zero": "OK",
            "color_nonzero": "f07070",
            "color_zero": "70f070"
        },
        {
            "id": "http",
            "pretty_name": "HTTP",
            "cmd": [
                "curl",
                "--max-time",
                "3",
                "-f",
                "http://{uri}"
            ],
            "text_nonzero": "UNREACHABLE",
            "text_zero": "OK",
            "color_nonzero": "f07070",
            "color_zero": "70f070"
        }
    ]
}
~~~

Configure your webserver with CGI to run the script. Make sure to not expose
unwanted files (`.git`, `__pycache__`, `config.json`).


## Issues
If you run into issues using ping, make sure capabalities for normal users
are set:

~~~
setcap cap_net_raw+p /bin/ping
~~~
