#!/bin/bash 

celery -A checking  beat -l debug
