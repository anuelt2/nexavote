from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import markdown
import os

def api_documentation(request):
    """
    Serve the API documentation as HTML page
    """
    # Path to markdown documentation file
    docs_path = os.path.join(os.path.dirname(__file__), 'api_docs.md')
    
    try:
        with open(docs_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content, 
            extensions=['codehilite', 'fenced_code', 'tables', 'toc']
        )
        
        context = {
            'documentation': html_content,
            'title': 'NexaVote API Documentation'
        }
        
        return render(request, 'docs/api_documentation.html', context)
        
    except FileNotFoundError:
        return HttpResponse("Documentation not found", status=404)

@api_view(['GET'])
def api_schema(request):
    """
    Return API schema information
    """
    return Response({
        'api_version': '1.0.0',
        'documentation_url': request.build_absolute_uri('/docs/'),
        'base_url': request.build_absolute_uri('/api/'),
        'endpoints': {
            'authentication': '/api/auth/',
            'users': '/api/users/',
            'elections': '/api/elections/',
            'candidates': '/api/candidates/',
            'votes': '/api/votes/',
            'invitations': '/api/invitations/',
            'election_events': '/api/election-events/',
        }
    })
