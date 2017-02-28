solr/bin/solr start -p 4000
solr/bin/solr create -c viator_core
cp manage-schema solr/server/solr/viator_core/conf