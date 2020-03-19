# coding: utf-8
"""
logfile
"""

__version__ = "1.0"
__author__  = "liujun.gz@live.com"
__date__    = "2020/3/11"

import re
import logging

logger = logging.getLogger(__name__)

class LogFile(object):
    hostname_pattern = re.compile('')

    def __init__(self, filename=None):
        self.filename = filename
        self.hostname = ''
        self._lines = None
        self.multi_match = False
        self.blocks = []
        
        if filename:
            self.read_logfile(filename)
            self.hostname = self.find_hostname()

    def read_logfile(self, filename):
        """read the log lines from log file.
        NOTICE: large file should be considered.
        """
        try:
            with open(filename) as fp:
                self._lines = fp.readlines()
        except Exception as err:
            print(f"Can't open logfile: {filename}. msg:{err}")

    
    def load_lines(self, lines):
        self._lines = lines
        
    def find_hostname(self):
        """find the hostname in the log file. return the hostname or 'unknown'
        """
        raise NotImplementedError

    def _select_lines(self, selector):
        """select the lines which filtered by selector.
        selector is a class of `BlockFilter`
        
        """
        selected = []
        for line in self._lines:
            start, end = selector.check(line)
            #logger.debug(f"line:{[line]}, {start}, {end}")
            if start:
                selected.append(line)
                continue
            if end and not self.multi_match:
                selected.append(line)
                return selected
            
        return selected

    def filter_blocks(self, selector):
        """filtering multi blocks which have same structure selected by selector.
        selector is a class of `BlockFilter`
        
        """
        blocks = []
        selected = []
        for line in self._lines:
            start, end = selector.check(line)
            #logger.debug(f"line:{[line]}, {start}, {end}")
            if start:
                selected.append(line)
                continue
            if end:
                selected.append(line)
                blocks.append(selected)
                selected = []
                
                
        return blocks
        
    def _filter_block(self, filter_list):
        """filter the log blocks using the 'ilter_list` 
        
        params: 
            filter_list,  a list including some `BlockFilter` classes
        
        return:
            a list including some log lines blocks.
        """
        blocks = []
        for blk_filter in filter_list:
            
            blocks.append(self._select_lines(blk_filter))
        
        self.blocks = blocks
        return blocks

    def filter_lines(self, filter_list):
        _lines = []
        for _filter in filter_list:
            _filter.reset() # the filter might had been used many times.
            _lines.extend(self._select_lines(_filter))

        return _lines
        
        
        
class BlockFilter(object):
    start_parttern = re.compile('')
    end_pattern = re.compile('')
    multi_match = False
    
    def __init__(self, multi_match=False):
        #self.multi_match = multi_match
        self.start = False
        self.end = False
        
    def check(self, line):
        """
        """
        if self.start:
            if self.end_pattern.match(line):
                logger.debug("--- end line found! closed")
                self.start = False
                self.end = True
                # if self.multi_match:
                    # self.end = False
                # else:
                    # self.end = True

        elif self.start_pattern.match(line):
            self.start = True
            logger.debug('--- start line found!')
        else:
            self.end = False

        return self.start, self.end

    def reset(self):
        self.start = False
        self.end = False
