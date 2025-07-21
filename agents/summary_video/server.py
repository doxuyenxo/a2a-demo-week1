from concurrent import futures
import grpc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared.gemini_client import search_google_with_gemini
from protos import agent_pb2
from protos import agent_pb2_grpc
from video_summary import summary_youtube_video

class VideoSummaryAgent(agent_pb2_grpc.AgentServicer):
    def Process(self, request, context):
        result = summary_youtube_video(request.prompt)
        return agent_pb2.AgentReply(response=result)

def serve():
    reply = agent_pb2.AgentReply(response="Hello from Google video summary Agent")
    print(reply.response)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agent_pb2_grpc.add_AgentServicer_to_server(VideoSummaryAgent(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("VideoSummaryAgent gRPC server started on port 50052")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()