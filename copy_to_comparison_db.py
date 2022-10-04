from influxdb import InfluxDBClient
from dateutil import parser

unix_epoch_string = '1970-01-01T00:00:00.000000Z'
synthetic = parser.parse(unix_epoch_string)

client = InfluxDBClient(host='jmeter-influxdb.default.svc.cluster.local', port=8086,
                        database='jmeterdb')
new_client = InfluxDBClient(host='jmeter-influxdb.default.svc.cluster.local', port=8086,
                            database='comparison')

tags = client.query('SHOW TAG VALUES FROM "jmeter" WITH KEY IN ("scenario")')

original_tags = []

for point in tags.get_points():
    original_tags.append(point['value'])

print('Detected following scenarios in jmeterdb:' + ','.join(original_tags))

tags = new_client.query('SHOW TAG VALUES FROM "jmeter" WITH KEY IN ("scenario")')

comparison_tags = []

for point in tags.get_points():
    comparison_tags.append(point['value'])

print('Detected following scenarios in comparison:' + ','.join(comparison_tags))

missing = list(set(original_tags) - set(comparison_tags))

print('Tags which are not in the comparision database:' + ','.join(missing))

for scenario in missing:

    print('Processing scenario: ' + scenario)
    db_data = client.query(
        'SELECT * from "jmeter" where scenario=\'' + scenario + '\'')

    delta = None


    def calculate_synthetic_date(original):
        time_from_influx = parser.parse(original)
        global delta
        if delta == None:
            delta = time_from_influx - synthetic
        new_time = time_from_influx - delta
        return new_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


    data_to_write = [{'measurement': 'jmeter',
                      'tags': {'application': d['application'],
                               #'responseCode': d['responseCode'],
                               #'responseMessage': d['responseMessage'],
                               'statut': d['statut'],
                               'transaction': d['transaction'],
                               'scenario': d['scenario'],
                               },
                      'time': calculate_synthetic_date(d['time']),
                      'fields': {'avg': d['avg'],
                                 'count': d['count'],
                                 'countError': d['countError'],
                                 'endedT': d['endedT'],
                                 'hit': d['hit'],
                                 'max': d['max'],
                                 'maxAT': d['maxAT'],
                                 'meanAT': d['meanAT'],
                                 'min': d['min'],
                                 'minAT': d['minAT'],
                                 'pct90.0': d['pct90.0'],
                                 'pct95.0': d['pct95.0'],
                                 'pct99.0': d['pct99.0'],
                                 'rb': d['rb'],
                                 'sb': d['sb'],
                                 'startedT': d['startedT']
                                 }
                      }
                     for d in db_data.get_points()]
    new_client.write_points(data_to_write)
