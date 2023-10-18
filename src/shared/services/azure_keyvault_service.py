import pathlib
from os import environ as env
from dotenv import load_dotenv
from src.shared.utils.colors import bcolors
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class AzureKeyvaultService:
    def __init__(self):
        root_path = pathlib.Path().resolve()
        env_path = root_path.joinpath('.env')
        load_dotenv(env_path)
        self.KEY_VAULT_NAME = env.get('KEY_VAULT_NAME',default=None)

    def connection(self):
        try:
            self.vault_url = f"https://{self.KEY_VAULT_NAME}.vault.azure.net"
            self.credential = DefaultAzureCredential()
            return SecretClient(vault_url=self.vault_url, credential=self.credential)
        except Exception as error:
            print(f'\n{bcolors.RED}[AZURE KEYVAULT SERVICE]{bcolors.ENDC} - Connection attempt to AZURE KEYVAULT failed:', error)

    def get_kv_secret(self, secret: str):
        if self.KEY_VAULT_NAME:
            gt_secret = self.connection().get_secret(secret).value
            print(f'{bcolors.CYAN}[AZURE KEYVAULT SERVICE]{bcolors.ENDC} - {secret}')
            return gt_secret
        else:
            gt_secret = env.get(secret)
            print(f'{bcolors.CYAN}[LOCAL KEYVAULT SERVICE]{bcolors.ENDC} - {secret}')
            return gt_secret