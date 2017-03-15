solr/bin/solr start -p 8983
solr/bin/solr create -c viator_core
cp manage-schema solr/server/solr/viator_core/conf