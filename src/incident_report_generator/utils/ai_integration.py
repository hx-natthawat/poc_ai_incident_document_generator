"""AI integration module for generating summaries using OpenAI."""
import os
import json
from typing import Dict, List, Optional
import logging
from openai import OpenAI, OpenAIError, APIError, APITimeoutError, AuthenticationError

# Configure logging
logger = logging.getLogger(__name__)

# Configure OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_summary(incidents: List[Dict]) -> str:
    """Generate a summary of incident data using OpenAI.
    
    Args:
        incidents: List of incident dictionaries
        
    Returns:
        Generated summary text
        
    Raises:
        ValueError: If incidents list is empty
        RuntimeError: If OpenAI API call fails
    """
    try:
        if not incidents:
            raise ValueError("No incidents provided for summary generation")
        
        # Prepare incident data for the prompt
        total_incidents = len(incidents)
        resolved = sum(1 for inc in incidents if inc['Status'] == 'Resolved')
        priorities = {}
        departments = {}
        categories = {}
        sla_status = {'Within SLA': 0, 'Breached': 0}
        
        for incident in incidents:
            # Count by priority
            priorities[incident['Priority']] = priorities.get(incident['Priority'], 0) + 1
            
            # Count by department
            departments[incident['Department']] = departments.get(incident['Department'], 0) + 1
            
            # Count by category
            categories[incident['Category']] = categories.get(incident['Category'], 0) + 1
            
            # Count SLA status
            if incident['SLA_Status'] == 'Within SLA':
                sla_status['Within SLA'] += 1
            else:
                sla_status['Breached'] += 1
        
        # Create a structured analysis
        analysis = {
            'total_incidents': total_incidents,
            'resolved_incidents': resolved,
            'unresolved_incidents': total_incidents - resolved,
            'priorities': priorities,
            'departments': departments,
            'categories': categories,
            'sla_status': sla_status
        }
        
        # Create the prompt
        prompt = f"""Analyze the following incident report data and provide a clear, concise summary:

Incident Analysis:
- Total Incidents: {analysis['total_incidents']}
- Resolved: {analysis['resolved_incidents']}
- Unresolved: {analysis['unresolved_incidents']}

Priority Distribution:
{json.dumps(analysis['priorities'], indent=2)}

Department Distribution:
{json.dumps(analysis['departments'], indent=2)}

Category Distribution:
{json.dumps(analysis['categories'], indent=2)}

SLA Status:
{json.dumps(analysis['sla_status'], indent=2)}

Please provide:
1. A brief overview of the incident landscape
2. Key observations about priorities and categories
3. Notable trends in resolution and SLA compliance
4. Any significant patterns or concerns
5. Recommendations for improvement

Format the response in clear paragraphs with proper line breaks."""

        # Call OpenAI API with retry logic
        for attempt in range(3):  # Retry up to 3 times
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert incident analyst. Provide clear, actionable insights from incident data."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                
                summary = response.choices[0].message.content.strip()
                logger.info("Successfully generated incident summary")
                return summary
                
            except (APIError, APITimeoutError) as e:
                if attempt == 2:  # Last attempt
                    logger.error(f"OpenAI API error after 3 attempts: {str(e)}")
                    raise RuntimeError(f"OpenAI API error: {str(e)}")
                logger.warning(f"OpenAI API error (attempt {attempt + 1}): {str(e)}")
                continue
                
            except AuthenticationError:
                logger.error("OpenAI API authentication failed. Check your API key.")
                raise RuntimeError("OpenAI API authentication failed")
                
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise RuntimeError(f"Failed to generate summary: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error in generate_summary: {str(e)}")
        raise RuntimeError(f"Error in generate_summary: {str(e)}")

def validate_openai_key() -> bool:
    """Validate the OpenAI API key.
    
    Returns:
        True if the API key is valid, False otherwise
    """
    try:
        # Make a minimal API call to test the key
        client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return True
        
    except AuthenticationError:
        logger.error("Invalid OpenAI API key")
        return False
        
    except Exception as e:
        logger.error(f"Error validating OpenAI API key: {str(e)}")
        return False
