from concurrent import futures
import grpc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared.gemini_client import search_google_with_gemini
from protos import agent_pb2
from protos import agent_pb2_grpc

class GoogleSearchAgent(agent_pb2_grpc.AgentServicer):
    def Handle(self, request, context):
        prompt = request.prompt
        print(f"[GoogleSearchAgent] Received prompt: {prompt}")

    def Process(self, request, context):
        result = search_google_with_gemini(request.prompt)
        return agent_pb2.AgentReply(response=result)

def serve():
    reply = agent_pb2.AgentReply(response="Hello from Google search Agent")
    print(reply.response)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agent_pb2_grpc.add_AgentServicer_to_server(GoogleSearchAgent(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("GoogleSearchAgent gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()