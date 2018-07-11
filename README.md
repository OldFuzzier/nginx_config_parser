# Nginx Config Transfer

### basic structure
1. n-node tree
2. SpecialNode: base n-node tree

### nginx.confg ---> n-node tree structure

1. nginx.confg ---> in_list `[list[list]]`
2. in_list ---> n-node tree
3. n-node tree ---> n-node tree after prune

### access way
`bn_obj.http.server.error_page` res: `LIST [404, 500 502 503 504]`
`bn_obj.http.server.error_page[1]` res: `STRING /50x.html;`
`bn_obj.http.server.location[2]` res: `DICT: ['index', 'root']`
`bn_obj.http.server.location[2].index` res: `STRING 404.html;`