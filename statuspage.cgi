#!/usr/bin/env python3

from wsgiref.handlers import CGIHandler
from statuspage import app

CGIHandler().run(app)
