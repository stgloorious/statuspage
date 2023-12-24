# Status Page for Homelab
This is the source code for my simple status website built using Flask.
Upon visiting the site, the Flask app makes a few simple queries to see
which services are online.

![Screenshot](docs/statuspage.png)

## TODO
 - [x] Basic functionality
 - [x] Config file instead of hard-coded domains
 - [ ] Config file instead of hard-coded queries
 - [ ] Add more informative text instead of "OK" and "UNREACHABLE"
 - [ ] IPv6 things

## Development
For local development, use
~~~
flask --app statuspage run
~~~

## Deployment
See the [Flask documentation](https://flask.palletsprojects.com/en/latest/deploying/nginx/)
for more information.

Configure the webserver to serve `/static` directly and provide a config.json with your domains:
~~~
{
    "domains" : ["example.com", "localhost"],
    "hostname" : "foo.bar"
}
~~~
