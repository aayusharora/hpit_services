import sure
import responses
import unittest
from mock import *

from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId

from couchbase import Couchbase
import couchbase

from plugins import SkillManagementPlugin

class TestSkillManagementPlugin(unittest.TestCase):

    def setUp(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.test_subject = SkillManagementPlugin(123,456,None)
        self.test_subject.db = self.test_subject.mongo.test_hpit.hpit_skills
       
    def tearDown(self):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        client = MongoClient()
        client.drop_database("test_hpit")
        
        self.test_subject = None


    def test_constructor(self):
        """
        SkillManagementPlugin.__init__() Test plan:
            -ensure name, logger set as parameters
            -ensure that mongo is an instance of mongo client
            -ensure that a cache db is set up
        """
        test_subject = SkillManagementPlugin(123,456,None)
        test_subject.logger.should.equal(None)
        
        isinstance(test_subject.mongo,MongoClient).should.equal(True)
        isinstance(test_subject.db,Collection).should.equal(True)
        
        isinstance(test_subject.cache,couchbase.connection.Connection).should.equal(True)


    def test_get_skill_name_callback(self):
        """
        SkillManagementPlugin.get_skill_name_callback() Test plan:
            - pass in message without id, should respond with error
            - pass in message with bogus id, should respond with error
            - pass in message with good id, should respond with name
        """
        self.test_subject.send_response = MagicMock()

        msg = {"message_id":"1"}
        self.test_subject.get_skill_name_callback(msg)
        self.test_subject.send_response.assert_called_with("1",{
                "error":"Message must contain a 'skill_id'",
        })
        self.test_subject.send_response.reset_mock()
        
        bogus_id = ObjectId()
        msg["skill_id"] = bogus_id 
        self.test_subject.get_skill_name_callback(msg)
        self.test_subject.send_response.assert_called_with("1",{
                "error":"Skill with id " + str(bogus_id) + " does not exist."      
        })
        self.test_subject.send_response.reset_mock()
        
        real_id = self.test_subject.db.insert({"skill_name":"addition"})
        msg["skill_id"] = real_id
        self.test_subject.get_skill_name_callback(msg)
        self.test_subject.send_response.assert_called_with("1",{
                "skill_name":"addition",
                "skill_id": str(real_id),
        })
        self.test_subject.send_response.reset_mock()
        
    
    def test_get_skill_id_callback(self):
        """
        SkillManagementPlugin.get_skill_id_callback() Test plan:
            - pass in message without name, should respond with error
            - pass in message with name for non existent, should create one
            - pass in message with existing name, should return proper id
        """
        self.test_subject.send_response = MagicMock()
        
        msg = {"message_id":"1"}
        self.test_subject.get_skill_id_callback(msg)
        self.test_subject.send_response.assert_called_with("1",{
                "error":"Message must contain a 'skill_name'",
        })
        self.test_subject.send_response.reset_mock()
        
        msg["skill_name"] = "addition"
        self.test_subject.get_skill_id_callback(msg)
        self.test_subject.db.find({"skill_name":"addition"}).count().should.equal(1)
        added_id = self.test_subject.db.find_one({"skill_name":"addition"})["_id"]
        
        self.test_subject.get_skill_id_callback(msg)
        self.test_subject.send_response.assert_called_with("1",{
                "skill_name":"addition",
                "skill_id":str(added_id),
        })
        
        
        
