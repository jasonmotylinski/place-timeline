"""Load script to ingest title_placements.csv into Elasticsearch."""
import logging
import md5

from datetime import datetime
from collections import deque
from optparse import OptionParser
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

es = Elasticsearch()


def read(path):
    """Read the CSV and yield actions."""
    m = md5.new()
    log.info("read: Reading file: %s", path)
    with open(path) as f:
        for line in f:
            parts = line.split(",")
            if parts[0].strip() != "ts":
                row = {"ts": datetime.fromtimestamp(float(parts[0].strip()) / 1000),
                       "user": parts[1].strip(),
                       "x_coordinate": int(parts[2].strip()),
                       "y_coordinate": int(parts[3].strip()),
                       "color": parts[4].strip()
                      }
                m.update('{0}{1}'.format(row["ts"], row['user']))
                doc_id = m.hexdigest()
                yield {
                    '_op_type': 'index',
                    '_index': 'tile_placements',
                    '_type': 'tile_placement',
                    '_id': doc_id,
                    'doc': row}

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file",
                      help="The path to the tile_placements.csv file.")
    (options, args) = parser.parse_args()

    if not options.file:
        parser.error("File not provided. -f is required.")
    deque(streaming_bulk(es, read(options.file), chunk_size=50000))
