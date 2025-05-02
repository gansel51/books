import csv
import json
from collections import Counter

def parse_goodreads_csv(csv_file):
    """Parse Goodreads export CSV and compute library statistics."""
    
    # Initialize counters
    stats = {
        'volumes_collected': 0,
        'books_read': 0,
        'distinct_authors': set(),
        'shelves': Counter(),
        'ratings_distribution': Counter(),
        'reading_by_year': Counter(),
        'top_authors': Counter()
    }
    
    try:
        # Read the CSV file
        with open(csv_file, 'r', encoding='utf-8') as f:
            # Create a CSV reader
            reader = csv.reader(f)
            
            # Skip the header line with column names
            next(reader)
            
            # Skip the separator line (dashes)
            next(reader)
            
            # Process each book
            for row in reader:
                # Check if we have a valid row with enough columns
                if len(row) < 20:
                    continue
                    
                book_id = row[0].strip() if row[0] else ""
                title = row[1].strip() if row[1] else ""
                author = row[2].strip() if row[2] else ""
                author_lf = row[3].strip() if row[3] else ""  # Last name, First name format
                additional_authors = row[4].strip() if row[4] else ""
                isbn = row[5].strip() if row[5] else ""
                isbn13 = row[6].strip() if row[6] else ""
                my_rating = row[7].strip() if row[7] else "0"
                avg_rating = row[8].strip() if row[8] else "0"
                publisher = row[9].strip() if row[9] else ""
                binding = row[10].strip() if row[10] else ""
                num_pages = row[11].strip() if row[11] else "0"
                year_published = row[12].strip() if row[12] else "0"
                orig_publication_year = row[13].strip() if row[13] else "0"
                date_read = row[14].strip() if row[14] else ""
                date_added = row[15].strip() if row[15] else ""
                bookshelves = row[16].strip() if row[16] else ""
                bookshelves_pos = row[17].strip() if row[17] else ""
                exclusive_shelf = row[18].strip() if row[18] else ""
                my_review = row[19].strip() if row[19] else ""
                
                # Check if this book is in the NYC collection
                if "nyc-collection" in bookshelves.lower():
                    stats['volumes_collected'] += 1
                    
                    # Add author to distinct authors set
                    if author:
                        stats['distinct_authors'].add(author)
                        stats['top_authors'][author] += 1
                    
                    # Check if additional authors exist and add them too
                    if additional_authors:
                        for add_author in additional_authors.split(','):
                            add_author = add_author.strip()
                            if add_author:
                                stats['distinct_authors'].add(add_author)
                
                # Check if this book has been read
                # Only count books that are explicitly on the "read" shelf
                if exclusive_shelf.lower() == "read":
                    stats['books_read'] += 1
                
                # Count books by shelf
                if bookshelves:
                    for shelf in bookshelves.split(','):
                        shelf = shelf.strip()
                        if shelf:
                            stats['shelves'][shelf] += 1
                
                # Count ratings distribution
                try:
                    if my_rating and my_rating != "0":
                        stats['ratings_distribution'][int(float(my_rating))] += 1
                except ValueError:
                    # Skip invalid ratings
                    pass
                
                # Count reading by publication year
                try:
                    if orig_publication_year and orig_publication_year != "0":
                        stats['reading_by_year'][orig_publication_year] += 1
                except ValueError:
                    # Skip invalid years
                    pass
        
        # Convert the distinct authors set to count
        stats['distinct_authors_count'] = len(stats['distinct_authors'])
        
        # Get top 5 authors
        stats['top_authors'] = dict(stats['top_authors'].most_common(5))
        
        # Get top 5 shelves
        stats['shelves'] = dict(stats['shelves'].most_common(5))
        
        # Convert set to list for JSON serialization
        stats['distinct_authors'] = list(stats['distinct_authors'])
        
        return stats
    
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found")
        return None
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return None

def generate_html_snippet(stats):
    """Generate an HTML snippet for the statistics section."""
    
    if not stats:
        return "<p>Error: No statistics available</p>"
    
    html = f"""
    <!-- Library Stats -->
    <section class="library-stats">
      <h2>The Collection</h2>
      <div class="stats-container">
        <div class="stat-card">
          <i class="fas fa-book-open"></i>
          <span class="stat-number">{stats['volumes_collected']}</span>
          <span class="stat-label">Volumes Collected</span>
        </div>
        <div class="stat-card">
          <i class="fas fa-bookmark"></i>
          <span class="stat-number">{stats['books_read']}</span>
          <span class="stat-label">Books Completed</span>
        </div>
        <div class="stat-card">
          <i class="fas fa-feather"></i>
          <span class="stat-number">{stats['distinct_authors_count']}</span>
          <span class="stat-label">Beloved Authors</span>
        </div>
      </div>
    </section>
    """
    
    return html

def process_library(csv_file_path, output_format='both', output_file='library_stats'):
    """
    Process a Goodreads library export file and generate statistics.
    
    Args:
        csv_file_path (str): Path to the Goodreads export CSV file
        output_format (str): Output format ('json', 'html', or 'both')
        output_file (str): Base name for output files (without extension)
        
    Returns:
        dict: The statistics dictionary or None if processing failed
    """
    # Generate statistics
    stats = parse_goodreads_csv(csv_file_path)
    
    if not stats:
        return None
    
    # Output based on selected format
    if output_format in ['json', 'both']:
        with open(f"{output_file}.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        print(f"JSON statistics written to {output_file}.json")
    
    if output_format in ['html', 'both']:
        html_snippet = generate_html_snippet(stats)
        with open(f"{output_file}.html", 'w', encoding='utf-8') as f:
            f.write(html_snippet)
        print(f"HTML snippet written to {output_file}.html")
    
    # Print summary to console
    print("\nLibrary Statistics Summary:")
    print(f"Volumes Collected: {stats['volumes_collected']}")
    print(f"Books Read: {stats['books_read']}")
    print(f"Distinct Authors: {stats['distinct_authors_count']}")
    
    # Print top 5 shelves
    print("\nTop 5 Shelves:")
    for shelf, count in stats['shelves'].items():
        print(f"  {shelf}: {count} books")
    
    # Print top 5 authors
    print("\nTop 5 Authors:")
    for author, count in stats['top_authors'].items():
        print(f"  {author}: {count} books")
        
    return stats

# Example usage
if __name__ == "__main__":
    # Configure these variables to match your needs
    goodreads_csv = "docs/assets/goodreads_library_export.csv"  # Change this to your file path
    output_format = "both"  # Options: "json", "html", or "both"
    output_file = "library_stats"  # Base name for output files (without extension)
    
    # Process the library
    process_library(goodreads_csv, output_format, output_file)