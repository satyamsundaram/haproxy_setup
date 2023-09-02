### About
- In this repo, we explore setting up haproxy with 4 backends.
- We implement sleep in the backends and timeout checks in haproxy.
- We implement health checks in haproxy.
- We implement sticky sessions in haproxy using sticky tables.
- We implement ACL-based routing in haproxy based on domain name.
- And, lastly, we implement rate-limiting in haproxy as well.

### Setup
- For the domain name based routing, we need to add the following to `/etc/hosts`:
```bash
127.0.0.1 a.com
127.0.0.1 b.com
```

### Run
```bash
docker-compose up --build
```

- Go to localhost in your incognito tab and watch the load balancing happen in a round robin fashion. 
- You can also go to a.com and b.com to see the domain name based routing where a.com will load balance between web1 and web2 and b.com will load balance between web3 and web4.


### Test
**Testing timeouts:**
To test the timeouts, in the docker-compose.yml, set different timeouts for the backends in the last argument to each of their commands. For example:
```bash
# for web1:
command: python index.py server1 0

# for web1:
command: python index.py server1 2

# for web1:
command: python index.py server1 5

# for web1:
command: python index.py server1 10
```

We have set the timeout server as 5s in our haproxy.cfg. This means that haproxy will wait for 5s to try to connect to a backend server and if it doesn't in 5s, it'll return 502 Bad Gateway. After entering localhost in your incoginito window (to overcome browser caching), you will see the requests to web3 and web4 fail. Yes, web3 will fail because it responds after 5s (not within).

**To test healthchecks:**
Stop one of the backends and you will see that haproxy will stop sending requests to that backend. Start it again and haproxy will start sending requests to it again.

**To test sticky sessions:**
Uncomment the following lines in haproxy.cfg:
```bash
stick-table type ip size 200k expire 30m
stick on src
```
and restart haproxy. Now, go to localhost in your incognito tab and you will see that the requests are sticky. This means that the requests from the same IP will go to the same backend. This is because we have set the stick-table to be based on IP and we have set the stickiness to be based on the source IP.

**To test rate-limiting:**
To test rate-limiting, we have set the rate-limiting to a maximum of 20 requests every 10 seconds. This means that if we send more than 20 requests in 10 seconds, we will get a 429 Too Many Requests error. To test this, we can use the following command:
```bash
for i in {1..30}; do curl localhost; done
```

### Resources
- [timeouts in haproxy](https://thehftguy.com/2016/05/22/configuring-timeouts-in-haproxy/)
- [healthchecks in haproxy](https://thehftguy.com/2016/05/22/configuring-timeouts-in-haproxy/)
- [sticky sessions in haproxy](https://thehftguy.com/2016/05/22/configuring-timeouts-in-haproxy/), [(2)](https://saturncloud.io/blog/haproxy-session-sticky-and-balance-algorithm/)
- [ACL based routing in haproxy using domain-name](https://saturncloud.io/blog/haproxy-session-sticky-and-balance-algorithm/)
- [rate-limiting in HAproxy](https://saturncloud.io/blog/haproxy-session-sticky-and-balance-algorithm/)
  