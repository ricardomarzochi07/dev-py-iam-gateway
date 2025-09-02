from pydantic import BaseModel


class AppEnvConfig(BaseModel):
    url_base_bitbucket: str
    path_local_repo: str
    path_file_excel: str
    history_file: str
    api_bitbucket_get_repository_angular: str
    api_bitbucket_all_repositories: str
    api_bitbucket_get_repository: str
    api_bitbucket_branches_exist: str
    api_bitbucket_get_version: str
    api_bitbucket_get_path_branch: str
    api_bitbucket_get_version_with_path: str
    authorization_token: str


class AppConfig(BaseModel):
    config: AppEnvConfig
