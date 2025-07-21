from concurrent import futures
import grpc
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from shared.gemini_client import generate_image_with_imagen2
from protos import agent_pb2
from protos import agent_pb2_grpc

class TextToImageAgent(agent_pb2_grpc.AgentServicer):
    def Process(self, request, context):
        prompt = request.prompt
        print(f"[TextToImageAgent] Processing image generation for prompt: {prompt}")
        image_url = generate_image_with_imagen2(prompt)
        return agent_pb2.AgentReply(response=image_url)

def serve():
    reply = agent_pb2.AgentReply(response="Hello from Text-to-Image Agent")
    print(reply.response)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agent_pb2_grpc.add_AgentServicer_to_server(TextToImageAgent(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("TextToImageAgent gRPC server started on port 50053")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
