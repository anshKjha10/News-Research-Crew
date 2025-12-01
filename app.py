from flask import Flask, render_template, request, jsonify, send_file
import os
from datetime import datetime
from pathlib import Path
from src.news_research_crew.crew import NewsResearchCrew

app = Flask(__name__)
app.config['SECRET_KEY'] = '5704a64e400809dd94bbfa09f2836c09327adf84466281f1bb944deffacd3fe8'

# Store for tracking crew runs
crew_runs = []

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_crew():
    """Run the News Research Crew with provided inputs."""

    try:
        topic = request.form.get('topic', '').strip()
        refined_query = request.form.get('refined_query', '').strip()
        
        if not topic:
            return jsonify({'error': 'Topic is required.'}), 400

        inputs = {
            'topic' : topic,
            'refined_query' : refined_query,
            'current_year' : str(datetime.now().year)
        }

        result = NewsResearchCrew().crew().kickoff(inputs=inputs)

        run_id = len(crew_runs)
        crew_runs.append({
            'id': run_id,
            'topic': topic,
            'refined_query': refined_query,
            'timestamp': datetime.now().isoformat(),
            'result': str(result)
        })

        return jsonify({
            'success': True,
            'run_id': run_id,
            'message': 'Crew run completed successfully.',
            'output_file': 'news_digest.md'
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred while running the crew: {e}'}), 500
    
@app.route('/results')
def results():
    """View all crew runs."""
    return render_template('results.html', runs=crew_runs)

@app.route('/results/<int:run_id>')
def view_result(run_id):
    """View specific crew run result."""
    if run_id < len(crew_runs):
        run = crew_runs[run_id]
        return render_template('view_result.html', run=run)
    
    return "Run not found", 404

@app.route('/download/<filename>')
def download_file(filename):
    """Download the generated markdown file."""
    file_path = Path(filename)
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
