def split_string_into_chunks(long_string: str, max_chars: int) -> list[str]:
    if len(long_string) <= max_chars:
        return [long_string]
        
    chunks = []
    remaining_text = long_string
    
    # First calculate max prefix length for worst case
    max_prefix_length = len(f"[XX/XX] ")  # Placeholder for max possible prefix
    available_chars = max_chars - max_prefix_length
    
    while remaining_text:
        if len(remaining_text) <= available_chars:
            chunks.append(remaining_text)
            break
            
        # Find break point
        split_index = available_chars
        
        # Try to break at sentence
        sentence_break = max(
            remaining_text.rfind('. ', 0, split_index),
            remaining_text.rfind('? ', 0, split_index),
            remaining_text.rfind('! ', 0, split_index)
        )
        if sentence_break > available_chars * 0.5:
            split_index = sentence_break + 1
            
        # Fall back to word break
        elif (word_break := remaining_text.rfind(' ', 0, split_index)) != -1:
            split_index = word_break
            
        chunk = remaining_text[:split_index].strip()
        remaining_text = remaining_text[split_index:].strip()
        chunks.append(chunk)
    
    # Add prefixes after knowing total chunk count
    if len(chunks) > 1:
        total = len(chunks)
        chunks = [f"[{i+1}/{total}] {chunk}" for i, chunk in enumerate(chunks)]
        
    return chunks
