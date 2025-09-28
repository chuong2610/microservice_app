"""
Advanced Fuzzy Matching for Author Names

This module provides robust fuzzy matching for author names. It aims to be:

- Resilient to casing, accents/diacritics, punctuation, and spacing differences
- Tolerant to small typos and partial matches
- Useful for both exact full-name queries and partial/incomplete inputs

Scoring is a combination of multiple signals:
1) Exact normalized equality
2) Full-string similarity (SequenceMatcher ratio)
3) Word-level coverage and fuzzy containment
4) Substring containment (query in name or name in query)
5) Initials heuristic for short queries

Only high-level comments are added to clarify intent; the matching logic remains unchanged.
"""

import re
import unicodedata
from difflib import SequenceMatcher
from typing import List, Dict, Any, Tuple

def _normalize_text(text: str) -> str:
    """Normalize text for fuzzy matching.

    Steps:
    - Lowercase
    - Decompose unicode to strip diacritics (accents)
    - Replace punctuation with spaces, collapse repeated whitespace
    """
    if not text:
        return ""
    
    text = text.lower()
    
    normalized = unicodedata.normalize('NFD', text)
    without_accents = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    
    cleaned = re.sub(r'[^\w\s]', ' ', without_accents)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def fuzzy_match_authors(query: str, all_authors: List[Dict[str, Any]], k: int) -> List[Tuple[Dict[str, Any], float]]:
    """Return top-k author matches for a query with a composite fuzzy score."""
    if not all_authors:
        return []
    
    matches = []
    
    # Normalize once for efficiency and consistent comparisons
    query_normalized = _normalize_text(query)
    query_words = query_normalized.split()
    
    for author in all_authors:
        full_name = author.get("full_name", "")
        if not full_name:
            continue
            
        # Normalize candidate name and split into words
        name_normalized = _normalize_text(full_name)
        name_words = name_normalized.split()
        
        # 1) Exact match (after normalization)
        exact_match_score = 0.0
        if query_normalized == name_normalized:
            exact_match_score = 1.0
        
        # 2) Full-string similarity (ratio in [0, 1])
        full_similarity = SequenceMatcher(None, query_normalized, name_normalized).ratio()
        
        # 3) Word-level coverage with fuzzy containment/typo tolerance
        word_match_score = 0.0
        if query_words and name_words:
            matched_words = 0
            total_query_words = len(query_words)
            
            for query_word in query_words:
                if query_word in name_words:
                    matched_words += 1
                else:
                    # If not an exact word hit, consider partial and fuzzy matches
                    for name_word in name_words:
                        if len(query_word) >= 3 and query_word in name_word:
                            matched_words += 0.7
                            break
                        elif len(name_word) >= 3 and name_word in query_word:
                            matched_words += 0.7
                            break
                        else:
                            word_sim = SequenceMatcher(None, query_word, name_word).ratio()
                            if word_sim >= 0.8:
                                matched_words += word_sim
                                break
            
            word_match_score = matched_words / total_query_words if total_query_words > 0 else 0.0
        
        # 4) Substring containment (favoring longer overlaps)
        substring_score = 0.0
        if query_normalized in name_normalized:
            substring_score = 0.9 * (len(query_normalized) / len(name_normalized))
        elif name_normalized in query_normalized:
            substring_score = 0.8 * (len(name_normalized) / len(query_normalized))
        
        # 5) Initials heuristic: for short queries, require successive word-initial matches
        initials_score = 0.0
        if len(query_words) <= 3 and len(name_words) >= len(query_words):
            initials_match = True
            for i, query_word in enumerate(query_words):
                if i < len(name_words):
                    if not name_words[i].startswith(query_word[0]):
                        initials_match = False
                        break
            if initials_match:
                initials_score = 0.7
        
        # Combine signals. Using max() keeps the highest strong signal and avoids overcounting.
        final_score = max(
            exact_match_score * 1.0,
            full_similarity * 0.9,
            word_match_score * 0.95,
            substring_score * 0.85,
            initials_score * 0.7
        )
        
        # Slight boost for plausible short-name matches to favor concise, relevant results
        if final_score > 0.5 and len(name_normalized) <= len(query_normalized) + 5:
            final_score = min(1.0, final_score * 1.1)
        
        # Keep only minimally plausible candidates to limit noise
        if final_score > 0.05:
            matches.append((author, final_score))
    
    # Sort by descending score and return top-k
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:k]

