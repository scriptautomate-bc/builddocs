#!/bin/bash
# Shared HTML post-processing, used by both the from-source build (master)
# and the release-tarball extraction path (latest/3008/3006).
# Must be sourced, not executed.

postprocess_html_dir() {
	local html_dir="$1"

	if [ -z "${WEBSITE_RELEASE}" ]
	then
		echo "ERROR: Missing environment variable WEBSITE_RELEASE"
		exit 1
	fi

	rm -rf "${html_dir}/_sources"
	echo "ErrorDocument 404 /en/${WEBSITE_RELEASE}/404.html" > "${html_dir}/.htaccess"

	# The 404 page has relative links.  We may or may not want to just move these changes to the actual built docs in the future.
	sed -i "s#\"contents.html#\"/en/${WEBSITE_RELEASE}/contents.html#g" "${html_dir}/404.html"
	sed -i "s#\"faq.html#\"/en/${WEBSITE_RELEASE}/faq.html#g" "${html_dir}/404.html"
	sed -i "s#\"genindex.html#\"/en/${WEBSITE_RELEASE}/genindex.html#g" "${html_dir}/404.html"
	sed -i "s#\"glossary.html#\"/en/${WEBSITE_RELEASE}/glossary.html#g" "${html_dir}/404.html"
	sed -i "s#\"home.html#\"/en/${WEBSITE_RELEASE}/home.html#g" "${html_dir}/404.html"
	sed -i "s#\"_images#\"/en/${WEBSITE_RELEASE}/_images#g" "${html_dir}/404.html"
	sed -i "s#\"index.html#\"/en/${WEBSITE_RELEASE}/index.html#g" "${html_dir}/404.html"
	sed -i "s#\"py-modindex.html#\"/en/${WEBSITE_RELEASE}/py-modindex.html#g" "${html_dir}/404.html"
	sed -i "s#\"ref#\"/en/${WEBSITE_RELEASE}/ref#g" "${html_dir}/404.html"
	sed -i "s#\"salt-modindex.html#\"/en/${WEBSITE_RELEASE}/salt-modindex.html#g" "${html_dir}/404.html"
	sed -i "s#\"search.html#\"/en/${WEBSITE_RELEASE}/search.html#g" "${html_dir}/404.html"
	sed -i "s#\"security#\"/en/${WEBSITE_RELEASE}/security#g" "${html_dir}/404.html"
	sed -i "s#\"_static#\"/en/${WEBSITE_RELEASE}/_static#g" "${html_dir}/404.html"
	sed -i "s#\"topics#\"/en/${WEBSITE_RELEASE}/topics#g" "${html_dir}/404.html"

	# Dealing with this bug: https://github.com/saltstack/salt/issues/52777
	if [ -f "${html_dir}/py-modindex.html" ] && [ ! -e "${html_dir}/salt-modindex.html" ]
	then
		echo '<meta http-equiv="refresh" content="0; url=py-modindex.html" />' > "${html_dir}/salt-modindex.html"
	fi

	if [ ! -e "${html_dir}/salt-modindex.html" ]
	then
		echo "ERROR: salt-modindex.html is missing"
		exit 1
	fi

	echo '<meta http-equiv="refresh" content="0; url=contents.html" />' > "${html_dir}/index.html"
	mkdir -p ./public/
	rsync -a "${html_dir}/" "./public/${WEBSITE_RELEASE}/"
}
