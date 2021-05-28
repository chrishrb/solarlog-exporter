#!/bin/sh
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

cleanup () {
  docker-compose -p ci -f docker-compose.test.yml down
  docker-compose -p ci -f docker-compose.test.yml rm
}

cleanup

# Test Container
trap 'cleanup ; printf "${RED}Tests Failed For Unexpected Reasons${NC}\n"' HUP INT QUIT PIPE TERM
docker-compose -p ci -f docker-compose.test.yml build && docker-compose -p ci -f docker-compose.test.yml up -d
if [ $? -ne 0 ] ; then
  printf "${RED}Docker Compose Failed${NC}\n"
  exit -1
fi

TEST_EXIT_CODE=`docker wait ci_solarlog-exporter_1`
docker logs ci_solarlog-exporter_1
if [ -z ${TEST_EXIT_CODE+x} ] || [ "$TEST_EXIT_CODE" -ne 0 ] ; then
  docker logs ci_solarlog-exporter_1
  docker logs ci_influxdb_1
  printf "${RED}Tests Failed${NC} - Exit Code: $TEST_EXIT_CODE\n"
else
  printf "${GREEN}Tests Passed${NC}\n"
fi

cleanup

exit $TEST_EXIT_CODE