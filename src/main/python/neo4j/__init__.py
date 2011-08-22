# -*- mode: Python; coding: utf-8 -*-

# Copyright (c) 2002-2011 "Neo Technology,"
# Network Engine for Objects in Lund AB [http://neotechnology.com]
#
# This file is part of Neo4j.
#
# Neo4j is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Python bindings for the embedded Neo4j Graph Database.
"""

__all__ = 'GraphDatabase', 'Node', 'Relationship',\
          'Property', 'In', 'Out', 'Any'

from neo4j._backend import GraphDatabase

class Nodes(object):
    
    def __init__(self, db):
      self.db = db
    
    def __call__(self, **properties):
        node = self.db.createNode()
        for key, val in properties.items():
            node[key] = val
        return node
        
    def __getitem__(self, items):
        if not isinstance(items, (int, long)):
            raise TypeError("Only integer and long values allowed to lookup node ids.")
            
        self.db.getNodeById( items )
        

class GraphDatabase(GraphDatabase):
    from neo4j._backend import __new__

    try:
        from contextlib import contextmanager
    except:
        pass
    else:
        ## yield in try is a recent feature in Python,
        ## guard with exec to support old versions of Python
        ## This should pass since import contextlib has worked
        exec('''def transaction(self):
        """Allows usage of the with-statement for Neo4j transactions:
        with graphdb.transaction:
            doMutatingOperations()
        """
        tx = self.beginTx()
        try:
            yield tx
            tx.success()
        finally:
            tx.finish()
''')
        transaction = property(contextmanager(transaction))
        del contextmanager # from the body of this class

    @property
    def node(self):
        if not hasattr(self, '_node'):
            self._node = Nodes(self)
        return self._node

