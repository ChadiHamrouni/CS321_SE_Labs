"""
Exercise 13: Product Review Analyzer with Structured Output
===========================================================
Learning Objectives:
- Using JSON mode for reliable structured output
- Structured data extraction with Pydantic models
- Sentiment analysis from text reviews

Task:
Students will implement a review analyzer that extracts sentiment,
score, key points, and recommendations from customer reviews.
"""

import ollama
import json
from models import ReviewAnalysis

# ============= GRADING FUNCTIONS =============

def grade_review_analysis(analysis: ReviewAnalysis) -> dict:
    """Grade a review analysis based on completeness."""
    score = 0
    feedback = []
    
    # Sentiment label (30 points)
    if analysis.sentiment in ['positive', 'negative', 'neutral']:
        score += 30
        feedback.append(f"✓ Valid sentiment: {analysis.sentiment} (30/30)")
    else:
        feedback.append(f"✗ Invalid sentiment: {analysis.sentiment} (0/30)")
    
    # Score range (30 points)
    if -1.0 <= analysis.score <= 1.0:
        score += 30
        feedback.append(f"✓ Valid score: {analysis.score:.2f} (30/30)")
    else:
        feedback.append(f"✗ Score out of range: {analysis.score:.2f} (0/30)")
    
    # Key points (40 points)
    num_points = len(analysis.key_points)
    if num_points >= 2:
        score += 40
        feedback.append(f"✓ Key points: {num_points} extracted (40/40)")
    elif num_points == 1:
        score += 20
        feedback.append(f"△ Only 1 key point extracted (20/40)")
    else:
        feedback.append(f"✗ No key points extracted (0/40)")
    
    return {
        "score": score,
        "max_score": 100,
        "percentage": score,
        "feedback": feedback
    }


# ============= SAMPLE SOLUTION (HIDDEN FROM STUDENTS) =============

def analyze_review_solution(review_text: str, model: str = "gemma3:1b") -> ReviewAnalysis:
    """Reference implementation for instructors."""
    
    system_prompt = """You are a review analyzer. Extract sentiment information.

Return JSON with this structure:
{
    "sentiment": "positive", "negative", or "neutral",
    "score": -1.0 to 1.0 (negative to positive),
    "key_points": ["point 1", "point 2", ...],
    "would_recommend": true or false
}

Rules:
- sentiment must match score (>0.3=positive, <-0.3=negative, else neutral)
- Extract 2-4 key points from the review
- Be concise"""
    
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze: {review_text}"}
        ],
        format='json'
    )
    
    data = json.loads(response['message']['content'])
    return ReviewAnalysis(**data)


# ============= TEST CASES =============

TEST_REVIEWS = [
    "Love this coffee maker! Quality is outstanding. Price was steep but worth it. Highly recommend!",
    "Very disappointed. Product arrived damaged. Customer service was rude. Would not recommend.",
    "It's okay. Does what it should. Price is fair, quality is average. Neutral about recommending."
]


def run_test_case(review_text: str, test_num: int):
    """Run analysis on a single test review."""
    print(f"\n{'='*60}")
    print(f"TEST {test_num}: {review_text}")
    print(f"{'='*60}")
    
    analysis = analyze_review_solution(review_text)
    
    print(f"✓ Sentiment: {analysis.sentiment.upper()} (score: {analysis.score:.2f})")
    print(f"✓ Recommend: {'YES' if analysis.would_recommend else 'NO'}")
    print(f"✓ Key Points: {', '.join(analysis.key_points)}")
    
    results = grade_review_analysis(analysis)
    print(f"\nScore: {results['score']}/{results['max_score']}")
    for fb in results['feedback']:
        print(f"  {fb}")


def main():
    """Main function to test review analysis."""

    for i, review in enumerate(TEST_REVIEWS, 1):
        run_test_case(review, i)
    
    print("\n" + "="*60)



if __name__ == "__main__":
    main()
