__version__ = '1.0.0'

from requests.structures import CaseInsensitiveDict
from .client import OssConfig, OssClient
from .exceptions import ClientError, ServerError
from .compat import to_bytes, to_string, to_unicode, urlparse, urlquote, urlunquote
