#
# coding=utf-8

import re


# solve file change to in_list and string problem
class Solution(object):

    item_set = {'error_page'}

    # change list to in_list by backtracking(core method)
    def backTracking(self, lst, i_dict, temp):
        '''
        :param lst: list
        :param i_dict: record index, default: i=0, need use variable structure to store then use Dict
        :param temp: temp list, default: temp=[], backTracking part
        :return: 嵌套字典(in_list)
        '''
        while i_dict['i'] < len(lst):
            # temp_dict = {}
            ele = lst[i_dict['i']]
            if ele.find('}') != -1:
                temp.append(ele)
                return temp
            if ele.find('{') != -1:
                i_dict['i'] += 1  # because add "{" so need +=1
                temp.append(self.backTracking(lst, i_dict, [ele]))  # back tracking == push [ele] and pop [ele]
            else:
                temp.append(ele)
            i_dict['i'] += 1
        return temp

    # 读取raw文件，去除空行和换行等，最后转换为list
    def read_file(self, config_path):
        '''
        :param config_path: file_name
        :return: list
        '''
        with open(config_path, 'rb') as f:
            file_list = f.readlines()
        temp_list = [line.strip() for line in file_list if re.search(r'\S+?', line)]
        # debug:
        # for line in temp_list:
        #     print line
        return temp_list

    # combine read_file and backtracking methods
    def to_inlist(self, filename):
        lst = self.read_file(filename)
        in_list = self.backTracking(lst, {'i': 0}, [])
        return in_list

    # self-bulid a match space method  分割两个空号的方法
    # def match_space(self, s):
    #     pattern = '  '
    #     res_list = []
    #     i = 0
    #     while i < len(s)-1:
    #         if s[i] == pattern[0] and s[i+1] == pattern[1]:
    #             res_list.append(s[:i].strip())
    #             res_list.append(s[i+1:].strip())
    #             break
    #         else:
    #             i += 1
    #     else:  # have not value
    #         res_list.append(s)
    #         res_list.append(' ')
    #     return res_list[0], res_list[1]

    # self-bulid a match space method, 可扩展
    def match_space(self, s):
        key_temp = s.split()
        key_first = key_temp[0]
        if key_first in self.item_set:
            key = ' '.join(key_temp[:-1])
            value = key_temp[-1]
            return [key, value]
        else:
            return key_temp


# n-node-tree + container structure
class Node(object):

    def __init__(self, val, children=None):
        self.val = val  # string
        self.children = children  # Node or dict

    # user interface
    def __str__(self):
        ele = self.children
        if isinstance(self.children, dict):
            return 'DICT: {ele}'.format(ele=str(self.children.keys()))
        elif isinstance(self.children, list):
            return 'LIST: {ele}'.format(ele=str(self.children))
        else:  # string
            return 'STRING: {ele}'.format(ele=ele.val)

    # debug
    def __repr__(self):
        return '{val}'.format(val=self.val)
        # return '{val} --> {children}'.format(val=self.val, children=self.children)

    # isinstance(self.children, dict) execute this method
    def __getattr__(self, item):
        child = self.children[item]
        return child

    # if isinstance(self.children, list) execute this method
    def __getitem__(self, item):
        child = self.children[item]
        return child

    # def collectChild(self, item):
    #     '''
    #     :param item: string
    #     :return: list
    #     '''
    #     child_list = [ele for ele in self.children.keys() if ele.split(' ')[0] == item[:-1]]
    #     return child_list


class SpecialNode(Node):
    # Include: location, error_page, ...

    def __init__(self, special_val, children):
        '''
        :param special_val: string
        :param children: list
        '''
        super(SpecialNode, self).__init__(special_val, children)  # children: List


class BulidNode(object):

    def __init__(self):
        self.solve = Solution()  # offer string support
        self.item_set = {'location', 'upstream', 'error_page'}  # special item

    # build n-node tree(core method)
    def build(self, in_list):
        '''
        :param in_list:  嵌套list
        :return: root(n-node)
        '''
        root = Node('nginx', {})  # set root

        def dfs(root, lst):  # dfs travel
            for ele in lst:
                if isinstance(ele, list):
                    index_line = ele[0].find('{')  # ele[0]: "location /publishManage  {"
                    key = ele[0][:index_line].strip()  # key: "location /publishManage"
                    n = Node(key, {})
                    dfs(n, ele[1:-1])  # recursive dfs
                    # print 'debug'
                else:
                    ele_temp = self.solve.match_space(ele)
                    key, value = ele_temp[0], Node(' '.join(ele_temp[1:]))  # ['error_page', '500 /50x.html']
                    n = Node(key, value)
                root.children[n.val] = n

        dfs(root, in_list)
        return root

    # take pruning to tree(core method)
    def prune(self, root):
        '''
        :param root: n-node-tree structure
        :return: None
        '''
        # init {item: SpecialNode,...} 可优化 item_dict.clear()
        item_dict = {}
        for item in self.item_set:
            item_dict[item] = SpecialNode(item, [])

        def bfs(root):  # bfs travel
            queue = [root]
            while queue:
                for _ in xrange(len(queue)):
                    root = queue.pop(0)
                    children = root.children  # Node or dict
                    if isinstance(children, dict):
                        queue.extend(children.values())  # queue add

                        for child_name in children.keys():  # prune part
                            key_temp = children[child_name].val.split()  # ["location",  "/publishManage"]
                            key_first = key_temp[0]  # "location"
                            if key_first in item_dict:
                                if not children.get(key_first):  # 如果还没有SpecialNode，需要新建
                                    # print key_first
                                    children[key_first] = item_dict[key_first]  # new build SpecialNode(key_first, [])
                                child = children.pop(child_name)  # prune
                                key_other = ' '.join(key_temp[1:])  # "/publishManage"
                                child.val = key_other  # update child.val
                                # print child.val, child.children
                                children[key_first].children.append(child)  # SpecialNode.children.append(node)
                    else:  # children(Node)
                        pass

        bfs(root)
        item_dict.clear()  # clear dict
        return

    # combine build and pruning
    def build_tree(self, in_list):
        root = self.build(in_list)
        self.prune(root)
        return root

    def travel(self):
        pass

    def load(self, filename):
        '''
        :return: n-node
        '''
        in_list = self.solve.to_inlist(filename)
        root = self.build_tree(in_list)
        # root = self.build(in_list)  # test build
        return root

    def dump(self, in_list, filename):
        '''
        :param in_list: 嵌套list
        :return: None
        '''
        pass


if __name__ == '__main__':
    nginx_obj = BulidNode().load('nginx.conf')
