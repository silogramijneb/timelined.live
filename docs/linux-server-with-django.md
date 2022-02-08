<h3>Linux Server and Django Setup</h3>

<p>Here is a brief guide I wrote to anyone interested in how to setup a webserver on a raspberry pi, and then host a Django website off of it. Since this pi is connected to my home network, for security reasons I will not be sharing SSH credentials. However, once we are closer to the project deadline, I will migrate all of our work to a virtual machine on Google Cloud Platform (GCP) which you will be able to access. These instructions will be basically identical to hosting on a Linux VM in GCP, with a few tweaks.</p><p>
  ---------------------------------------------------------------------------------------------------------------
</p>

<h5>Raspberry Pi Specifications</h5>

<ul><li>OS: Ubuntu Server 20.04.3 LTS (aarch64)</li>
  <li>Model: Raspberry Pi 4 Model B</li>
  <li>CPU: BCM2835 (4) @ 1.5GHz</li>
  <li>Memory: 2GB</li>
  <li>Kernel: 5.4.0-1048-raspi</li>
  <li>Shell: bash 5.0.17</li></ul>
<p>
  ---------------------------------------------------------------------------------------------------------------
</p>

<h5>Pi Base Setup</h5>

<ol><li>Download latest LTS (Long Time Support) Ubuntu Server from <a>https://ubuntu.com/download/server</a></li>
  <li>Burn .iso to Raspberry Pi SD Card (I recommend using <a href="https://www.balena.io/etcher/">balenaEtcher</a>)</li>
  <li>Connect Raspberry Pi to monitor, keyboard, and power</li>
  <li>Follow on-screen installation instructions</li>
  <li><code>sudo apt update</code></li>
  <li><code>sudo apt upgrade -y</code></li></ol>
<p>
  ---------------------------------------------------------------------------------------------------------------
</p>

<h5>Linux Setup</h5>

<p>For basic Linux commands and setup <a href="https://docs.google.com/document/d/1qGtuQAEwh_IZSLRGaSSuc97JLEZK2ms-HcEEswflReg/edit?usp=sharing">check out this document.</a> To use Linux you should also be familiar with either <a href="https://www.nano-editor.org/">Nano</a> or <a href="https://vim.org/">Vim</a>. I recommend learning Vim because it is installed on almost every Linux OS and it is lightweight, fast, and very powerful. The best way to learn Vim is to run vim: <code>vim</code> and enter <code>:help</code></p>

<h6>Creating a Swapfile</h6>

<pre>
<code>sudo fallocate -l 4GB /swapfile</code>
<code>sudo dd if=/dev/zero of=/swapfile bs=1024 count=1048576</code>
<code>sudo chmod 600 /swapfile</code>
<code>sudo mkswap /swapfile</code>
<code>sudo swapon /swapfile/code>
<code>sudo vim /etc/fstab:</code>
	<code>/swapfile swap swap defaults 0 0</code>
<code>sudo mount -a</code>
</pre>

<p>A swapfile essentially allows the Linux operating system to use the system disk (HDD or SSD) as virtual RAM when its available memory is running low. Read more about swapfiles <a href="https://averagelinuxuser.com/linux-swap/">here</a>. For our Raspberry Pi with only 2GB of RAM, it is pretty much essential.</p>

<h6>Editing SSH configuration</h6>

<code>sudo vim /etc/ssh/sshd_config</code>

<p>Uncomment these lines ... </p>

<pre>
<code># Authentication
	LoginGraceTime 2m
	PermitRootLogin prohibit-password
	StrictModes yes
	MaxAuthTries 6
	MaxSessions 10

PrintMotD yes<
PrintLastLog yes</code>
</pre>

<p>This will make all SSH connections to the server more secure and prevent different types of attacks through SSH.</p>

<h6>Firewall Configuration</h6>

<p>By default, UFW (Uncomplicated Firewall) should be installed on the system, if it is not, install it with <code>sudo apt install ufw</code></p>

<p><a href="https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-20-04">This link</a> will provide you with the basics of configuring the firewall. By default, ufw will <code>sudo ufw default deny incoming</code> and <code>sudo ufw default allow outgoing</code>, which is all we need for now. To enable SSH outside of your local network you need to add an "A" record pointing to the raspberry pi's local IP Address in your Router Firewall > Port Forwarding Settings (which you can access by going to <a>192.168.1.1</a> in your browser).</p>

<p>The completed Rule should look something like this: </p>

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

<p>You can then add the rule to ufw with the command <code>sudo ufw allow ssh</code> and then enabling ufw with <code>sudo ufw enable</code>. You can reboot your pi with <code>sudo reboot</code> and try to SSH into it to test everything is working. We will have to add some more rules once the webserver is live to allow people to access it through the domain <a>timelined.live</a> which will be shown in a later section.</p>
<p>
  ---------------------------------------------------------------------------------------------------------------
</p>

<h5>Django Installation</h5>

<p>Use pip to install Django with <code>pip3 install django</code>. Now in your <code>~/home</code> directory, create a new folder with the <code>mkdir "folder-name"</code> command. <code>cd "folder-name"</code> and run <code>django-admin startproject "project-name"</code>. In our case, the Django files will live in the "website" folder.<p>

<h6>Django Setup - LOCALHOST NOT MEANT FOR PRODUCTION</h6>

<p>Since I am SSH'd into my Raspberry Pi from my laptop, running the development server won't allow me to view it locally on my web browser. To get around this (for now): <ol>
  <li><code>curl ifconfig.me</code> to get <strong>YOUR-PUBLIC-IP</strong></li>
  <li><code>website/website/settings.py</code> ALLOWED_HOSTS = [ <strong>YOUR-PUBLIC-IP</strong> ]</li>
  <li><code>cd ..</code> (back to previous directory)</li>
  <li>run <code>python3 manage.py runserver 0:8000</code></li>
</ol><p>You should be able to access the live site by visiting <strong>YOUR-PUBLIC-IP</strong>:8000 in your web browser.</p>

<h6>Database (MongoDB) Setup</h6>

<p>For this website we will be using <a href="https://www.mongodb.com/">MongoDB</a> as our backend database. To install it on the Raspberry Pi follow <a href="https://www.mongodb.com/developer/how-to/mongodb-on-raspberry-pi/">these instructions</a>. If you get a <strong>mongod.service: Failed with result 'core-dump'</strong> error, follow <a href='https://stackoverflow.com/questions/68937131/illegal-instruction-core-dumped-mongodb-ubuntu-20-04-lts'>these instructions</a> to reinstall.

<ol>
  <li><code>pip3 install djongo</code></li>
  <li><code>pip3 install mongoengine</code></li>
  <li>From instructions above get your databse <strong>USERNAME</strong> and <strong>PASSWORD</strong></li>
  <li><code>mongo -u <strong>USERNAME</strong> -p <strong>PASSWORD</strong></code></li><ul>
  <li><code>use <strong>DATABASE_NAME</strong></code></li>
	<li><code>db.test.insert({name:"test", value: 1})</code></li>
  <li><code>exit</code></li></ul>
  <li>In <code>website/settings.py</code> change:
 	<code><pre>DATABASES = {
    	'default': {
    		'ENGINE': 'djongo',
    		'NAME': <strong>'DATABASE_NAME'</strong>,
    		'CLIENT': {
    			'username': <strong>'USERNAME'</strong>,
    			'password': <strong>'PASSWORD'</strong>,
    		}
    	}
}</pre></code></li>
	<li><code>python3 manage.py makemigrations</code></li>
  <li><code>python3 manage.py migrate</code></li>
</ol>

<p>The following commands created a "test" table in our MongoDB database so we could migrate Django's ORM (object-relational mapping layer) to MongoDB so we can use the admin page to create, read, update, delete models.</p>

<h6>Hosting the site with NGINX</h6>

<p>TODO</p>
<p>
  ---------------------------------------------------------------------------------------------------------------
</p>

<h5>Github Collaboration</h5>

<p>It is important to understand how Github works and how we can use it to work on this project. Since I have added you as a collaborator, this means that you have the ability to push, pull, merge, and make dangerous changes to the repository. Please read <a href="https://medium.com/@jonathanmines/the-ultimate-github-collaboration-guide-df816e98fb67">this article</a> on how to correctly use Github in a collaborative setting so we can all be on the same page for when we start developing the site.</p>



