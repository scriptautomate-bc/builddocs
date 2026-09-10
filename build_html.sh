#!/bin/bash -ex
# Builds HTML docs from source. Used for master only -- released versions
# are consumed as pre-built tarballs by build_html_release.sh.

if [ -z "${WEBSITE_RELEASE}" ]
then
	echo "ERROR: Missing environment variable WEBSITE_RELEASE"
	exit 1
fi

. ./build_env.sh
. ./build_html_common.sh

SALT_ON_SALTSTACK=true make -C salt/doc html SPHINX_OPTS=-W
postprocess_html_dir salt/doc/_build/html
