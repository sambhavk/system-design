# URL Shortener HLD

## Function requirements: 
1) An api should shorten the requested url
2) Requested url should be redirected to the original url
3) Url will be expired after default period or user defined period

## Non Functional requirements:
1) Url redirection should be high availability with eventual consistency
2) Url redirection should be done with min latency to not hamper ux
3) Let's use cassandra for high availability and eventual consistency

## Capacity Estimations
1) Assuming a read heavy system that is more url redirection than url shortening
2) assuming 100:1 ratio
3) suppose 10M url shortening request we get in a month that makes the qps as 10M/30*24*3600 ~ 4 QPS
4) url redirection will be = 1B per month that makes qps ~ 400 QPS
5) suppose each url object takes 500 bytes then a month storage = 10M * 500 = 5 GB per month
6) Following 80-20 rule that is 80% of the traffic comes from 20% of the urls then 80% of months data ~ 4 GB
7) Hot Cache size will be of 4 GB 
8) suppose default expiry is 100 years and if we get 10M req a month then total urls the system should support = 100*10M = 1B urls
9) To support 1B urls and considering only alphanumeric char can be used which are 62 that makes endpoint size ~ 8 char long (n! / (n-k)!)

## Storage design
Cassandra:
1) Table Name - url_manager
2) Schema - (id, original_url, shortened_url, expires_at, created_at, updated_at)

Redis:
1) key - shortened url
2) value - original url
3) default ttl - 100 yrs
4) eviction policy - LRU

## APIs
1) shorten url: 
   > endpoint: /v1/url/shorten POST \
   > req: ```{"original_url": "", "expires_at": "", "user_id": "<uuid>"}``` \
   > resp: ```{"shortened_url": "http://url-shortener/u2y43rks2"}```

2) redirect url:
   > endpoint: /v1/url/u2y43rks2 GET \
   > resp: 302 redirect to original url