from boto3.session import Session
from bedrock_agentcore_starter_toolkit import Runtime

boto_session = Session()
region = boto_session.region_name

# Have Amazon Cognito for Authentication set up before continue
tool_name = "pubmed_mcp_server_github"
client_id = "123asd123asd123asd123"
pool_id = "us-east-1_aaaaaaa"

discovery_url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/openid-configuration"

# configure
agentcore_runtime = Runtime()

auth_config = {
    "customJWTAuthorizer": {
        "allowedClients": [
            client_id
        ],
        "discoveryUrl": discovery_url,
    }
}

print("Configuring AgentCore Runtime...")
response = agentcore_runtime.configure(
    entrypoint="pubmed_server.py",
    auto_create_execution_role=True,
    auto_create_ecr=True,
    requirements_file="requirements.txt",
    region=region,
    authorizer_configuration=auth_config,
    protocol="MCP",
    agent_name=tool_name
)
print("Configuration completed ✓")


## launch
print("Launching MCP server to AgentCore Runtime...")
print("This may take several minutes...")
launch_result = agentcore_runtime.launch()
print("Launch completed ✓")
print(f"Agent ARN: {launch_result.agent_arn}")
print(f"Agent ID: {launch_result.agent_id}")
