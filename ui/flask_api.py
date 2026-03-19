"""
Flask REST API for PD Screening System
Provides HTTP endpoints for screening services
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from flask import Flask, request, jsonify
from flask_cors import CORS
from loguru import logger
import os

from main import PDScreeningSystem


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize screening system
screening_system = None


def initialize_system():
    """Initialize the screening system"""
    global screening_system
    if screening_system is None:
        logger.info("Initializing PD Screening System")
        config_path = os.getenv('CONFIG_PATH', 'config.yaml')
        screening_system = PDScreeningSystem(config_path)
        logger.info("System initialized successfully")


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500


# API Routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PD Screening API',
        'version': '1.0.0'
    })


@app.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        initialize_system()
        stats = screening_system.get_system_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v1/screen', methods=['POST'])
def screen_transcript():
    """
    Screen a transcript for PD indicators
    
    Request body:
    {
        "transcript": "text to analyze",
        "include_details": true/false (optional)
    }
    """
    try:
        initialize_system()
        
        # Validate request
        if not request.json:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        transcript = request.json.get('transcript')
        if not transcript:
            return jsonify({
                'success': False,
                'error': 'Missing required field: transcript'
            }), 400
        
        if not isinstance(transcript, str) or len(transcript.strip()) < 5:
            return jsonify({
                'success': False,
                'error': 'Transcript must be a string with at least 5 characters'
            }), 400
        
        # Optional parameters
        include_details = request.json.get('include_details', False)
        
        # Run screening
        logger.info(f"Processing screening request (length: {len(transcript)} chars)")
        results = screening_system.screen_transcript(
            transcript,
            include_details=include_details
        )
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Screening failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v1/batch-screen', methods=['POST'])
def batch_screen():
    """
    Screen multiple transcripts in batch
    
    Request body:
    {
        "transcripts": [
            {"id": "1", "text": "transcript 1"},
            {"id": "2", "text": "transcript 2"}
        ],
        "include_details": true/false (optional)
    }
    """
    try:
        initialize_system()
        
        # Validate request
        if not request.json:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        transcripts = request.json.get('transcripts')
        if not transcripts or not isinstance(transcripts, list):
            return jsonify({
                'success': False,
                'error': 'Missing or invalid field: transcripts (must be array)'
            }), 400
        
        include_details = request.json.get('include_details', False)
        
        # Process each transcript
        results = []
        for item in transcripts:
            transcript_id = item.get('id', 'unknown')
            text = item.get('text', '')
            
            if not text or len(text.strip()) < 5:
                results.append({
                    'id': transcript_id,
                    'success': False,
                    'error': 'Transcript too short or empty'
                })
                continue
            
            try:
                result = screening_system.screen_transcript(
                    text,
                    include_details=include_details
                )
                result['id'] = transcript_id
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process transcript {transcript_id}: {e}")
                results.append({
                    'id': transcript_id,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'total': len(transcripts),
            'processed': len(results),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Batch screening failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v1/validate', methods=['POST'])
def validate_transcript():
    """
    Validate a transcript without full screening
    
    Request body:
    {
        "transcript": "text to validate"
    }
    """
    try:
        initialize_system()
        
        if not request.json:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        transcript = request.json.get('transcript')
        if transcript is None:
            return jsonify({
                'success': False,
                'error': 'Missing required field: transcript'
            }), 400
        
        # Validate using preprocessor
        preprocessed = screening_system.preprocessor.preprocess(transcript)
        
        return jsonify({
            'success': True,
            'is_valid': preprocessed['is_valid'],
            'validation': preprocessed['validation'],
            'features': preprocessed.get('features', {})
        })
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Documentation endpoint
@app.route('/api/v1/docs', methods=['GET'])
def api_docs():
    """API documentation"""
    docs = {
        'service': 'PD Screening API',
        'version': '1.0.0',
        'endpoints': {
            '/health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            },
            '/api/v1/stats': {
                'method': 'GET',
                'description': 'Get system statistics'
            },
            '/api/v1/screen': {
                'method': 'POST',
                'description': 'Screen a single transcript',
                'body': {
                    'transcript': 'string (required)',
                    'include_details': 'boolean (optional)'
                }
            },
            '/api/v1/batch-screen': {
                'method': 'POST',
                'description': 'Screen multiple transcripts',
                'body': {
                    'transcripts': 'array of {id, text} (required)',
                    'include_details': 'boolean (optional)'
                }
            },
            '/api/v1/validate': {
                'method': 'POST',
                'description': 'Validate transcript without full screening',
                'body': {
                    'transcript': 'string (required)'
                }
            }
        },
        'response_format': {
            'risk_score': 'float (0.0 - 1.0)',
            'confidence': 'string (low|medium|high)',
            'rationale': 'array of strings',
            'recommendation': 'string (monitor|refer for evaluation|insufficient data)'
        }
    }
    return jsonify(docs)


def main():
    """Run Flask application"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PD Screening REST API')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Initialize system at startup
    initialize_system()
    
    # Run app
    logger.info(f"Starting Flask API on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()