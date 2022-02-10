<div>
  <h3>Linux Server and Django Setup</h3>
  <p>
    Setting up a Raspberry Pi 4 Model B (or Ubuntu VM) Django website using NGINX and MongoDB. The stack is as follows: <br>
    <ul>
      <li><a href="https://timelined.live">https://timelined.live</a></li>
      <li>NGINX</li>
      <li>Unix Socket</li>
      <li>uWSGI (Web Server Gateway Interface)</li>
      <li>Django (Web Framework)</li>
      <li>MongoDB (Database)</li>
  </ul>
  </p>
	<h4>Raspberry Pi Specifications</h4>
	<ul>
    <li>OS: Ubuntu Server 20.04.3 LTS (aarch64)</li>
    <li>Model: Raspberry Pi 4 Model B</li>
    <li>CPU: BCM2835 (4) @ 1.5GHz</li>
    <li>Memory: 2GB</li>
    <li>Kernel: 5.4.0-1048-raspi</li>
    <li>Shell: bash 5.0.17</li>
</ul>
	<h4>Pi Base Setup</h4>
	<ol>
    <li>Download latest LTS (Long Time Support) Ubuntu server from <a href="https://ubuntu.com/download/server">https://ubuntu.com/download/server</a></li>
    <li>Burn .iso to Raspberry Pi SD card (I recommend using <a href="https://www.balena.io/etcher/">balenaEtcher</a>)</li>
    <li>Connect Raspberry Pi to monitor, keyboard, and power</li>
    <li>Follow on-screen installation instructions</li>
    <li><code>sudo apt upgrade</code></li>
    <li><code>sudo apt upgrade -y</code></li>
</ol>
	<h4>Linux Setup</h4>
	<p>For basic Linux commands and setup <a href="https://docs.google.com/document/d/1qGtuQAEwh_IZSLRGaSSuc97JLEZK2ms-HcEEswflReg/edit?usp=sharing">check out this document.</a> To use Linux you should also be familiar with either <a href="https://www.nano-editor.org/">Nano</a> or <a https://vim.org/>Vim</a>. I recommend learning Vim because it is installed on almost every Linux OS and it is lightweight, fast, and very powerful. The best way to learn Vim is to run (in command-line) <code>vim</code> then <code>:help</code></p>
<h5>Creating a Swapfile</h5>
<pre>
<code>sudo fallocate -l 4GB /swapfile</code>
<code>sudo dd if=/dev/zero of=/swapfile bs=1024 count=1048576</code>
<code>sudo chmod 600 /swapfile</code>
<code>sudo mkswap /swapfile</code>
<code>sudo swapon /swapfile</code>
<code>sudo vim /etc/fstab</code>
<code>	/swapfile swap swap defaults 0 0</code>
<code>sudo mount -a</code>
</pre>
<p>A swapfile essentially allows the Linux operating system to use the system disk (HDD or SSD) as virtual RAM when its available memory is running low. Read more about swapfiles <a href="https://averagelinuxuser.com/linux-swap/">here</a>. For our Raspberry Pi with only 2GB of RAM, it is pretty much essential.</p>
<h5>Editing SSH configuration</h5>
<code>sudo vim /etc/ssh/sshd_config</code>
<p>Uncomment these lines ...</p>
<pre>
<code># Authentication</code>
<code>	LoginGraceTime 2m</code>
<code>	PermitRootLogin prohibit-password</code>
<code>	StrictModes yes</code>
<code>	MaxAuthTries 6</code>
<code>	MaxSessions 10</code>
<code>PrintMotD yes</code>
<code>PrintLastLog yes</code>
</pre>
<h5>Firewall Configuration</h5>
<p>By default, UFW (Uncomplicated Firewall) should be installed on the system, if it is not, install it with <code>sudo apt install ufw</code></p>
<p><a href="https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-20-04">This link</a> will provide you with the basics of configuring the firewall. By default, ufw will <code>sudo ufw default deny incoming</code> and <code>sudo ufw default allow outgoing</code>, which is all we need for now. To enable SSH outside of your local network you need to add an "A" record pointing to the Raspberry Pi's local IP Address in your Router > Firewall > Port Forwarding settings (which you can access by going to <a href="192.168.1.1">192.168.1.1</a> in your browser).</p>
<p>The completed rule should look something like this:</p>
<table>
  <tr>
    <th>Application</th>
    <th>Original Port</th>
    <th>Protocol</th>
    <th>Fwrd to Address</th>
    <th>Fwrd to Port</th>
    <th>Schedule</th>
  </tr>
  <tr>
    <td>SSH</td>
    <td>22</td>
    <td>TCP/UDP</td>
    <td>192.168.1.xxx</td>
    <td>22</td>
    <td>Always</td>
  </tr>
</table>
<p>You can then add the rule to ufw with the command <code>sudo ufw allow ssh</code> and then enabling it with <code>sudo ufw enable</code>. You can reboot your Pi with <code>sudo reboot</code> and try to SSH into it to test everything is working. We will add additional rules when NGINX is configured in a later section.</p>
<h5>Django Configuration</h5>
<p>First setup a virtual environment in Python. This is done with <code>sudo apt install python3-venv</code> and make a new folder <code>mkdir /home/ubuntu/env</code>. Then <code>python3 -m venv /home/ubuntu/env/md</code> and activate it with <code>source /home/ubuntu/env/md/bin/activate</code>. Now that we are in our venv, we can do the following ...</p>
<pre>
<code>pip install Django</code>
<code>pip install djongo</code>
<code>pip install mongoengine</code>
</pre>
<p>Now make a folder in your <code>~/home</code> directory with <code>mkdir "folder-name"</code>. Change into that directory <code>cd "folder-name"</code> and run <code>django-admin startproject "project-name"</code>. In our case the Django files will live in the "website" folder.</p>
<h5>Database (MongoDB) Setup</h5>
<p>For this website we will be using <a href="https://www.mongodb.com">MongoDB</a> as our backend database. To install it on the Raspberry Pi follow <a href="https://www.mongodb.com/developer/how-to/mongodb-on-raspberry-pi/">these instructions.</a> If you get a <strong>mongod.service: Failed with result 'core-dump'</strong> error, follow <a href="https://stackoverflow.com/questions/68937131/illegal-instruction-core-dumped-mongodb-ubuntu-20-04-lts">these instructions</a> to reinstall.</p>
<ol>
<li>From instructions above make note of your Databse <strong>USERNAME</strong> and <strong>PASSWORD</strong></li>
<li><code>mongo -u <strong>USERNAME</strong> -p <strong>PASSWORD</strong></code></li><ul><li><code>use <strong>DATABASE_NAME</strong></code></li>
<li><code>db.test.insert({name:"test", value: 1})</code></li>
<li><code>exit</code></li></ul>
<li>In <code>website/settings.py</code> change: </li>
  <pre><code>DATABASES = {
  	'default': {
  		'ENGINE': 'djongo',
  		'NAME': <strong>'DATABASE_NAME'</strong>,
  		'CLIENT': {
  			'username': <strong>'USERNAME'</strong>,
  			'password': <strong>'PASSWORD'</strong>,
  		}
  	}
}</code></pre>
  <li><code>python3 manage.py makemigrations</code></li>
  <li><code>python3 manage.py migrate</code></li>
</ol>
<p>The following commands create a "test" table in our MongoDB database so we can migrate Django's ORM (object-relational mapping layer) to MongoDB so we can use the Django admin page to create, read, update, and delete models.</p>
<h5>Hosting the site with NGINX</h5>
<p>First, in <code>website/settings.py</code> change: <code>ALLOWED_HOSTS = ['your-domain', 'www.your-domain']</code>. </p><p>Now to install uWSGI (webserver gateway interface): </p>
<pre>
<code>sudo apt-get install python3.8-dev</code>
<code>sudo apt-get install gcc</code>
<code>pip install uwsgi</code>
<code>sudo apt-get install nginx</code>
</pre>
<p><code>sudo vim /etc/nginx/site-available/"your-domain".conf</code></p>
<pre>
<code># the upstream component nginx needs to connect to
upstream django {
	server unix:///home/ubuntu/website/timelined/website/website.sock;
} 
#configuration of the server
server {
	listen			80;
	server_name		timelined.live, www.timelined.live;
	charset			utf-8;
	# max upload size
	client_max_body_size 75M;
	# Django media and static files
	location /media {
		alias /home/ubuntu/website/timelined/website/media;
	}
	location /static {
		alias /home/ubuntu/website/timelined/website/static;
	}
	# send all non-media requests to Django server
	location / {
		uwsgi_pass	django;
		include		/home/ubuntu/website/timelined/website/uwsgi_params;
	}
}</code></pre>
<p>Now we need to create the <code>uwsgi_params</code> file: </p>
<p><code>vim /home/ubuntu/website/timelined/website/uwsig_params</code> and inside it paste the following: </p>
<pre><code>uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;
uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;
uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
</code></pre>
<p>Now we want to create a symlink to our configuration files: <br>
<code>sudo ln -s /etc/nginx/sites-available/timelined.conf /etc/nginx/sites-enabled/</code></p>
<p>Now in <code>website/settings.py</code>: </p>
<ol>
  <li><code>import os</code></li>
  <li>under <strong>STATIC_URL</strong>: <br>
  <code>STATIC_ROOT = os.path.join(BASE_DIR, "static/")</code></li>
  <li>save the <code>website/settings.py</code></li>
  <li><code>python manage.py collectstatic</code></li>
</ol>
<p>Restart the NGINX server:
<code>sudo /etc/init.d/nginx restart</code></p>
<p>Create a media folder (for user-uploads): 
<code>mkdir media</code></p>
<p>Now to configre NGINX, uWSGI, and Django to communicate: <code>touch timelined_uwsgi.ini</code> and in that file: </p>
<pre><code>[uwsgi]
# full path to Django project's root directory
chdir = /home/ubuntu/website/timelined/website
# Django's wsgi file
module = website.wsgi
# full path to python virtual env
home = /home/ubuntu/env/md
# enable uwsgi master process
master = true
# maximum number of worker processes
processes = 10
# the socket (using full path)
socket = /home/ubuntu/website/timelined/website/website.sock
# socket permissions
chmod-socket = 666
# clear environment on exit
vacuum = true
# daemonize uwsgi and write messages into log
daemonize = /home/ubuntu/uwsgi-emperor.log
</code></pre>
<p>Startup uWSGI: <code>uwsgi --ini timelined_uwsgi.ini</code></p>
<p>Running uWSGI in emperor mode will monitor changes to the configuration files and will spawn vassals (instances) for each one it finds. We can do this by</p>
<ul>
  <li><code>cd /home/ubuntu/env/md</code></li>
  <li><code>mkdir vassals</code></li>
  <li><code>sudo ln -s /home/ubuntu/website/timelined/website/timelined_uwsgi.ini /home/ubuntu/env/md/vassals</code></li>
</ul>
<p>To start uWSGI on system boot create a system service file with <code>sudo vim /etc/systemd/system/emperor.uwsgi.service</code> and inside paste the following: </p>
<pre><code>[Unit]
Description=uwsgi emperor for timelined website
After=network.target
[Service]
User=ubuntu
Restart=always
ExecStart=/home/ubuntu/env/md/bin/uwsgi --emperor /home/ubuntu/env/md/vassals --uid www-data --gid www-data
[Install]
wantedBy=multi-user.target
</code></pre>
<p>And finally, to enable the service and execute it on system boot: </p>
<pre><code>sudo systemctl enable emperor.uwsgi.service
sudo systemctl start emperor.uwsgi.service</code></pre>
<h5>Configuring SSL (HTTPS and HSTS)</h5>
<pre><code>sudo apt install snapd
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx</code></pre>
<p>And in <code>website/settings.py</code> add the following: </p>
<pre><code># HTTPS Settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
# HSTS Settings
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
</code></pre>
</div>

