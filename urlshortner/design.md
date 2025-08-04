# URL Shortener HLD

## Function requirements:
1) An api should shorten the requested url
2) Requested url should be redirected to the original url
3) Url will be expired after default period or user defined period

## Non Functional requirements:
1) Url redirection should be high availability with eventual consistency
2) Url redirection should be done with min latency to not hamper ux
3) Url shortened should not be duplicate

## Capacity Estimations
1) Assuming a read heavy system that is more url redirection than url shortening
2) assuming 100:1 ratio
3) suppose 100M url shortening request we get in a month that makes the qps as 100M/30*24*3600 ~ 40 QPS
4) url redirection will be = 10B per month that makes qps ~ 4000 QPS
5) suppose each url object takes 500 bytes then a month storage = 100M * 500 = 50 GB per month
6) Following 80-20 rule that is 80% of the traffic comes from 20% of the urls then 20% of months data ~ 40 GB
7) Hot Cache size will be of 40 GB
8) suppose default expiry is 100 years and if we get 100M req a month then total urls the system should support = 100*12*100M = 120B urls
9) To support 120B urls and considering only alphanumeric char can be used which are 62 that makes endpoint size ~ 7 char long (62^7)

## Storage design
1) url shortening should be unique and hence multiple write nodes are not possible
2) so we can choose a sql db such as postgres
3) how to make writes faster with single write node?
4) we can add data partitioning but that will only make the query run faster and not give horizontal scaling
5) what if we did sharding based on char. so we have 62 char in total so if we divide it into 4 shards and add consistent hashing
for routing access and insert req to this cluster then we can get horizontal scaling and it will make writes faster
6) for reading we can add a redis cache. but read through cache or write through?
7) if we choose WTC then multiple redis nodes are not possible as that will again lead to inconsistency of shortened endpoint hashes.
8) we can choose RTC which will allow scaling the caching layer horizontally and for every cache miss we can call db
9) also we can use LRU as the eviction policy
10) but how to handle race condition while shortening url? if 2 urls shortened hashes are inserting to db at the same time then which one will be inserted?
11) we cannot lock the row as there is no data yet. but we can create hashes preemptively and add those to db.
12) because the hash is already present in the table now both req can use locking

> Postgres sharded nodes for fast writes with consistent hashing to route the req to right node
> Redis cache for fast reads using read through cache with LRU as eviction policy

Postgres table:
1) url_metadata
Schema - id(PK), original_url, shortened_url, user_id, expires_at, created_at
user_id and shortened_url = unique constraint as different users can add same url to be shortened
shortened_url = unique constraint as preemptive generation will not have user_id then

## APIs
1) shorten url:
   > endpoint: /v1/url/shorten POST \
   > req: ```{"original_url": "", "expires_at": "", "user_id": "<uuid>"}``` \
   > resp: ```{"shortened_url": "http://url-shortener/u2y43rks2"}```

2) redirect url:
   > endpoint: /v1/url/u2y43rks2 GET \
   > resp: 302 redirect to original url
