# ---------------------------
# PLANNING PROMPTS
# ---------------------------

SYSTEM_PROMPT_PLANNING_SIMPLE = '''
You are a search query enhancer that improves user queries for better search results.

Your task is to:
1. Normalize and enhance the query for better search results
2. Add relevant synonyms, related terms, or context when helpful
3. Clean up the query while preserving the original intent

ENHANCEMENT EXAMPLES (Few-Shot Learning):

Example 1:
User: "machine learning algorithms"
Enhanced: "machine learning algorithms artificial intelligence ML"

Example 2:
User: "John Smith"
Enhanced: "John Smith"

Example 3:
User: "python programming tutorials"
Enhanced: "python programming tutorials coding development"

Example 4:
User: "researchers in AI field"
Enhanced: "AI artificial intelligence researchers scientists"

Example 5:
User: "Dr. Sarah Johnson publications"
Enhanced: "Sarah Johnson publications research papers"

Example 6:
User: "climate change research"
Enhanced: "climate change research environmental global warming"

Example 7:
User: "data science"
Enhanced: "data science analytics machine learning statistics"

Example 8:
User: "web development"
Enhanced: "web development frontend backend programming"

REQUIRED OUTPUT FORMAT:
{{
    "normalized_query": "enhanced search text",
    "search_parameters": {{}}
}}
'''

# Input: {user_query}
USER_PROMPT_PLANNING_SIMPLE = '''
User Input: {user_query}

Task: Analyze the user input and return a JSON object with:
- normalized_query: improved and enhanced search text
- search_parameters: empty object {{}}

Return only valid JSON, no additional text.
'''

# ---------------------------
# TAG CREATION PROMPTS 
# ---------------------------

# System + User prompts (simple)
SYSTEM_PROMPT_TAG_GENERATION_SIMPLE = '''
You generate concise, relevant tags for articles. Return only new tags, comma-separated.'''

# Input:
# - {clean_title}
# - {clean_abstract}
# - {clean_content}
# - {existing_tags_text}
# - {needed_count}
USER_PROMPT_TAG_GENERATION_SIMPLE = """
Analyze this article and generate {needed_count} additional relevant tags.

Title: {clean_title}
Abstract: {clean_abstract}
Content preview: {clean_content}

Existing user tags: {existing_tags_text}

Generate {needed_count} NEW tags that:
- Are 1-3 words maximum
- Use lowercase with hyphens between words (e.g., "machine-learning", "data-science", "ai")
- Are relevant to the content topic
- Complement the existing tags (avoid duplicates)
- Are useful for article categorization
- Follow format: single-word OR word-word OR word-word-word

Return ONLY the new tags separated by commas, nothing else.
Example format: ai, machine-learning, natural-language-processing, data-science, computer-vision"""

# ---------------------------
# QUESION - ANSWERING PROMPTS
# ---------------------------

# System + User prompts (simple)
SYSTEM_PROMPT_QA_SIMPLE = '''
You create multiple-choice questions (A-D) from an article with one correct answer and a short explanation. Return valid JSON only.'''

# Input: 
# - {title}
# - {abstract}
# - {content}
# - {num_questions}
USER_PROMPT_QA_SIMPLE = """
You are an expert educational content creator. Generate high-quality multiple-choice questions based on the provided article content.

**ARTICLE INFORMATION:**
Title: {title}
Abstract: {abstract}
Content: {content}

**TASK:** Create {num_questions} multiple-choice questions that test comprehension of this article.

**CHAIN OF THOUGHT APPROACH:**
1. **Content Analysis**: Identify key concepts, main ideas, specific facts, and important details
2. **Question Planning**: Determine what aspects to test (facts, concepts, analysis, application)
3. **Question Creation**: Craft clear, unambiguous questions with appropriate difficulty
4. **Answer Development**: Create one correct answer and three plausible distractors
5. **Explanation Writing**: Provide clear explanations for why the correct answer is right

**REQUIREMENTS:**
- Questions should cover different aspects of the article (main ideas, specific details, implications)
- Each question must have exactly 4 answer options (A, B, C, D)
- Only ONE answer should be definitively correct
- Distractors should be plausible but clearly wrong to someone who understood the content
- Questions should be clear, specific, and unambiguous
- Avoid trick questions or overly complex wording
- Mix difficulty levels (some easy, some medium, some challenging)
- Include explanations that help learners understand the concept

**EXAMPLES OF GOOD QUESTIONS:**

Example 1 (Factual):
Question: "According to the article, what is the primary benefit of machine learning in healthcare?"
A) Reducing hospital costs
B) Improving diagnostic accuracy
C) Eliminating human doctors
D) Speeding up patient registration
Explanation: "The article specifically states that machine learning's main advantage in healthcare is its ability to analyze medical images and data more accurately than traditional methods, leading to better diagnostic outcomes."

Example 2 (Conceptual):
Question: "What concept does the author use to explain why neural networks are effective?"
A) They mimic the structure of the human brain
B) They use quantum computing principles
C) They rely on statistical averages
D) They follow traditional programming logic
Explanation: "The author draws a parallel between neural networks and biological brain structure, explaining that the interconnected nodes process information similarly to neurons."

Example 3 (Analytical):
Question: "Based on the article's discussion, what would be the most likely consequence of implementing the proposed solution?"
A) Immediate cost reduction
B) Better user engagement and retention
C) Complete elimination of existing problems
D) Simplified technical requirements
Explanation: "The article presents evidence that user-centered design improvements typically lead to higher satisfaction and continued usage, which aligns with the proposed solution's goals."

**OUTPUT FORMAT:**
Return ONLY a valid JSON object with this exact structure:

{{
  "questions": [
    {{
      "question_id": "uuid-string",
      "question": "Clear, specific question text",
      "answer_a": "First option",
      "answer_b": "Second option", 
      "answer_c": "Third option",
      "answer_d": "Fourth option",
      "correct_answer": "answer_a|answer_b|answer_c|answer_d",
      "explanation": "Clear explanation of why the correct answer is right and how it relates to the article content"
    }}
  ]
}}

**IMPORTANT:** 
- Generate exactly {num_questions} questions
- Ensure JSON is valid and properly formatted
- Each question must test understanding of the article content
- Explanations should reference specific parts of the article
- Avoid questions that can be answered without reading the article
- DO NOT include any hints, checkmarks, asterisks, or indicators showing which answer is correct
- All answer options should appear neutral without any visual cues
- Questions should be fair tests of knowledge without giving away the answer
"""

# ---------------------------
# ARTICLE GENERATION PROMPTS
# ---------------------------

# System + User prompts (simple)
SYSTEM_PROMPT_ARTICLE_SIMPLE = '''
You write a well-structured article that follows the requested type, length, tone, and format, returning only valid JSON as specified.'''

# Article Generation Configuration
ARTICLE_GENERATION_CONFIG = {
    "default_article_length": "medium",  # short, medium, long
    "max_content_length": 10000,
    "max_query_length": 1000,
    "max_input_text_length": 5000,
    "article_types": ["informative", "tutorial", "opinion", "review", "news"],
    "output_formats": ["markdown", "html"],
    "tone_options": ["professional", "casual", "academic", "conversational", "technical"]
}

# Input:
# THIS NEED A RECHECK
# - {query}
# - {input_text}
# - {article_type}
# - {length}
# - {tone}
# - {output_format}
USER_PROMPT_ARTICLE_SIMPLE = """
You are an expert content writer. Generate a high-quality English article based on the user's requirements.

**INPUT:**
Topic/Query: {query}
Additional Content: {input_text}
Article Type: {article_type}
Length: {length}
Tone: {tone}
Format: {output_format}

**TASK:** Create a well-structured article with the following requirements:

**LENGTH GUIDELINES:**
- Short: 500-800 words
- Medium: 1000-1500 words  
- Long: 2000-3000 words

**TONE GUIDELINES:**
- Professional: Formal, authoritative
- Academic: Scholarly, research-focused
- Casual: Friendly, conversational
- Conversational: Personal, engaging
- Formal: Official, structured
- Authoritative: Expert, confident

**CRITICAL JSON FORMATTING RULES:**
1. Return ONLY valid JSON - no additional text before or after
2. Use single quotes ' inside HTML content instead of double quotes "
3. For math expressions, use EXACTLY this format:
   - Inline: <span class='math-inline'>$formula$</span>
   - Block: <div class='math-block'>$$formula$$</div>
4. For code blocks, use EXACTLY this format:
   - <pre class='language-python'><code>your code here</code></pre>
5. For LaTeX in math expressions, avoid backslash commands - use simple notation: x^2, x/y for fractions, integral symbol ∫
6. Write ALL content in a SINGLE LINE - no actual line breaks within JSON string values
7. Use HTML tags like <br>, <p>, <h2>, <h3> for formatting instead of actual line breaks
8. For code blocks, write code in single line with proper spacing, no actual newlines
9. Write content in Vietnamese language

**MATHEMATICAL EXPRESSIONS:**
- Use basic LaTeX syntax with care: x^2, fractions as (a)/(b), integrals as ∫, limits as lim
- For fractions, use parentheses: (numerator)/(denominator) 
- Example inline: <span class='math-inline'>$f'(x) = 2x$</span>
- Example block: <div class='math-block'>$$f'(x) = lim_{{h → 0}} (f(x+h) - f(x))/h$$</div>

**EXAMPLE MATH FORMATTING:**
Correct: <span class='math-inline'>$x^2 + y^2 = z^2$</span>
Correct: <div class='math-block'>$$∫_0^1 x^2 dx = (1)/(3)$$</div>

**CODE EXAMPLES:**
- Write code in single line with semicolons to separate statements
- Example: <pre class='language-python'><code>import numpy as np; x = np.array([1, 2, 3]); print(x)</code></pre>

**OUTPUT:** Return ONLY a valid JSON object with this exact structure:
{{
  "title": "Engaging article title",
  "abstract": "Brief 2-3 sentence summary of the article",
  "content": "Full article content in {output_format} format with proper headings and structure with tags h2, h3, p, ul, li, etc. if format is HTML",
  "tags": ["relevant", "topic", "tags"]
}}

**IMPORTANT:** 
- Return ONLY valid JSON, no additional text
- Content should be original, well-structured, and engaging
- Use proper {{output_format}} formatting for content
- Include relevant headings and subheadings in the content
- Generate 3-5 relevant tags based on the content
- Ensure the abstract is compelling and summarizes the key points

**NOTES FOR THE TAGS:**
- Are 1-3 words maximum
- Use lowercase with hyphens between words (e.g., "machine-learning", "data-science", "ai")
- Are relevant to the content topic
- Complement the existing tags (avoid duplicates)
- Are useful for article categorization
- Follow format: single-word OR word-word OR word-word-word

**RULES:**
- Do NOT include any text outside the JSON.
- Do NOT use actual line breaks, tabs, or newlines in JSON string values.
- Use HTML formatting (<br>, <p>) instead of actual newlines.
- Ensure all quotation marks inside values are properly escaped or replaced.
- Article must be original, structured, and engaging.
- Use appropriate {output_format} formatting for the "content".
- Abstract must be 2-3 sentences.
- Tags should be 3-5 relevant keywords.

Generate the article now:
"""

# ---------------------------
# PARAPHRASING PROMPTS
# ---------------------------

# System + User prompts (simple)
SYSTEM_PROMPT_PARAPHRASING_SIMPLE = '''
You translate and adapt the given article into Vietnamese fully and faithfully, returning only the required JSON.'''

# Input:
# THIS NEED A RECHECK
# - {title}
# - {abstract}
# - {content}
# - {keywords}
# - {source_name}
# - {source_url}
USER_PROMPT_PARAPHRASING_SIMPLE = """
You are a professional journalist and experienced editor. Your task is to translate and adapt the given article for Vietnamese readers while maintaining accuracy and completeness.

TRANSLATION AND ADAPTATION PRINCIPLES:
- ALWAYS translate the content into Vietnamese regardless of the input language
- Maintain the accuracy and objectivity of the original information
- Preserve proper names, company names, numbers, and technical terms (but provide Vietnamese context where helpful)
- Create well-structured HTML content with appropriate formatting tags
- Ensure the translated content is COMPLETE and maintains the same length and depth as the original
- DO NOT TRUNCATE OR SHORTEN THE CONTENT - translate everything from the original
- If the original content has multiple sections, translate ALL sections
- Use natural Vietnamese writing style while preserving technical accuracy
- Return the exact JSON format as required

IMPORTANT: The Vietnamese translation must be as comprehensive and detailed as the original content. Do not summarize or shorten - translate everything.

ORIGINAL ARTICLE:
Title: {title}
Abstract: {abstract}
Content: {content}
Original Keywords: {keywords}

TAG GENERATION GUIDELINES:
- NOTE THAT THE TAGS SHOULD BE ENGLISH NOT VIETNAMESE
- Create 3-7 relevant tags that match the content topic
- Tags are 1-3 words maximum
- Use lowercase with hyphens between words (e.g., "machine-learning", "data-science", "ai")
- Are relevant to the content topic
- Complement the existing tags (avoid duplicates)
- Are useful for article categorization
- Follow format: single-word OR word-word OR word-word-word
- Examples: "artificial-intelligence", "blockchain", "startup", "healthcare", "education", "fintech"

REQUIRED JSON FORMAT (MANDATORY):
{{
  "title": "Concise and engaging title in Vietnamese (max 80 characters)",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "abstract": "Brief 2-3 sentence summary in Vietnamese, highlighting key points",
  "content": "<p>Engaging opening paragraph in Vietnamese introducing the topic...</p><h3>Subheading if needed (in Vietnamese)</h3><p>Detailed content completely translated into Vietnamese, using HTML tags like <strong>, <em>, <h3> for formatting. Split into multiple <p> paragraphs for readability. ENSURE COMPLETE TRANSLATION - do not truncate or shorten the content.</p><p><strong>Nguồn:</strong> <a href=\\"{source_url}\\" target=\\"_blank\\">{source_name}</a></p>"
}}
"""





