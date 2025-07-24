# URL Shortener HLD

## Function requirements: 
1) An api should shorten the requested url
2) Requested url should be redirected to the original url
3) Url will be expired after default period or user defined period

## Non Functional requirements:
1) System should support 1B urls for shortening
    a) url consist of alphanumeric char which is 62 in total
    b) to support 1B combinations, a string length of 8 is required
2) Url redirection should support sub millisecond latency under a heavy load of 10k QPS
3) Url redirection should be high availability with eventual consistency
4) System should support 100M req a day
5) Lets use cassandra for high availability and eventual consistency