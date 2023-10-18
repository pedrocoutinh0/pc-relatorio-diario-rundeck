from src.shared.utils.colors import bcolors
from src.shared.services.azure_keyvault_service import AzureKeyvaultService
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import os

load_dotenv()

class Rundeck:
    def __init__(self):
        # Inicializa o cliente Rundeck
        keyvault = AzureKeyvaultService()
        self.APITOKEN = keyvault.get_kv_secret("TOKEN-RUNDECK")
        self.RUNDECKURL = os.getenv("RUNDECK_URL")
        self.PROJECTNAME = os.getenv("PROJECT_NAME")
        self.HEADER = {
            "Accept": "application/json",
            "X-Rundeck-Auth-Token": f"{self.APITOKEN}"
        }
    
    def jobs_rodando(self):
        # Obtém informações sobre trabalhos em execução
        response = requests.get(f"{self.RUNDECKURL}/api/32/project/{self.PROJECTNAME}/executions/running", headers=self.HEADER)
        jobs_json = response.json()
        
        jobs_formated = []
        for job in jobs_json["executions"]:
            # Processa as informações dos trabalhos em execução
            dt_exec = job["date-started"]["date"]
            dt_obj = datetime.strptime(dt_exec, "%Y-%m-%dT%H:%M:%SZ")
            dt_obj = dt_obj - timedelta(hours=3)
            now = datetime.now()
            time_run = now - dt_obj
            time_run = int(time_run.total_seconds() / 60)
            dt_formated = dt_obj.strftime("%d/%m/%Y %H:%M:%S")
            id = job["job"]["id"]
            name = job["job"]["name"]
            permlink = job["permalink"]
            atual = dict(ID=id, NAME=name, PERMLINK=permlink, DATA=dt_formated, TIME=time_run)
            jobs_formated.append(atual)
        return jobs_formated
    
    def jobs_status_error(self):
        # Obtém informações sobre trabalhos com status de erro
        query = {
            "statusFilter": "failed",
            "recentFilter": "12h"
        }   
        response = requests.get(f"{self.RUNDECKURL}/api/32/project/{self.PROJECTNAME}/executions", headers=self.HEADER, params=query)
        jobs_json = response.json()
        
        jobs_formated = []
        for job in jobs_json["executions"]:
            # Processa as informações dos trabalhos com status de erro
            dt_exec_init = job["date-started"]["date"]
            dt_obj_init = datetime.strptime(dt_exec_init, "%Y-%m-%dT%H:%M:%SZ")
            dt_obj_init = dt_obj_init - timedelta(hours=3)
            dt_formated_init = dt_obj_init.strftime("%d/%m/%Y %H:%M:%S")
            
            dt_exec_end = job["date-ended"]["date"]
            dt_obj_end = datetime.strptime(dt_exec_end, "%Y-%m-%dT%H:%M:%SZ")
            dt_obj_end = dt_obj_end - timedelta(hours=3)
            dt_formated_end = dt_obj_end.strftime("%d/%m/%Y %H:%M:%S")
 
            id = job["job"]["id"]
            name = job["job"]["name"]
            permlink = job["permalink"]
            atual = dict(ID=id, NAME=name, PERMLINK=permlink, DATA_INIT=dt_formated_init, DATA_END=dt_formated_end)
            jobs_formated.append(atual)
        return jobs_formated
