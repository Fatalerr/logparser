# coding: utf-8

__version__ = "1.0"
__author__  = "liujun.gz@live.com"
__date__    = "2020/3/11"

class LogParser(object):
    """文本log分析器
    本分析器根据输入的分析器列表，从log文件中提取出对应的数据，并计算基本的统计数据
    Usage:
     parser = LogParser('cmg_config_file')
     parser.parse(parser_list)

     parser.stats
     parser.data

    """
    def __init__(self, rules=None, logfile=None):
        self.filename = logfile
        self._rules = rules
        self.lines = None
        self._data = {}

        if logfile:
            if isinstance(logfile, list):
                self.load_from_list(logfile)
            else:
                self.load_from_file(logfile)

    def load_from_file(self, filename=None):
        """load log content from file.
        """
        try:
            with open(filename) as fp:
                self.lines = fp.readlines()
        except IOError as err:
            print(f"Can't open config file: {filename}\n{err}")
            exit(1)

    def load_from_list(self, lines):
        """load the log content from the list
        """
        self.lines = lines

    def load_rules(self, rules):
        self._rules = rules

    @property   
    def stats(self):
        stats = {}
        for key, values in self._data.items():
            stats[key] = len(values)

        return stats

    @property
    def data(self):
        return self._data
    
    def parse(self, lines):
        """parse the lines with the loaded/preset rules
        """
        self._data = {}
        
        for rule in self._rules:
            #print(rule.name, rule.re_pattern)
            data = rule.parse(lines)
            self._data[rule.name] = data

        return self._data