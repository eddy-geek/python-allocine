#  AllocineApi.py
#  
#  Copyright 2012 Cilyan Olowen <gaknar@gmail.com>
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  

try:
  # Python3
  from urllib.request import urlopen as url_urlopen
  from urllib.parse import urlencode as url_urlencode, quote
except ImportError:
  # Python2
  from urllib2 import urlopen as url_urlopen, quote
  from urllib import urlencode as url_urlencode

from base64 import b64encode
from datetime import datetime
from hashlib import sha1
import logging

from .settings import *
logger = logging.getLogger(__name__)

# Parameters for Allocine API v3
VERSION=3
BASE_URL = "http://api.allocine.fr/rest/v3/{action}?{params}"
ALLOCINE_ENCODING = "utf-8"

class AllocineQuery(object):
  
  def __init__(self, reply_format="xml", profile="large"):
    # Validate reply_format (key "format")
    if reply_format not in ["xml", "json"]:
      raise ValueError("reply_format is either 'xml' or 'json'")
    self.reply_format = reply_format
    # Validate profile (key "profile")
    if profile not in ["large", "medium", "small"]:
      raise ValueError("profile is either 'large', 'medium' or 'small'")
    self.profile = profile
  
  def query(self, action, **args):
    args.update({
      "partner": PARTNER_CODE,
      "format": self.reply_format,
      "sed": datetime.now().strftime('%Y%m%d')
    })
    params = url_urlencode(args)
    sig = quote(b64encode(sha1((action + params + ALLOCINE_SECRET_KEY).encode()).digest()), safe='+')
    url = BASE_URL.format(action=action, params=params + "&sig=" + sig)
    logger.info("GET %s", url)
    result = url_urlopen(url).read()
    return result.decode(ALLOCINE_ENCODING)
  
  def search(self, keywords, **args):
    """
      accepts:
        "filter", "count"
    """
    args["q"] = keywords
    return self.query("search", **args)
  
  def query_movie(self, code, **args):
    """
      accepts:
        "filter", "mediafmt", "striptags"
    """
    args["code"] = code
    args["profile"] = self.profile
    return self.query("movie", **args)
  
  def query_person(self, code, **args):
    """
      accepts:
        "filter", "mediafmt", "striptags"
    """
    args["code"] = code
    args["profile"] = self.profile
    return self.query("person", **args)
  
  def query_reviewlist(self, code, **args):
    """
      accepts:
        "filter", "count", "page", "type"
    """
    args["code"] = code
    return self.query("reviewlist", **args)
  
  def query_filmography(self, code, **args):
    """
      accepts:
        "filter"
    """
    args["code"] = code
    return self.query("filmography", **args)
