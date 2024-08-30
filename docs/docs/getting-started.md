# Getting started


The model files  are saved in the  **models/weights/**  folder.

the model files must be in **PyTorch** format.

The model names must be **`yolov8n-obb.pt` `yolov8s-obb.pt` `yolov8m-obb.pt` `yolov8l-obb.pt` `yolov8x-obb.pt`**

The `classes.txt` files are saved in the  **models/**  folder.

## Configuration file
backup file in the folder `backup/config.json`

### Config.json


1. **preference** - display the settings tab `true` or `false`


2. **db_confidence** - the confidence threshold above which the database entry is from `0 to 1`


3. **db_use_conf_model** - to write to the database, use the confidence threshold set for detecting the model `true` or `false`


4. **db_save** - writing to the database use `DataBase` , to a file in the YOLO  format use `File`, do not record use `Disabled`

- the rest of the parameters are changed by the program

## Makefile

### Help
- List of commands and their description 

```shell
make help
```

### Install
- Set up python interpreter environment

```shell
make create_venv
```

- Install required packages with pip

```shell
make requirements
```

### Start
- Launching the application

```shell
make run
```

### Debug
- Deletes compiled Python files and temporary directories.

```shell
make clear
```

- Checks the code for compliance with the style and the presence of errors using flake8 and isort.

```shell
make lint
```


### Data Base 
Our application uses a **PostgreSQL** database by default. To switch to a different database, simply configure the **src/utils/db_config.py** file.


#### Configuration

- Create an .env file to securely store your database credentials:

```shell
make db_env
```

- Variables of the **env** file

```shell


    DB_USER=your-user


    DB_PASS=your-pass


    DB_NAME=vtormet_yolo_db


    DB_PORT=5432


    DB_HOST=localhost  
```

#### Creating
- Creating a database and tables for recording detection results:

```shell
make db_create
```


- Creating directories to write detection results to files

```shell
make folders_create
```
#### Dump

- Data Base
Creates a dump of the database and images into an archive in the data folder and database tables and cleans up the database.

```shell
make dump_db
```

- Files
Creates a dump of directories with images and labels and cleans them

```shell
make dump_files
```

#### Clean
- Clears database tables and deletes images.

```shell
make clear_db
```

- Clears directories with images and labels.

```shell
make clear_folders
```



### MkDocs
#### Install

```shell
make install_docs
```
#### Create site
MkDocs is a static site generator that creates a website from Markdown files.

```shell
make build_docs
```

#### Start site
MkDocs launches your documentation site at [ http://127.0.0.1:8000/]( http://127.0.0.1:8000/)

```shell
make serve_docs
```