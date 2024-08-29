Generating the docs
----------

## Use [mkdocs](http://www.mkdocs.org/) structure to update the documentation. 




## Build locally with:

    pip install mkdocs
    
    pip install mkdocs-material

    mkdocs build -f ./docs/mkdocs.yml

## Serve locally with:

    mkdocs serve -f ./docs/mkdocs.yml

## Use Makefile commands

    make install_docs             Install MkDocs

    make build_docs               Create site MkDocs

    make serve_docs               Start site MkDocs
