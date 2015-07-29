set -e
git checkout master
git pull
bower install
ssh frans.chnet 'cd /srv/www/dienst2 && sudo -u www-dienst2 git pull'
rsync -r -v --del dienst2/static/lib frans.chnet:/srv/www/dienst2/dienst2/static/
ssh frans.chnet 'cd /srv/www/dienst2 && chmod -Rf ug=rwX,o-rwx .; chgrp -Rf dienst2 .; sudo -u www-dienst2 ./update.sh'