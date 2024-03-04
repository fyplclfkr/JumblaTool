# coding:utf-8
import six, sys
if six.PY3:
    basestring = (str, bytes)
else:
    basestring=basestring
    
def to_unicode(s):
    if isinstance(s, six.binary_type):
        return s.decode('utf-8')
    return s
    
def to_syscode(s):
    """将unicode转为系统编码, 一般用于cmd执行的时候使用"""
    if isinstance(s, six.text_type):
        encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
        return s.encode(encoding, 'replace')
    return s    