from hpitclient import Tutor
from hpitclient.settings import HpitClientSettings
import logging
import os
import time
import argparse

class DataShopConnectorTutor(Tutor):
    
    def __init__(self,entity_id,api_key,logger,run_once = None, args = None):
        super().__init__(entity_id, api_key, self.main_callback, run_once=run_once)
        self.run_once = run_once
        self.logger = logger
        
        if args: 
            self.args = json.loads(args[1:-1])
        else:
            self.args = None
        
        
    def main_callback(self):         
        print("Main Menu")
        print("0. Quit")
        print("1. Get dataset metadata")
        print("2. Get sample metadata")
        print("3. Get transactions")
        print("4. Get student steps")
        print("5. Add custom field")
        try:
            choice = int(input("==> "))
        except ValueError:
            choice = -1
        
        if choice == 0:
            return False
        elif choice == 1:
            choice = int(input("Dataset id? "))
            self.send("tutorgen.get_dataset_metadata",{"dataset_id":choice},self.print_response_callback)
            time.sleep(2)
        elif choice == 2:
            did = int(input("Dataset id? "))
            sid = int(input("Sample id? "))
            self.send("tutorgen.get_sample_metadata",{"dataset_id":did,"sample_id":sid},self.print_response_callback)
            time.sleep(2)
        elif choice == 3:
            did = int(input("Dataset id? "))
            sid = int(input("Sample id?  (optional, -1 for none)"))
            if sid != -1:
                self.send("tutorgen.get_transactions",{"dataset_id":did,"sample_id":sid},self.print_response_callback)
            else:
                self.send("tutorgen.get_transactions",{"dataset_id":did},self.print_response_callback)
            time.sleep(2)
        elif choice == 4:
            did = int(input("Dataset id? "))
            sid = int(input("Sample id?  (optional, -1 for none)"))
            if sid != -1:
                self.send("tutorgen.get_student_steps",{"dataset_id":did,"sample_id":sid},self.print_response_callback)
            else:
                self.send("tutorgen.get_student_steps",{"dataset_id":did},self.print_response_callback)
            time.sleep(2)
        elif choice == 5:
            did = int(input("Dataset id? "))
            name = input("Custom field name: ")
            description  = input("Custom field description: ")
            typ = input("Type? (number, string, date, big) ")
            
            self.send("tutorgen.add_custom_field",{"dataset_id":did,"name":name,"description":description,"type":typ},self.print_response_callback)
            time.sleep(2) 
           
        
        print("=====")
        print("")
        
        return True
            
    
    def print_response_callback(self,response):
        print("Response from HIPT: " + str(response))
 
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Entity id and secret')
    parser.add_argument('entity_id', type=str, help="The entity ID of the entity.")
    parser.add_argument('api_key', type=str, help="The api key of the entity.")
    arguments = parser.parse_args()
    
    settings = HpitClientSettings.settings()
    settings.HPIT_URL_ROOT = 'http://127.0.0.1:8000'
    
    logger_path = os.path.join(settings.PROJECT_DIR, 'log/tutor_71f476d0-55c0-4173-84c2-811edb350d02.log')
    logging.basicConfig(
            filename=logger_path,
            level=logging.DEBUG,
            propagate=False,
            format='%(asctime)s %(levelname)s:----:%(message)s', 
            datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)
    d = DataShopConnectorTutor(arguments.entity_id,arguments.api_key,logger,None,None)
    d.start()
