# Nginx Config Transfer

## Basic Structure
1. n-node tree
2. SpecialNode: base n-node tree

## Raw File to Data Structure

### nginx.confg ---> n-node tree structure

1. nginx.confg ---> in_list `[list[list]]`
2. in_list ---> n-node tree
3. n-node tree ---> n-node tree after prune

### access way (python env)
* `nginx_obj = BulidNode().load('nginx.conf')`
* `nginx_obj.http.server.error_page` res: `LIST: [404, 500 502 503 504]`
* `nginx_obj.http.server.error_page[1]` res: `STRING: /50x.html;`
* `nginx_obj.http.server.location[2]` res: `DICT: ['index', 'root']`
* `nginx_obj.http.server.location[2].index` res: `STRING: 404.html;`

## Data Structure to Raw File