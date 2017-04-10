#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import cherrypy

import feed

class FlaskApplication(object):
    HOST = "127.0.0.1"
    PORT = 5000

    def run(self):
        cherrypy.config.update({
            'environment': 'production',
            'server.socket_host': self.HOST,
            'server.socket_port': self.PORT,
            'engine.autoreload_on': False,
            'log.error_file': 'site.log',
            'log.screen': True
        })

        cherrypy.log("Loading and serving Flask application")
        cherrypy.tree.graft(feed.app, '/')
        cherrypy.engine.start()
        cherrypy.log("Your app is running at http://%s:%s" % (self.HOST, self.PORT))

        cherrypy.engine.block()


if __name__ == "__main__":
    FlaskApplication().run()
