#
# coding=utf-8

import re


# tree structure
class Node(object):

    def __init__(self, val, children):
        self.val = val
        self.children = children

    def __repr__(self):
        return '{val} --> {children}'.format(val=self.val, children=self.children)


# solve file change to in_list
class Solution(object):

    # change list to in_list by backtracking(core_method)
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
    def toStructure(self, filename):
        lst = self.read_file(filename)
        in_list = self.backTracking(lst, {'i': 0}, [])
        return in_list


class BulidNode(object):

    # build n-node tree(core method)
    def build(self, lst):
        '''
        :param lst:  嵌套list
        :return: root(n-node)
        '''
        root = Node('nginx', {})  # set root
        def dfs(root, lst):  # dfs travel
            for ele in lst:
                if isinstance(ele, list):
                    index_line = ele[0].find('{')
                    key = ele[0][:index_line].strip()
                    n = Node(key, {})
                    dfs(n, ele[1:-1])  # recursive dfs
                    # print 'debug'

                else:
                    line_temp = ele.split()
                    key, value = line_temp[0], line_temp[1]
                    n = Node(key, value)

                root.children[n.val] = n
        dfs(root, lst)
        return root

    def travel(self):
        pass

    def loads(self, filename):
        '''
        :return: n-node
        '''
        in_list = Solution().toStructure(filename)
        root = self.build(in_list)
        return root

    def dumps(self):
        pass

if __name__ == '__main__':
    # test
    # lst = Solution().main('nginx.conf')
    # print lst
    # BulidNode().build(lst).children['http'].children['server'].children['location /'].children
    print BulidNode().loads('nginx.conf').children['http'].children['server'].children['location /'].children

