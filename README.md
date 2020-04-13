# managebac-file-scraper

This is a python script that downloads all files listed within the Files tab of ManageBac. It authenticates using your credentials, iterates over each class, and queues the downloads to an asynchronous download thread.

## Usage

```cmd
python3 scrape.py school_code username password output_dir [class_name]
```

- `school_code` is the part between `https://` and `.managebac.com`.
- `username` is your login email address.
- `password` is your password.
- `output_dir` is where all your downloads go. Each class gets its own subfolder inside.
- The optional `class_name` is where you can specify a single class name (has to be identical word-for-word to what's on your ManageBac)

You can view this help through the optional `-h` or `--help` argument.

## Disclaimer

This script was made for the sole intent of backing up every class material before I left the school. While I did provide the `school_code` argument to make the script universal for all schools using ManageBac, this script isn't capable of handling every single edge case out there. If some part of this script can be of use, go ahead and fork it to create a version specific to your school.

Since I have graduated my school now, I can't fix/test/add anything to this script either. This repository exists as an archive and any issues or pull requests will not be accepted.

## License

GNU General Public License v3.0. See LICENSE.md for more details.
