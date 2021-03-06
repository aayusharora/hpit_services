import os
import unittest
from mock import *
import sure

from hpit.management.entity_manager import EntityManager

class TestBaseManager(unittest.TestCase):

    def setUp(self):
        self.subject = EntityManager()

        self.configuration = {
            'plugins': ['A', 'B', 'C'],
            'tutors': ['D', 'E', 'F']
        }

    def test_constructor(self):
        """
        BaseManager.__init__() Test plan:
            - make sure settings set
            - make sure app_instance set
        """
        self.subject.settings.should_not.be.none
        self.subject.app_instance.should_not.be.none


    def test_read_configuration_no_file(self):
        m = mock_open(mock=Mock(side_effect=FileNotFoundError()))

        with patch('hpit.management.entity_manager.open', m, create=True):
            result = self.subject.read_configuration()
            result.should.equal({})


    def test_read_configuration_bad_file(self):
        m = mock_open(read_data='{...')

        with patch('hpit.management.entity_manager.open', m, create=True):
            self.subject.read_configuration.when.called_with().should.throw(ValueError)


    def test_read_configuration_good_file(self):
        m = mock_open(read_data='{"plugins": ["A", "B", "C"]}')

        with patch('hpit.management.entity_manager.open', m, create=True):
            result = self.subject.read_configuration()
            result.should.equal({'plugins': ['A', 'B', 'C']})


    def test_write_configuration(self):
        m = mock_open()

        with patch('hpit.management.entity_manager.open', m, create=True):
            self.subject.write_configuration({'plugins': ['A', 'B', 'C']})

        handle = m()
        handle.write.assert_called_one_with('{"plugins": ["A", "B", "C"]}')


    def test_build_sub_commands(self):
        pass


    def test_build_argument_parser(self):
        pass


    def test_run_manager(self):
        pass


