tree=$(tree -tf -I "__pycache__|jspm_packages|*.pyc|__init__.py|static|*facebook.json|*facebook.csv|*.js|*.html|etc" --charset ascii $1 |
       sed -e 's/| \+/  /g' -e 's/[|`]-\+/ */g' -e 's:\(* \)\(\(.*/\)\([^/]\+\)\):\1[\4](\2):g')

printf "# Project tree\n\n${tree}"
