The snapshot folder contains a snapshot of the entire YouPorn repository. This is stored in snapshot.dat.

The temporal folder contains ~2k files, each containing the data for an individual video. The filename contains the video's identifier. Each row contains a recorded set of meta-data for the video. Please note that errors could result in non-contiguous entries (i.e. skipping days).

The schema for all data files is as follows:

Timestamp, Timestamp_date, Vid_ID, Rating, Num_Rating, Length, Views, Up_date, Age, Categories, Num_Categories, Num_Comments, User

The length (duration) is measured in seconds. The age is measured in days. Dates are in the format of DD-MM-YYYY. The categories are separated using semi colons and a space, e.g. "amateur; latina".
