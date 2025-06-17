#this is the script I used - it's most likely underoptimized. Feel free to fix it. I actually welcome all fixes. 
import json
import argparse
#I couldn't figure out argparse for the life of me, had to resort to help here.
def searchlogs(filename, eventid=None, input_cmd=None, message=None,
               sensor=None, timestamp=None, src_ip=None, session=None, duration=None):
    results = []
    with open(filename, 'r') as file1:
        for line in file1:
            try:
                log_entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if eventid and log_entry.get('eventid') != eventid:
                continue
            if input_cmd and log_entry.get('input') != input_cmd:
                continue
            if message and log_entry.get('message') != message:
                continue
            if sensor and log_entry.get('sensor') != sensor:
                continue
            if timestamp and log_entry.get('timestamp') != timestamp:
                continue
            if src_ip and log_entry.get('src_ip') != src_ip:
                continue
            if session and log_entry.get('session') != session:
                continue
            if duration and log_entry.get('duration') != duration:
                continue

            results.append(log_entry)
    return results
#added a Help for each function because I know I'm going to forget at some point
def main():
    parser = argparse.ArgumentParser(description="Search Cowrie JSON logs")
    parser.add_argument("filename", help="Path to Cowrie JSON log file")
    parser.add_argument("--eventid", help="Filter by eventid")
    parser.add_argument("--input", dest="input_cmd", help="Filter by input command (field 'input')")
    parser.add_argument("--message", help="Filter by message")
    parser.add_argument("--sensor", help="Filter by sensor")
    parser.add_argument("--timestamp", help="Filter by timestamp")
    parser.add_argument("--src_ip", help="Filter by source IP")
    parser.add_argument("--session", help="Filter by session ID")
    parser.add_argument("--duration", help="Filter by duration")

    parser.add_argument("--write", action="store_true", help="Write output to results.json instead of printing")
    #also added a --write flag in case you want to write to a 'results.json' instead of printing the output. You can also change this to write to whatever file you want.
    args = parser.parse_args()

    results = searchlogs(
        args.filename,
        eventid=args.eventid,
        input_cmd=args.input_cmd,
        message=args.message,
        sensor=args.sensor,
        timestamp=args.timestamp,
        src_ip=args.src_ip,
        session=args.session,
        duration=args.duration,
    )

    print(f"Results found: {len(results)}")

    if args.write:
        with open("results.json", "w") as ofile:
            for entry in results:
                ofile.write(json.dumps(entry) + "\n")
        print("Results written to results.json")
    else:
        for entry in results:
            print(json.dumps(entry, indent=4))
#pretty print output, actually readable because the indent is set to 4
if __name__ == "__main__":
    main()
