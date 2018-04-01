GH_REF=git@github.com:networkx/grave.git

try:
	git checkout website -- _build/html
	git mv -f _build/html/* .
	git mv -f _build/html/.[a-zA-Z]* .

update-website:
	git clone --quiet --branch=website --depth=1 ${GH_REF} website_build
	cp -a website_build/_build/html/* .
	git status
	@echo
	@echo "If this looks correct, then add, commit, and push."
