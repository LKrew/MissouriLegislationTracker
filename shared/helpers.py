def split_string_into_chunks(long_string, max_chars):
    """
    Splits a given long string into chunks of maximum length `max_chars`. 
    Each chunk is appended to a list and returned at the end. 
    If the total number of chunks is greater than 1, the chunk count is appended to each chunk.
    
    :param long_string: The string to be split into chunks.
    :type long_string: str
    :param max_chars: The maximum length of each chunk.
    :type max_chars: int
    :return: A list of chunks, where each chunk is a substring of `long_string`.
    :rtype: List[str]
    """
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