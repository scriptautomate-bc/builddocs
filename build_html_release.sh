#!/bin/bash -ex
# Downloads a salt docs-html release tarball and runs it through the same
# post-processing as a from-source build, instead of rebuilding released
# versions from scratch.

if [ -z "${WEBSITE_RELEASE}" ]
then
	echo "ERROR: Missing environment variable WEBSITE_RELEASE"
	exit 1
fi

if [ -z "${RELEASE_VERSION}" ]
then
	echo "ERROR: Missing environment variable RELEASE_VERSION"
	exit 1
fi

. ./build_env.sh
. ./build_html_common.sh

curl -fsSL -o docs-html.tar.xz \
	"https://github.com/saltstack/salt/releases/download/v${RELEASE_VERSION}/salt-${RELEASE_VERSION}-docs-html.tar.xz"

rm -rf ./release_html
mkdir -p ./release_html
tar xf docs-html.tar.xz -C ./release_html

postprocess_html_dir ./release_html
