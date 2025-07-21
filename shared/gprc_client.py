import grpc

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import protos.agent_pb2 as agent_pb2
import protos.agent_pb2_grpc as agent_pb2_grpc

def call_agent(host: str, prompt: str) -> str:
    with grpc.insecure_channel(host) as channel:
        stub = agent_pb2_grpc.AgentStub(channel)
        request = agent_pb2.AgentRequest(prompt=prompt)
        response = stub.Process(request)
        return response.response
