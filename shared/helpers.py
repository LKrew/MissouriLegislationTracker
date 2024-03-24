def split_string_into_chunks(long_string, max_chars):
    chunks = []
    current_chunk = ""
    max_chars_per_chunk = max_chars - len("(x/y) ")

    while long_string:
        # Find the index where the next chunk should end
        index = max_chars_per_chunk
        if '\n' in long_string[:index]:
            index = long_string.index('\n') + 1
        elif ' ' in long_string[:index]:
            index = long_string.rindex(' ') + 1

        # Extract the chunk and remove it from the long string
        chunk = long_string[:index]
        long_string = long_string[index:].lstrip()

        # Append chunk
        if current_chunk:
            current_chunk += chunk
        else:
            current_chunk = chunk

        # Check if adding this chunk exceeds the max_chars_per_chunk
        if len(current_chunk) > max_chars_per_chunk:
            chunks.append(current_chunk[:-len(chunk)])
            current_chunk = chunk

    # Append the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    # Calculate total number of chunks
    total_chunks = len(chunks)
    
    # Append chunk count if there is more than one chunk
    if total_chunks > 1:
        for i, chunk in enumerate(chunks):
            chunks[i] = f"({i+1}/{total_chunks}) {chunk}"

    return chunks