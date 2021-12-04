### SJTU EE208 Proj
**Final projects for SJTU EE208 final projects**
---
#### Crawler and data formats
We assume that all components related to web crawler are contained in the crawler/ directory.
Since we have to build different crawlers for different websites, in the crawler/ directory
one can see three directories representing crawler's target website. For example, crawler/jd/
represents JD.com.

Crawlers are always under the crawler/(name of target)/ directory and are named crawler.py,
and their outputs are placed in a folder named ./html/ (crawler/(name of target)/html/), you'd
better use absolute path in case your IDE select some different working directory for you.

The url information are placed inside ./html/index.txt, you can refer to the example inside
crawler/jd/html/index.txt for data and commenting infromations.

