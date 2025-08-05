Social media hld

functional requirements: 
1) usbat follow users and see who follows him
2) usbat see a feed posted by his followed people 
3) usbat post nested comments on a post

non functional requirements:
1) system should be highly available
2) feed latency should be very low. no loading screen

capacity estimations:
1) 100:1 read write ratio
2) the system gets 1B post per month which makes write qps for post ~ 1B/30*24*3600 = 400 qps
3) as per this reads per month will be 100B that makes the qps to be ~ 40k qps
4) the system has a hard limit of 15 MB per post then monthly storage required would be = 1B * 15MB = 15 PB and yearly = 15*12 = 330 PB
5) each post can have 10 avg number of comments and each comment corresponds to 100 bytes = 1B * 10 * 100 = 1T bytes = 1 TB per month

Storage requirements:
1) System is highly avaialble so HA with eventual consistency
2) photo file would be stores in s3 exposed via CDNs
3) user profiling data (user name, bio, email, user posts) will be stored in documents in mongodb
4) for nested comments neo4j will be used as it supports o(1) for insertion, update, deletion and fetch of comments wrt a post
5) 