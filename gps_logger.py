import gps
import time


# Function to save GPS coordinates to a file
def log_gps_data():
    # Open a file to save the data
    with open('/var/log/gps_data.log', 'a') as file:
        # Start the GPS session
        session = gps.gps('localhost', '2947')
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        try:
            while True:
                report = session.next()
                # Wait for a 'TPV' report and check if it has the 'lat' attribute
                if report['class'] == 'TPV':
                    if hasattr(report, 'lat') and hasattr(report, 'lon'):
                        # Log the latitude and longitude
                        file.write(
                            f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Latitude: {report.lat}, Longitude: {report.lon}\n")
                        file.flush()
                time.sleep(10)  # Log every 10 seconds
        except KeyError:
            pass  # Ignore reports that do not contain position data
        except KeyboardInterrupt:
            exit()  # Gracefully handle Ctrl+C


# Run the function
if __name__ == '__main__':
    log_gps_data()
