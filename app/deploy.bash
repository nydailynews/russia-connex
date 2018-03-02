#!/bin/bash
# scp flat files to prod.
# Deploy to QA: ./deploy.bash
# Deploy to prod: ./deploy.bash --server prod
ENVIRON='PROD'
export environ=$ENVIRON
SERVER='qa'
DIR='/apps/project/'
PROJECT='donald-trump-ties-russia-key-players'
LOCATION_OVERRIDE=0
html_only() { 
    echo ''
}

while [ "$1" != "" ]; do
    case $1 in
        -e | --environ ) shift
            ENVIRON=$1
            ;;
        -p | --project ) shift
            PROJECT=$1
            ;;
        -s | --server ) shift
            SERVER=$1
            ;;
        -d | --dir ) shift
            DIR=$1
            ;;
        -h | --htmlonly ) shift
            html_only() {
                find public \! -name "*.html" -type f -delete;
            }
            ;;
        -f | --freeze ) shift
            python freeze.py; export environ='DEV'; exit 1
            ;;
    esac
    shift
done

# If we bailed on deploy mid-deploy we'll still have the public dir around.
if [ -d "$PROJECT" ]; then rm -fr $PROJECT; fi

# J-A-N-K-Y
curl http://interactive.nydailynews.com/project/donald-trump-ties-russia-key-players/tag-russia-1.html > tag-russia-1.html
#wget -O tag-russia-1.html http://interactive.nydailynews.com/project/donald-trump-ties-russia-key-players/tag-russia-1.html

#python tests.py && \
html_only && \
    python freeze.py && \
    mv build $PROJECT && \
    scp -r $PROJECT $SERVER:$DIR && \
    mv $PROJECT build

export environ='DEV'
