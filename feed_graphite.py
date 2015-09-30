#!/usr/bin/env python

import argparse
import json
import socket
import time
import urllib2

parser = argparse.ArgumentParser()
parser.add_argument('--graphite_host', required=True, nargs='?', help='graphite_host')
parser.add_argument('--graphite_port', required=True, type=int, nargs='?', help='graphite_port')
parser.add_argument('--goProbe_url', required=True, nargs='?', help='goProbe metric url path')
parser.add_argument('--mode', default='once', nargs='?', help='can be either once or continuous')
parser.add_argument('--interval', type=int, default=60, nargs='?', help='sleep time when run in continuous mode')


args = parser.parse_args()
print args.graphite_host

def GraphiteMetrics():
  vars =['probe_count', 'probe_error_count', 'probe_timeout_count', 'probe_latency', 'probe_payload_size', 'probe_up']

  resp = urllib2.urlopen(args.goProbe_url)
  data = json.loads(resp.read())

  metrics = []
  for var in vars:
    for key, val in data[var].iteritems():
      single_metric = '%s.%s %s %d\n' % (var, key, val['value'], val['time'])
      metrics.append(single_metric)

  metric_message = "".join(metrics)
  print metric_message
  sock = socket.socket()
  sock.connect((args.graphite_host, args.graphite_port))
  sock.sendall(metric_message)
  sock.close()

def main():
  if args.mode == 'continuous':
    while  True:
  	  GraphiteMetrics()
  	  print 'Done..'
  	  print 'Sleeping for %d secs..' % args.interval
  	  time.sleep(args.interval)
  else:
  	GraphiteMetrics()
  	print 'Done..'

if __name__ == '__main__':
	main()