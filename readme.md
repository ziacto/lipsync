```markdown
# Lip Sync Script

This script performs lip synchronization for a given video and audio using the SyncLabs API.

## How to use

1. Install the requirements using:
   ```bash
   pip install -r requirements.txt
   ```

2. Create accounts on SyncLabs and Supabase.

3. On Supabase, create a bucket that will store the data. It currently needs to be public and called `translation`.

4. Create a `.env` file with the following variables:
   ```
   SYNC_API_KEY=your_sync_api_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

5. Place the video and audio files in the Supabase bucket and update the script with their URLs.

6. Run the script using:
   ```bash
   python main.py
   ```

## Script Description

- The script uses the SyncLabs API for lip synchronization.
- The script checks the status of the lip sync job until it is completed or failed.
- The final video is downloaded once the lip sync process is completed.

## Requirements

- `requests`
- `python-dotenv`
```

This README file provides the necessary steps and information to set up and run the script, focusing on the essential details and removing any unnecessary information.